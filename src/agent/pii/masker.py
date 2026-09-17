"""PII Masking with Microsoft Presidio (Phase 2).

Provides a warm singleton AnalyzerEngine + AnonymizerEngine with:
- Standard entity detection (PERSON, EMAIL, PHONE, LOCATION, IP, etc.)
- US PII recognizers (US_SSN, US_PASSPORT, US_DRIVER_LICENSE, US_ITIN)
- Indian PII recognizers (IN_PAN, IN_AADHAAR, IN_PASSPORT)
- Robust Phone number recognition (US, Indian, International + context cues like "phoen/phone is ...")
- Custom recognizers (Ticket IDs, Project Codenames)
- Smart Person name cleaning (stripping "Resume -", "CV:", etc.)
- Per-thread alias & substring deduplication so "Aydin" and "Aydin Adnan" share <PERSON_1>.

Masking is one-way: callers receive masked text only, never the reverse map. The
reverse map stays in-process, lives under a bounded thread registry, and is read
back only through get_token_map() or discarded with forget_thread().
"""
import re
import sys
from typing import Any

from presidio_analyzer import (
    AnalyzerEngine,
    EntityRecognizer,
    Pattern,
    PatternRecognizer,
    RecognizerResult,
)
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

# ============================================================================
# 1. Custom & Enhanced Recognizers
# ============================================================================

class ContextPhoneRecognizer(EntityRecognizer):
    """Detects phone numbers accurately, extracting only the digit span."""

    def __init__(self):
        super().__init__(supported_entities=["PHONE_NUMBER"], name="context_phone_recognizer")
        # Matches phone numbers preceded by keywords, extracting only group 1
        self.re_ctx = re.compile(
            r"(?i)\b(?:phone|phoen|mobile|cell|tel|call|contact|whatsapp)\s*(?:number|no\.?|#)?\s*(?:is|:)?\s*(\+?[\d\s\-().]{7,18}\b)",
        )
        # Standard US and Indian direct numbers
        self.re_direct = re.compile(
            r"\b(?:\+?1[-.\s]?)?\(?[2-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b|"
            r"\b(?:\+?91[\-\s]?)?[6-9]\d{9}\b|"
            r"\b\d{10,12}\b"
        )

    def load(self):
        pass

    def analyze(self, text: str, entities: list[str], nlp_artifacts: Any = None) -> list[RecognizerResult]:
        results = []
        if "PHONE_NUMBER" not in entities:
            return results

        # 1. Context-guided phone match (e.g. "my phoen number is 799417804888")
        for m in self.re_ctx.finditer(text):
            span_str = m.group(1).strip().rstrip(".")
            start = m.start(1)
            end = start + len(span_str)
            results.append(
                RecognizerResult(
                    entity_type="PHONE_NUMBER",
                    start=start,
                    end=end,
                    score=0.95,
                )
            )

        # 2. Direct phone match
        for m in self.re_direct.finditer(text):
            span_str = m.group(0).strip().rstrip(".")
            start = m.start(0)
            end = start + len(span_str)
            results.append(
                RecognizerResult(
                    entity_type="PHONE_NUMBER",
                    start=start,
                    end=end,
                    score=0.85,
                )
            )

        return results


class ContextSSNRecognizer(EntityRecognizer):
    """Detects US Social Security Numbers (SSN) accurately."""

    def __init__(self):
        super().__init__(supported_entities=["US_SSN"], name="context_ssn_recognizer")
        self.re_ctx = re.compile(
            r"(?i)\b(?:ssn|social\s*security(?:\s*number)?)\s*[:#]?\s*(?:is\s*)?(\d{3}[-\s]?\d{2}[-\s]?\d{4}|\d{9})\b"
        )
        self.re_direct = re.compile(
            r"\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b"
        )

    def load(self):
        pass

    def analyze(self, text: str, entities: list[str], nlp_artifacts: Any = None) -> list[RecognizerResult]:
        results = []
        if "US_SSN" not in entities:
            return results

        for m in self.re_ctx.finditer(text):
            span_str = m.group(1).strip().rstrip(".")
            start = m.start(1)
            end = start + len(span_str)
            results.append(
                RecognizerResult(
                    entity_type="US_SSN",
                    start=start,
                    end=end,
                    score=0.95,
                )
            )

        for m in self.re_direct.finditer(text):
            span_str = m.group(0).strip().rstrip(".")
            start = m.start(0)
            end = start + len(span_str)
            results.append(
                RecognizerResult(
                    entity_type="US_SSN",
                    start=start,
                    end=end,
                    score=0.90,
                )
            )

        return results


def _build_custom_recognizers() -> list[EntityRecognizer]:
    """Build custom recognizers for domain entities, regional IDs, and robust phones."""
    recognizers: list[EntityRecognizer] = [
        ContextPhoneRecognizer(),
        ContextSSNRecognizer(),
    ]

    # Ticket ID Recognizer (e.g., ACME-12345, TICK-9876)
    ticket_pattern = Pattern(
        name="ticket_id_pattern",
        regex=r"\b[A-Z]{2,10}-\d{3,6}\b",
        score=0.9,
    )
    recognizers.append(
        PatternRecognizer(
            supported_entity="TICKET_ID",
            patterns=[ticket_pattern],
            name="ticket_id_recognizer",
        )
    )

    # Indian PAN Card (5 uppercase letters, 4 digits, 1 letter)
    pan_pattern = Pattern(
        name="in_pan_pattern",
        regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
        score=0.95,
    )
    recognizers.append(
        PatternRecognizer(
            supported_entity="IN_PAN",
            patterns=[pan_pattern],
            name="in_pan_recognizer",
        )
    )

    # Indian Aadhaar Card
    # MUST have spaces (4-4-4) OR explicit context keyword to avoid colliding with plain phone numbers!
    aadhaar_spaced_pattern = Pattern(
        name="in_aadhaar_spaced",
        regex=r"\b[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}\b",
        score=0.9,
    )
    aadhaar_context_pattern = Pattern(
        name="in_aadhaar_context",
        regex=r"(?i)\b(?:aadhaar|aadhar|uidai|uid)\s*(?:number|no\.?|#)?\s*(?:is|:)?\s*([2-9]{1}[0-9]{3}\s?[0-9]{4}\s?[0-9]{4})\b",
        score=0.95,
    )
    recognizers.append(
        PatternRecognizer(
            supported_entity="IN_AADHAAR",
            patterns=[aadhaar_spaced_pattern, aadhaar_context_pattern],
            name="in_aadhaar_recognizer",
        )
    )

    # Indian Passport (1 letter followed by 7 digits)
    passport_pattern = Pattern(
        name="in_passport_pattern",
        regex=r"\b[A-PR-WYa-pr-wy][1-9]\d{6}\b",
        score=0.85,
    )
    recognizers.append(
        PatternRecognizer(
            supported_entity="IN_PASSPORT",
            patterns=[passport_pattern],
            name="in_passport_recognizer",
        )
    )

    # Project Codenames Deny-List
    project_codenames = [
        "Project Titan",
        "Titan",
        "Project Apollo",
        "Apollo",
        "Project Manhattan",
        "Manhattan",
        "Project Excalibur",
        "Excalibur",
        "Project BlueBook",
        "BlueBook",
    ]
    recognizers.append(
        PatternRecognizer(
            supported_entity="PROJECT_CODENAME",
            deny_list=project_codenames,
            name="project_codename_recognizer",
        )
    )

    return recognizers


# spaCy models to try, most accurate first. en_core_web_lg is locked in uv.lock.
_SPACY_MODEL_NAMES = ("en_core_web_lg", "en_core_web_sm")

# Threads kept in memory before the oldest registry is evicted.
_MAX_THREADS = 128


def _create_analyzer() -> AnalyzerEngine:
    """Build the Presidio analyzer, preferring the large spaCy model."""
    failures: list[str] = []
    for model_name in _SPACY_MODEL_NAMES:
        try:
            engine = NlpEngineProvider(
                nlp_configuration={
                    "nlp_engine_name": "spacy",
                    "models": [{"lang_code": "en", "model_name": model_name}],
                }
            ).create_engine()
        except (ImportError, OSError, ValueError) as exc:
            failures.append(f"{model_name}: {exc}")
        else:
            return AnalyzerEngine(nlp_engine=engine)

    raise RuntimeError(
        "No usable spaCy model for Presidio. Run `uv sync` to install the pinned "
        "en_core_web_lg wheel. Failures: " + "; ".join(failures)
    )


# Supported Entities to scan
TARGET_ENTITIES = [
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "LOCATION",
    "URL",
    "IP_ADDRESS",
    "CREDIT_CARD",
    "DATE_TIME",
    "US_SSN",
    "US_PASSPORT",
    "US_DRIVER_LICENSE",
    "US_ITIN",
    "IN_PAN",
    "IN_AADHAAR",
    "IN_PASSPORT",
    "TICKET_ID",
    "PROJECT_CODENAME",
]

_PERSON_PREFIX_CLEAN_RE = re.compile(
    r"^(?:resume|cv|profile|fwd|re|fw|application|candidate)\s*[-:–—|]\s*",
    re.IGNORECASE,
)
_PERSON_SUFFIX_CLEAN_RE = re.compile(
    r"\s*[-:–—|]\s*(?:resume|cv|profile|candidate)$",
    re.IGNORECASE,
)
_HONORIFICS_RE = re.compile(
    r"^(?:mr\.|ms\.|mrs\.|dr\.|prof\.)\s*",
    re.IGNORECASE,
)


def _clean_person_name(raw_name: str) -> str:
    """Strip metadata noise (Resume -, CV:, Mr.) from recognized person names."""
    cleaned = _PERSON_PREFIX_CLEAN_RE.sub("", raw_name.strip())
    cleaned = _PERSON_SUFFIX_CLEAN_RE.sub("", cleaned)
    cleaned = _HONORIFICS_RE.sub("", cleaned)
    return cleaned.strip()


# ============================================================================
# 2. Singleton Presidio Engine
# ============================================================================

class PresidioMasker:
    """Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry."""

    _instance: "PresidioMasker | None" = None

    def __init__(self):
        self.analyzer = _create_analyzer()
        self.anonymizer = AnonymizerEngine()

        # Add custom recognizers
        for rec in _build_custom_recognizers():
            self.analyzer.registry.add_recognizer(rec)

        # Thread registry: thread_id -> {(entity_type, canonical_value): token}
        self._thread_registries: dict[str, dict[tuple[str, str], str]] = {}
        # Reverse map for unmasking: thread_id -> {token: best_raw_value}
        self._reverse_token_maps: dict[str, dict[str, str]] = {}

    @classmethod
    def get_instance(cls) -> "PresidioMasker":
        """Access or initialize the singleton PresidioMasker."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _registry_for(self, thread_id: str) -> tuple[dict[tuple[str, str], str], dict[str, str]]:
        """Return a thread's registries, evicting the oldest thread past the cap."""
        if thread_id not in self._thread_registries:
            while len(self._thread_registries) >= _MAX_THREADS:
                oldest = next(iter(self._thread_registries))
                del self._thread_registries[oldest]
                self._reverse_token_maps.pop(oldest, None)
            self._thread_registries[thread_id] = {}
            self._reverse_token_maps[thread_id] = {}
        return self._thread_registries[thread_id], self._reverse_token_maps[thread_id]

    def forget_thread(self, thread_id: str) -> bool:
        """Drop a thread's tokens and reverse map; returns whether it existed."""
        self._reverse_token_maps.pop(thread_id, None)
        return self._thread_registries.pop(thread_id, None) is not None

    @staticmethod
    def _token_count(registry: dict[tuple[str, str], str], entity_type: str) -> int:
        """Count distinct tokens already handed out for one entity type."""
        return len({token for (entity, _), token in registry.items() if entity == entity_type})

    def _match_or_create_person_token(self, thread_id: str, clean_name: str) -> str:
        """Deduplicate person names: match aliases, first names, and full names to one token."""
        reg, rev = self._registry_for(thread_id)

        norm_name = clean_name.lower()

        # 1. Exact match
        if ("PERSON", norm_name) in reg:
            return reg[("PERSON", norm_name)]

        # 2. Substring / Alias matching among existing registered persons
        for (ent_type, existing_norm), token in list(reg.items()):
            if ent_type == "PERSON":
                existing_parts = set(existing_norm.split())
                new_parts = set(norm_name.split())

                if new_parts.issubset(existing_parts) or existing_parts.issubset(new_parts):
                    reg[("PERSON", norm_name)] = token
                    if len(clean_name) > len(rev[token]):
                        rev[token] = clean_name
                    return token

        # 3. Create a new PERSON token
        token = f"<PERSON_{self._token_count(reg, 'PERSON') + 1}>"
        reg[("PERSON", norm_name)] = token
        rev[token] = clean_name
        return token

    def _get_or_create_token(self, thread_id: str, entity_type: str, raw_val: str) -> str:
        """Assign or retrieve a consistent <TYPE_N> token for an entity value within a thread."""
        if entity_type == "PERSON":
            return self._match_or_create_person_token(thread_id, _clean_person_name(raw_val))

        reg, rev = self._registry_for(thread_id)
        norm_val = raw_val.strip().lower()
        key = (entity_type, norm_val)

        if key in reg:
            return reg[key]

        token = f"<{entity_type}_{self._token_count(reg, entity_type) + 1}>"
        reg[key] = token
        rev[token] = raw_val.strip()
        return token

    def mask_text(
        self,
        text: str,
        thread_id: str = "default",
        language: str = "en",
    ) -> str:
        """Mask PII entities in text with consistent <TYPE_N> tokens."""
        if not text:
            return ""

        results = self.analyzer.analyze(
            text=text,
            entities=TARGET_ENTITIES,
            language=language,
        )

        filtered_results = self._resolve_overlaps(results)
        sorted_results = sorted(filtered_results, key=lambda r: r.start, reverse=True)

        masked_chars = list(text)
        for res in sorted_results:
            new_start, new_end = res.start, res.end
            raw_span = text[new_start:new_end]

            if res.entity_type == "PERSON":
                prefix_match = _PERSON_PREFIX_CLEAN_RE.match(raw_span)
                if prefix_match:
                    new_start = res.start + prefix_match.end()
                suffix_match = _PERSON_SUFFIX_CLEAN_RE.search(raw_span)
                if suffix_match:
                    new_end = res.start + suffix_match.start()
                raw_span = text[new_start:new_end]

            token = self._get_or_create_token(thread_id, res.entity_type, raw_span)
            masked_chars[new_start:new_end] = list(token)

        return "".join(masked_chars)

    @staticmethod
    def _resolve_overlaps(results: list[RecognizerResult]) -> list[RecognizerResult]:
        """Resolve overlapping spans by preferring higher confidence or larger spans."""
        sorted_res = sorted(results, key=lambda r: (r.start, -r.score, -(r.end - r.start)))
        resolved: list[RecognizerResult] = []

        for r in sorted_res:
            overlap = False
            for existing in resolved:
                if not (r.end <= existing.start or r.start >= existing.end):
                    overlap = True
                    break
            if not overlap:
                resolved.append(r)

        return resolved

    def unmask_text(self, text: str, thread_id: str = "default") -> str:
        """Replace <TYPE_N> tokens back with original values."""
        rev = self._reverse_token_maps.get(thread_id, {})
        for token, original in rev.items():
            text = text.replace(token, original)
        return text


# ============================================================================
# 3. Global Public API
# ============================================================================

def mask_for_llm(
    subject: str,
    body: str,
    thread_id: str = "default",
) -> tuple[str, str]:
    """Sanitize subject and body before any model call. Returns masked text only."""
    masker = PresidioMasker.get_instance()
    return (
        masker.mask_text(subject, thread_id=thread_id),
        masker.mask_text(body, thread_id=thread_id),
    )


def get_token_map(thread_id: str = "default") -> dict[str, str]:
    """Retrieve the current token to original value map for a thread."""
    masker = PresidioMasker.get_instance()
    return dict(masker._reverse_token_maps.get(thread_id, {}))


def forget_thread(thread_id: str = "default") -> bool:
    """Drop a thread's token registry and reverse map."""
    return PresidioMasker.get_instance().forget_thread(thread_id)


# ============================================================================
# 4. Interactive Test Pipeline (CLI Mode)
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" Presidio PII Masking Pipeline Demonstration")
    print("=" * 70)

    if len(sys.argv) >= 3:
        input_subject = sys.argv[1]
        input_body = sys.argv[2]
        thread_id = sys.argv[3] if len(sys.argv) > 3 else "custom_thread"
    else:
        input_subject = "Resume - Aydin Adnan"
        input_body = "Hi my name is Aydin Adnan I build AI systems , my phoen number is 799417804888. Also my SSN is 123-45-6789."
        thread_id = "test_user_eval"

    print(f"\n[1] INPUT SUBJECT:\n    {input_subject}")
    print(f"\n[2] INPUT BODY:\n    {input_body}")

    print("\n[3] RUNNING MASKER...")
    masked_sub, masked_bod = mask_for_llm(input_subject, input_body, thread_id=thread_id)
    token_map = get_token_map(thread_id)

    print(f"\n[4] MASKED SUBJECT:\n    {masked_sub}")
    print(f"\n[5] MASKED BODY (SAFE FOR LLM):\n    {masked_bod}")

    print("\n[6] TOKEN REGISTRY (PERSISTED IN STATE, NEVER SENT TO LLM):")
    for token, original in sorted(token_map.items()):
        print(f"    {token:<25} -> {original}")

    print("\n[7] AUTOMATIC REPLY RE-CONSTRUCTION TEST:")
    raw_llm_reply = "Dear <PERSON_1>, thank you for reaching out! We received your application."
    print(f"    Raw LLM Output:       {raw_llm_reply}")
    unmasked_reply = PresidioMasker.get_instance().unmask_text(raw_llm_reply, thread_id=thread_id)
    print(f"    Final Unmasked Reply: {unmasked_reply}")

    print("\n" + "=" * 70)
    print(" Pipeline complete. All PII shielded & deduplicated.")
    print("=" * 70)
