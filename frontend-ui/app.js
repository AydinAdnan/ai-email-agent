const el = (id) => document.getElementById(id);

let since = 0;
let timer = null;
let live = false;

async function api(path, body) {
  const response = await fetch(path, {
    method: body === undefined ? "GET" : "POST",
    headers: { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  return response.json();
}

// The run prints each arrival in a fixed shape: a header line, the fields it read, then the
// body indented under them. Reading that shape here is what makes the page a mailbox instead
// of a log.
const MAIL_FIELD = /^\s{2}(From|To|Subject|Thread|prior|Acted):\s*(.*)$/;
const MAIL_HEAD = /^\[\s*(\d+\/\d+)\]\s*(.*)$/;
const REPLY_LINE = /^\s*reply for (\S+):\s*'([\s\S]*)'\s*$/;
const VERDICT = /\[([A-Z_]+):/;

// The four routes as the plan names them, each with the colour the page shows it in.
const ROUTES = {
  PROCEED_SILENTLY: "silent",
  PROCEED_AND_NOTIFY: "notify",
  ASK_FIRST_WITH_PREDRAFT: "ask first",
  ESCALATE: "escalate",
};

// The four things a person can say about mail like this, as the lines the parser already
// accepts: a click and a typed line are the same input.
const CHOICES = [
  { route: "PROCEED_SILENTLY", label: "quietly", line: "ignore this sender" },
  { route: "PROCEED_AND_NOTIFY", label: "tell me", line: "notify me about this sender" },
  { route: "ASK_FIRST_WITH_PREDRAFT", label: "ask me first", line: "ask me first about this sender" },
  { route: "ESCALATE", label: "escalate", line: "always escalate these" },
];

const clean = (text) => text.split("\n").map((line) => line.trim()).join("\n").trim();
// The summary's own indentation is one level of structure worth keeping: the route counts
// line up under it, and the per-bucket lines sit one level in.
const strip = (text) => text.split("\n").map((line) => line.replace(/^ {4}/, "")).join("\n");

let summary = null;
// Which decision the buttons currently on screen were built for.
let actionsKey = "";

function parseMail(text) {
  const [head = "", ...rest] = text.split("\n");
  const mail = { step: "", id: "", prior: [], text: "" };
  const found = head.match(MAIL_HEAD);
  if (found) {
    mail.step = found[1];
    mail.id = found[2];
  }
  const body = [];
  let fields = false;
  for (const line of rest) {
    const field = line.match(MAIL_FIELD);
    if (field) {
      fields = true;
      const name = field[1].toLowerCase();
      if (name === "prior") {
        mail.prior.push(field[2]);
      } else {
        mail[name] = field[2];
      }
      continue;
    }
    // Indented and unprefixed means a body line; the four spaces are the run's, not the mail's.
    if (fields && (line.trim() === "" || /^\s{4}/.test(line))) {
      body.push(line.replace(/^\s{4}/, ""));
    }
  }
  mail.text = body.join("\n").replace(/^\n+/, "").replace(/\n+$/, "");
  return mail;
}

function renderMail(block, state) {
  const mail = parseMail(block.text);
  const node = el("mail-template").content.firstElementChild.cloneNode(true);
  node.dataset.case = mail.id;
  const pick = (selector) => node.querySelector(selector);
  pick(".step").textContent = mail.step;
  pick(".id").textContent = mail.id;
  pick(".sender").textContent = mail.from || "unknown sender";
  pick(".subject").textContent = mail.subject || "(no subject)";
  pick(".to").textContent = mail.to ? `to ${mail.to}` : "";
  // The route this arrival got, when the run has decided it: that is the coloured state.
  const route = (state.routes_by_case || {})[mail.id];
  const verdict = (mail.acted || "").match(VERDICT);
  const badge = pick(".verdict");
  badge.textContent = route ? ROUTES[route] : verdict ? verdict[1].replaceAll("_", " ").toLowerCase() : "";
  badge.hidden = !route && verdict === null;
  if (route) {
    badge.dataset.route = route;
    badge.title = route;
  }
  const prior = pick(".prior");
  for (const line of mail.prior) {
    const item = document.createElement("li");
    item.textContent = line;
    prior.append(item);
  }
  prior.hidden = mail.prior.length === 0;
  const body = pick("details");
  body.hidden = mail.text === "";
  pick(".text").textContent = mail.text;
  const acted = pick(".acted");
  acted.hidden = !mail.acted;
  pick(".acted .value").textContent = mail.acted || "";
  el("transcript").append(node);
}

function renderSaid(block) {
  const node = document.createElement("div");
  node.className = `block ${block.kind}`;
  const label = document.createElement("p");
  label.className = "label";
  const text = document.createElement("p");
  text.className = "said";
  const mine = block.kind === "reply" ? block.text.match(REPLY_LINE) : null;
  if (mine) {
    label.textContent = `you on ${mine[1]}`;
    text.textContent = mine[2];
  } else if (block.kind === "reply") {
    label.textContent = "you";
    text.textContent = clean(block.text);
  } else {
    label.textContent = block.kind === "wait" ? "needs you" : "agent";
    text.textContent = clean(block.text.replace(/^\s*\[waiting\]\s*/, ""));
  }
  node.append(label, text);
  el("transcript").append(node);
}

function renderSummary(block) {
  if (summary === null) {
    summary = document.createElement("div");
    summary.className = "block summary";
    const text = document.createElement("pre");
    summary.append(text);
    el("transcript").append(summary);
  }
  summary.querySelector("pre").textContent += `${strip(block.text)}\n`;
}

function renderRaw(block) {
  const node = document.createElement("div");
  node.className = `block ${block.kind}`;
  const text = document.createElement("pre");
  text.textContent = clean(block.text);
  node.append(text);
  el("transcript").append(node);
}

function renderBlock(block, state) {
  if (block.kind === "mail") {
    renderMail(block, state);
  } else if (block.kind === "summary") {
    renderSummary(block);
  } else if (["note", "wait", "reply"].includes(block.kind)) {
    renderSaid(block);
  } else {
    renderRaw(block);
  }
}

function renderList(id, items, empty) {
  const list = el(id);
  list.textContent = "";
  if (!items.length) {
    const only = document.createElement("li");
    only.className = "empty";
    only.textContent = empty;
    list.append(only);
    return;
  }
  for (const item of items) {
    const node = document.createElement("li");
    node.textContent = item;
    list.append(node);
  }
}

function renderState(partial) {
  const state = {
    waiting: false,
    done: false,
    case: "",
    error: "",
    count: 0,
    seen: 0,
    interrupts: 0,
    receipts: 0,
    routes: {},
    claims: [],
    posteriors: [],
    rules_file: "",
    rules_refusal: "",
    ...partial,
  };
  const counts = el("counts");
  counts.textContent = "";
  const rows = [
    ["mails decided", state.seen],
    ["asked for a line", state.interrupts],
    ["receipts", state.receipts],
  ];
  for (const [name, value] of rows) {
    const dt = document.createElement("dt");
    dt.textContent = name;
    const dd = document.createElement("dd");
    dd.textContent = String(value);
    counts.append(dt, dd);
  }
  for (const [route, count] of Object.entries(state.routes || {})) {
    const dt = document.createElement("dt");
    dt.textContent = route.toLowerCase().replaceAll("_", " ");
    dt.dataset.route = route;
    const dd = document.createElement("dd");
    dd.textContent = String(count);
    counts.append(dt, dd);
  }

  renderList("rules", state.claims || [], "nothing yet");
  renderList("posteriors", state.posteriors || [], "nothing counted yet");

  const notice = el("notice");
  notice.textContent = state.error
    ? state.error
    : state.rules_refusal
      ? `rules not kept: ${state.rules_refusal}`
      : state.rules_file
        ? `rules file: ${state.rules_file}`
        : "no rules file: this run keeps nothing";
  notice.className = state.error ? "notice bad" : "notice";

  const status = el("status");
  if (state.error) {
    status.textContent = `stopped: ${state.error}`;
  } else if (state.waiting) {
    status.textContent = `waiting for you on ${state.case}`;
  } else if (state.done) {
    status.textContent = "run finished. the rules it kept are in force for the next run.";
  } else if (live) {
    status.textContent = "running";
  }
  status.className = state.waiting || live ? "status live" : "status";

  el("line").disabled = !state.waiting;
  el("send").disabled = !state.waiting;
  if (state.waiting && document.activeElement !== el("line")) {
    el("line").focus();
  }
  renderActions(state);
}

function action(label, line, route, enabled, why = "") {
  const button = document.createElement("button");
  button.type = "button";
  button.className = route ? "action" : "action keep";
  button.textContent = label;
  button.title = enabled ? `say: ${line}` : why;
  button.disabled = !enabled;
  if (route) {
    button.dataset.route = route;
  }
  button.addEventListener("click", () => {
    for (const other of document.querySelectorAll(".action")) {
      other.disabled = true;
    }
    sendLine(line);
  });
  return button;
}

// The decisions under the message: what the run would accept as a line, offered as buttons.
// A choice that cannot quieten this decision is shown disabled rather than hidden, so the
// four states stay the same shape on every card. The row is rebuilt only when the decision
// or the question changes: a button that is replaced under the cursor cannot be clicked.
function renderActions(state) {
  const key = state.waiting ? `${state.case}|${state.confirming}|${state.quietenable}` : "";
  if (key === actionsKey) {
    return;
  }
  actionsKey = key;
  for (const row of document.querySelectorAll(".actions")) {
    row.remove();
  }
  if (!key) {
    return;
  }
  const card = document.querySelector(`.block.mail[data-case="${state.case}"]`);
  if (!card) {
    return;
  }
  const row = document.createElement("div");
  row.className = "actions";
  if (state.confirming) {
    row.append(action("yes, keep it", "yes", null, true), action("no", "no", null, true));
  } else {
    for (const choice of CHOICES) {
      const helps = state.quietenable || choice.route === "ESCALATE";
      row.append(
        action(
          choice.label,
          choice.line,
          choice.route,
          helps,
          "no rule quietens this one: it stays your call",
        ),
      );
    }
  }
  card.append(row);
}

async function poll() {
  const data = await api(`/api/poll?since=${since}`);
  for (const block of data.blocks) {
    renderBlock(block, data.state);
    since = Math.max(since, block.index + 1);
    el("transcript").scrollTop = el("transcript").scrollHeight;
  }
  renderState(data.state);
  if (data.state.done || data.state.error) {
    stopPolling();
  }
}

function startPolling() {
  live = true;
  el("start").disabled = true;
  el("stop").disabled = false;
  if (timer === null) {
    timer = setInterval(poll, 400);
  }
  poll();
}

function stopPolling() {
  live = false;
  el("start").disabled = false;
  el("stop").disabled = true;
  if (timer !== null) {
    clearInterval(timer);
    timer = null;
  }
}

// A run lives on the server, not in this tab: opening the page onto one already going shows
// it rather than pretending the inbox is empty.
async function attach() {
  const running = await api("/api/state");
  if (running.error || running.done) {
    return;
  }
  el("transcript").textContent = "";
  since = 0;
  startPolling();
}

el("controls").addEventListener("submit", async (event) => {
  event.preventDefault();
  const started = await api("/api/start", {
    fixture: el("fixture").value,
    lane: el("lane").value,
    seed: Number(el("seed").value),
    store: el("store").value,
    provider: el("provider").value,
  });
  if (started.error) {
    renderState({ error: started.error, routes: {}, claims: [], posteriors: [] });
    // The likeliest reason a run will not start is that one is already going, so the page
    // attaches to it instead of leaving the user with a message and a dead stop button.
    await attach();
    return;
  }
  el("transcript").textContent = "";
  since = 0;
  startPolling();
});

// Stop means end of input, not end of the page: the run keeps deciding the rest of the lane
// and the summary still has to arrive, so polling ends only when the run says it is done.
el("stop").addEventListener("click", async () => {
  await api("/api/stop", {});
  await poll();
});

async function sendLine(text) {
  const sent = await api("/api/reply", { text });
  if (sent.error) {
    renderState(sent);
    return;
  }
  await poll();
}

el("say").addEventListener("submit", async (event) => {
  event.preventDefault();
  const box = el("line");
  const text = box.value.trim();
  if (!text) {
    return;
  }
  box.value = "";
  box.disabled = true;
  el("send").disabled = true;
  await sendLine(text);
});

attach();
