/* DE Interview Practice - frontend */
(function () {
  "use strict";

  // ------------------------------------------------------------------ state
  const state = {
    problems: [],
    stats: null,
    current: null, // full problem payload
    editor: null, // CodeMirror instance or fallback textarea adapter
    timers: {}, // id -> {elapsed, running, lastTick}
    hintsRevealed: {}, // id -> count
    solutionShown: {}, // id -> bool
    draftTimer: null,
    running: false,
  };

  const $ = (sel) => document.querySelector(sel);
  const el = (tag, attrs = {}, children = []) => {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") node.className = v;
      else if (k === "text") node.textContent = v;
      else if (k === "html") node.innerHTML = v;
      else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
      else node.setAttribute(k, v);
    }
    for (const c of [].concat(children)) {
      if (c == null) continue;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    }
    return node;
  };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const cap = (s) => (s ? s[0].toUpperCase() + s.slice(1) : "");
  const fmtJson = (v) => JSON.stringify(v, null, v && typeof v === "object" && JSON.stringify(v).length > 80 ? 2 : 0);

  async function api(path, opts = {}) {
    const res = await fetch(path, {
      headers: { "Content-Type": "application/json" },
      ...opts,
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    });
    const data = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
    if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
    return data;
  }

  function toast(msg, kind = "") {
    const t = $("#toast");
    t.textContent = msg;
    t.className = `toast ${kind}`;
    clearTimeout(toast._h);
    toast._h = setTimeout(() => t.classList.add("hidden"), 2600);
  }

  function renderMarkdown(md) {
    if (window.marked) {
      try {
        return window.marked.parse(md, { gfm: true, breaks: false });
      } catch (e) {
        /* fall through */
      }
    }
    return `<pre>${esc(md)}</pre>`;
  }

  // ------------------------------------------------------------------ editor
  function initEditor() {
    const ta = $("#editor");
    if (window.CodeMirror) {
      const cm = window.CodeMirror.fromTextArea(ta, {
        mode: "python",
        theme: "material-darker",
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        matchBrackets: true,
        autoCloseBrackets: true,
        lineWrapping: false,
        extraKeys: {
          "Ctrl-Enter": runTests,
          "Cmd-Enter": runTests,
          "Ctrl-/": "toggleComment",
          Tab: (c) => {
            if (c.somethingSelected()) c.indentSelection("add");
            else c.replaceSelection(" ".repeat(c.getOption("indentUnit")), "end");
          },
        },
      });
      cm.on("change", scheduleDraftSave);
      state.editor = {
        get: () => cm.getValue(),
        set: (v) => {
          cm.setValue(v || "");
          cm.clearHistory();
        },
        mode: (m) => cm.setOption("mode", m === "sql" ? "text/x-sql" : "python"),
        focus: () => cm.focus(),
        refresh: () => cm.refresh(),
      };
    } else {
      ta.classList.add("fallback");
      ta.addEventListener("input", scheduleDraftSave);
      ta.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") runTests();
      });
      state.editor = {
        get: () => ta.value,
        set: (v) => (ta.value = v || ""),
        mode: () => {},
        focus: () => ta.focus(),
        refresh: () => {},
      };
    }
  }

  function scheduleDraftSave() {
    if (!state.current) return;
    clearTimeout(state.draftTimer);
    const id = state.current.id;
    state.draftTimer = setTimeout(() => {
      const code = state.editor.get();
      if (code === state.current.starter) return;
      api(`/api/problems/${encodeURIComponent(id)}/draft`, { method: "POST", body: { code } }).catch(() => {});
    }, 1500);
  }

  // ------------------------------------------------------------------ timer
  function timerFor(id) {
    if (!state.timers[id]) state.timers[id] = { elapsed: 0, running: true, lastTick: Date.now() };
    return state.timers[id];
  }
  function tick() {
    if (!state.current) return;
    const t = timerFor(state.current.id);
    if (t.running) {
      const now = Date.now();
      t.elapsed += (now - t.lastTick) / 1000;
      t.lastTick = now;
    }
    renderTimer();
  }
  function renderTimer() {
    if (!state.current) return;
    const t = timerFor(state.current.id);
    const s = Math.floor(t.elapsed);
    const mm = String(Math.floor(s / 60)).padStart(2, "0");
    const ss = String(s % 60).padStart(2, "0");
    const node = $("#timer");
    node.textContent = `${mm}:${ss}`;
    node.classList.toggle("paused", !t.running);
    $("#btn-timer-toggle").textContent = t.running ? "Pause" : "Resume";
  }
  function pauseAll() {
    for (const t of Object.values(state.timers)) t.running = false;
  }
  setInterval(tick, 500);

  // ------------------------------------------------------------------ list
  function populateTags() {
    const tags = new Set();
    state.problems.forEach((p) => p.tags.forEach((t) => tags.add(t)));
    const sel = $("#f-tag");
    const cur = sel.value;
    sel.innerHTML = '<option value="">All tags</option>';
    [...tags].sort().forEach((t) => sel.appendChild(el("option", { value: t, text: t })));
    sel.value = cur;
  }

  function filteredProblems() {
    const q = $("#f-search").value.trim().toLowerCase();
    const lang = $("#f-language").value;
    const diff = $("#f-difficulty").value;
    const status = $("#f-status").value;
    const tag = $("#f-tag").value;
    return state.problems.filter(
      (p) =>
        (!lang || p.language === lang) &&
        (!diff || p.difficulty === diff) &&
        (!status || p.status === status) &&
        (!tag || p.tags.includes(tag)) &&
        (!q || p.title.toLowerCase().includes(q) || p.tags.some((t) => t.includes(q)))
    );
  }

  function renderList() {
    const list = $("#problem-list");
    list.innerHTML = "";
    const items = filteredProblems();
    if (!items.length) {
      list.appendChild(el("div", { class: "list-empty", text: "No problems match these filters." }));
      return;
    }
    let lastGroup = null;
    for (const p of items) {
      const group = p.language === "python" ? "Python" : "SQL";
      if (group !== lastGroup) {
        list.appendChild(el("li", { class: "list-group", text: group }));
        lastGroup = group;
      }
      const li = el(
        "li",
        { class: state.current && state.current.id === p.id ? "active" : "", onclick: () => openProblem(p.id) },
        [
          el("span", { class: `status-dot ${p.status}`, title: cap(p.status) }),
          el("div", {}, [
            el("div", { class: "pl-title", text: p.title }),
            el("div", { class: "pl-sub", text: p.tags.slice(0, 3).join(" · ") }),
          ]),
          el("div", { class: "pl-right" }, [el("span", { class: `diff-pill ${p.difficulty}`, text: cap(p.difficulty) })]),
        ]
      );
      list.appendChild(li);
    }
  }

  function renderStats() {
    const s = state.stats;
    if (!s) return;
    const d = s.by_difficulty || {};
    const part = (k) => (d[k] ? `${d[k].solved}/${d[k].total}` : "0/0");
    $("#stats").innerHTML =
      `<span>Solved <b>${s.solved}</b> / ${s.total}</span>` +
      `<span>Easy <b>${part("easy")}</b></span>` +
      `<span>Medium <b>${part("medium")}</b></span>` +
      `<span>Hard <b>${part("hard")}</b></span>`;
  }

  async function loadProblems() {
    const data = await api("/api/problems");
    state.problems = data.problems;
    state.stats = data.stats;
    populateTags();
    renderList();
    renderStats();
  }

  // ------------------------------------------------------------------ problem view
  async function openProblem(id) {
    if (state.current && state.current.id !== id) {
      // keep other timers paused when you switch away
      const t = timerFor(state.current.id);
      t.running = false;
    }
    let p;
    try {
      p = await api(`/api/problems/${encodeURIComponent(id)}`);
    } catch (e) {
      toast(e.message, "bad");
      return;
    }
    state.current = p;
    location.hash = encodeURIComponent(id);
    $("#problem-empty").classList.add("hidden");
    $("#problem-content").classList.remove("hidden");

    $("#p-title").textContent = p.title;
    const st = $("#p-status");
    st.textContent = cap(p.status);
    st.className = `status-pill ${p.status}`;
    const dp = $("#p-difficulty");
    dp.textContent = cap(p.difficulty);
    dp.className = `diff-pill ${p.difficulty}`;
    const lp = $("#p-language");
    lp.textContent = p.language === "sql" ? "SQL (DuckDB)" : "Python";
    lp.className = `lang-pill ${p.language}`;
    $("#p-tags").innerHTML = p.tags.map((t) => `<span class="tag">${esc(t)}</span>`).join("");
    $("#editor-lang").textContent = p.language === "sql" ? "SQL" : "Python";
    $("#editor-lang").className = `lang-pill ${p.language}`;

    // description + schema
    const desc = $("#tab-description");
    desc.innerHTML = renderMarkdown(p.statement);
    if (p.language === "sql") desc.appendChild(renderSchema(p));
    if (p.language === "python") {
      desc.appendChild(
        el("p", {
          class: "table-note",
          text: `${p.test_count} test cases. Keep the function name "${p.function_name}" and its signature.`,
        })
      );
    } else {
      desc.appendChild(
        el("p", {
          class: "table-note",
          text: `${p.dataset_names.length} datasets: ${p.dataset_names.join(", ")}. ` +
            (p.order_matters ? "Row order IS graded." : "Row order is not graded; column order is."),
        })
      );
    }

    renderHints();
    renderSolutionTab();
    $("#tab-submissions").innerHTML = "";
    switchTab("description");

    // editor
    state.editor.mode(p.language);
    state.editor.set(p.draft && p.draft.trim() ? p.draft : p.starter);
    setTimeout(() => {
      state.editor.refresh();
      state.editor.focus();
    }, 0);
    $("#btn-run").disabled = false;
    $("#results").innerHTML = '<div class="results-placeholder">Results show up here after you run the tests.</div>';

    // timer
    const t = timerFor(id);
    if (p.status !== "solved") {
      t.running = true;
      t.lastTick = Date.now();
    }
    renderTimer();
    renderList();
  }

  function renderSchema(p) {
    const wrap = el("div", { class: "schema" });
    wrap.appendChild(el("h3", { text: "Tables (first dataset)" }));
    for (const t of p.schema || []) {
      const det = el("details", { open: "" });
      const summary = el("summary", {}, [
        t.name,
        el("span", { class: "cols", text: `${t.row_count} rows · ${t.columns.map((c) => c.name).join(", ")}` }),
      ]);
      det.appendChild(summary);
      const table = el("table");
      const thead = el("tr");
      t.columns.forEach((c) => thead.appendChild(el("th", {}, [c.name, el("span", { class: "type", text: c.type })])));
      table.appendChild(thead);
      for (const row of t.sample) {
        const tr = el("tr");
        row.forEach((v) => tr.appendChild(el("td", { class: v === null ? "null" : "", text: v === null ? "NULL" : String(v) })));
        table.appendChild(tr);
      }
      det.appendChild(table);
      if (t.row_count > t.sample.length) det.appendChild(el("div", { class: "table-note", text: `Showing ${t.sample.length} of ${t.row_count} rows.` }));
      wrap.appendChild(det);
    }
    return wrap;
  }

  function renderHints() {
    const p = state.current;
    const pane = $("#tab-hints");
    pane.innerHTML = "";
    const shown = state.hintsRevealed[p.id] || 0;
    if (!p.hints.length) {
      pane.appendChild(el("div", { class: "empty", text: "No hints for this problem." }));
      return;
    }
    p.hints.forEach((h, i) => {
      if (i < shown) {
        pane.appendChild(el("div", { class: "hint" }, [el("div", { class: "hint-label", text: `Hint ${i + 1}` }), el("div", { text: h })]));
      } else if (i === shown) {
        pane.appendChild(
          el("div", { class: "hint locked" }, [
            el("span", { text: `Hint ${i + 1} of ${p.hints.length}` }),
            el("button", {
              class: "btn btn-small",
              text: "Reveal",
              onclick: () => {
                state.hintsRevealed[p.id] = shown + 1;
                renderHints();
              },
            }),
          ])
        );
      }
    });
  }

  function renderSolutionTab() {
    const p = state.current;
    const pane = $("#tab-solution");
    pane.innerHTML = "";
    if (state.solutionShown[p.id]) {
      loadSolution();
      return;
    }
    pane.appendChild(
      el("div", { class: "solution-warning" }, [
        p.solution_viewed
          ? "You have looked at this solution before. "
          : "Try for at least 20 minutes before peeking. ",
        "Looking at the solution is recorded in your progress.",
      ])
    );
    pane.appendChild(
      el("button", {
        class: "btn",
        text: "Show solution",
        onclick: () => {
          if (p.status !== "solved" && !confirm("Reveal the reference solution for this problem?")) return;
          state.solutionShown[p.id] = true;
          loadSolution();
        },
      })
    );
  }

  async function loadSolution() {
    const p = state.current;
    const pane = $("#tab-solution");
    pane.innerHTML = '<div class="empty">Loading...</div>';
    try {
      const data = await api(`/api/problems/${encodeURIComponent(p.id)}/solution`);
      pane.innerHTML = "";
      pane.appendChild(el("div", { class: "code-block", text: data.solution.trim() }));
      pane.appendChild(
        el("div", { style: "margin:8px 0 16px" }, [
          el("button", {
            class: "btn btn-small",
            text: "Copy into editor",
            onclick: () => {
              if (confirm("Replace your editor contents with the reference solution?")) state.editor.set(data.solution);
            },
          }),
        ])
      );
      const expl = el("div", { class: "markdown" });
      expl.innerHTML = renderMarkdown(data.explanation || "_No explanation written for this problem yet._");
      pane.appendChild(expl);
      const item = state.problems.find((x) => x.id === p.id);
      if (item) item.solution_viewed = true;
    } catch (e) {
      pane.innerHTML = `<div class="empty">${esc(e.message)}</div>`;
    }
  }

  async function loadSubmissions() {
    const p = state.current;
    const pane = $("#tab-submissions");
    pane.innerHTML = '<div class="empty">Loading...</div>';
    const data = await api(`/api/problems/${encodeURIComponent(p.id)}/submissions`);
    pane.innerHTML = "";
    if (!data.submissions.length) {
      pane.appendChild(el("div", { class: "empty", text: "No submissions yet." }));
      return;
    }
    const table = el("table", { class: "sub-table" });
    table.appendChild(el("tr", {}, ["When", "Status", "Tests", "Runtime", "Timer", ""].map((h) => el("th", { text: h }))));
    for (const s of data.submissions) {
      const cls = s.status === "accepted" ? "ok" : s.status === "wrong_answer" ? "bad" : "warn";
      table.appendChild(
        el("tr", {}, [
          el("td", { text: s.created_at.replace("T", " ") }),
          el("td", { class: cls, text: statusLabel(s.status) }),
          el("td", { text: `${s.passed}/${s.total}` }),
          el("td", { text: s.runtime_ms != null ? `${s.runtime_ms} ms` : "-" }),
          el("td", { text: s.elapsed_s != null ? fmtElapsed(s.elapsed_s) : "-" }),
          el("td", {}, [el("button", { class: "btn btn-small", text: "Load code", onclick: () => state.editor.set(s.code) })]),
        ])
      );
    }
    pane.appendChild(table);
  }

  const fmtElapsed = (s) => `${Math.floor(s / 60)}m ${s % 60}s`;
  const statusLabel = (s) =>
    ({ accepted: "Accepted", wrong_answer: "Wrong answer", error: "Error", time_limit: "Time limit" }[s] || s);

  function switchTab(name) {
    document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("active", t.dataset.tab === name));
    document.querySelectorAll(".tab-pane").forEach((p) => p.classList.toggle("active", p.id === `tab-${name}`));
    if (name === "submissions" && state.current) loadSubmissions().catch((e) => toast(e.message, "bad"));
  }

  // ------------------------------------------------------------------ running
  async function runTests() {
    if (!state.current || state.running) return;
    const p = state.current;
    const code = state.editor.get();
    state.running = true;
    const btn = $("#btn-run");
    btn.disabled = true;
    btn.textContent = "Running...";
    $("#results").innerHTML = '<div class="result-summary"><span class="running">Running tests...</span></div>';
    try {
      const t = timerFor(p.id);
      const result = await api("/api/run", { method: "POST", body: { id: p.id, code, elapsed_s: Math.floor(t.elapsed) } });
      renderResults(result, p.language);
      if (result.status === "accepted") {
        t.running = false;
        renderTimer();
        toast(`Accepted - ${p.title} solved in ${fmtElapsed(Math.floor(t.elapsed))}`, "good");
      }
      // refresh status in list/header
      const item = state.problems.find((x) => x.id === p.id);
      if (item) item.status = result.problem_status;
      p.status = result.problem_status;
      $("#p-status").textContent = cap(p.status);
      $("#p-status").className = `status-pill ${p.status}`;
      renderList();
      loadProblems().catch(() => {});
    } catch (e) {
      $("#results").innerHTML = `<div class="result-summary error">Server error</div><div class="kv"><pre class="err">${esc(e.message)}</pre></div>`;
    } finally {
      state.running = false;
      btn.disabled = false;
      btn.textContent = "Run tests";
    }
  }

  function renderResults(r, language) {
    const box = $("#results");
    box.innerHTML = "";
    const label = {
      accepted: "Accepted",
      wrong_answer: "Wrong answer",
      error: "Runtime error",
      time_limit: "Time limit exceeded",
    }[r.status] || r.status;
    box.appendChild(
      el("div", { class: `result-summary ${r.status}` }, [
        el("span", { text: label }),
        el("span", { class: "meta", text: `${r.passed}/${r.total} ${language === "sql" ? "datasets" : "tests"} passed · ${r.runtime_ms} ms` }),
      ])
    );
    if (r.stderr) box.appendChild(kv("stderr", r.stderr, "err"));
    r.results.forEach((c, i) => {
      const det = el("details", { class: `case ${c.passed ? "pass" : "fail"}` });
      if (!c.passed) det.open = true;
      det.appendChild(
        el("summary", {}, [
          el("span", { text: c.passed ? "PASS" : "FAIL" }),
          el("span", { text: c.name || `Test ${i + 1}` }),
          el("span", { class: "ms", text: c.ms != null ? `${c.ms} ms` : "" }),
        ])
      );
      const body = el("div", { class: "case-body" });
      if (language === "python") {
        body.appendChild(kv("Input", fmtJson(c.input)));
        body.appendChild(kv("Expected", fmtJson(c.expected)));
        if (c.error) body.appendChild(kv("Error", c.error, "err"));
        else body.appendChild(kv("Actual", fmtJson(c.actual)));
        if (c.stdout) body.appendChild(kv("stdout", c.stdout));
      } else {
        if (c.error) body.appendChild(kv("Error", c.error, "err"));
        else if (c.message && c.message !== "OK") body.appendChild(kv("Why it failed", c.message, "msg"));
        (c.warnings || []).forEach((w) => body.appendChild(kv("Warning", w, "warn")));
        const grid = el("div", { class: "grid-2" });
        grid.appendChild(sqlTable("Expected", c.expected));
        if (c.actual) grid.appendChild(sqlTable("Your output", c.actual));
        body.appendChild(grid);
      }
      det.appendChild(body);
      box.appendChild(det);
    });
  }

  function kv(label, text, cls = "") {
    return el("div", { class: "kv" }, [el("div", { class: "k", text: label }), el("pre", { class: cls, text: text })]);
  }

  function sqlTable(label, t) {
    const wrap = el("div", { class: "kv" });
    wrap.appendChild(el("div", { class: "k", text: `${label} (${t.total_rows} rows)` }));
    const scroll = el("div", { class: "table-scroll" });
    const table = el("table", { class: "sql-table" });
    table.appendChild(el("tr", {}, t.columns.map((c) => el("th", { text: c }))));
    for (const row of t.rows) {
      table.appendChild(
        el("tr", {}, row.map((v) => el("td", { class: v === null ? "null" : "", text: v === null ? "NULL" : typeof v === "object" ? JSON.stringify(v) : String(v) })))
      );
    }
    scroll.appendChild(table);
    wrap.appendChild(scroll);
    if (t.total_rows > t.rows.length) wrap.appendChild(el("div", { class: "table-note", text: `Showing first ${t.rows.length} rows.` }));
    return wrap;
  }

  // ------------------------------------------------------------------ actions
  async function randomUnsolved() {
    const lang = $("#f-language").value;
    const diff = $("#f-difficulty").value;
    const data = await api(`/api/random?language=${lang}&difficulty=${diff}`);
    if (!data.id) {
      toast("Nothing unsolved left for these filters. Nice.", "good");
      return;
    }
    openProblem(data.id);
  }

  async function resetProgress() {
    const p = state.current;
    if (!p || !confirm(`Reset all progress for "${p.title}"? Submissions, draft and solved status will be deleted.`)) return;
    await api(`/api/problems/${encodeURIComponent(p.id)}/reset`, { method: "POST", body: {} });
    delete state.timers[p.id];
    delete state.hintsRevealed[p.id];
    delete state.solutionShown[p.id];
    await loadProblems();
    openProblem(p.id);
  }

  function resetCode() {
    const p = state.current;
    if (!p || !confirm("Replace the editor with the starter code?")) return;
    state.editor.set(p.starter);
    api(`/api/problems/${encodeURIComponent(p.id)}/draft`, { method: "POST", body: { code: "" } }).catch(() => {});
  }

  // ------------------------------------------------------------------ boot
  function bind() {
    $("#btn-run").addEventListener("click", runTests);
    $("#btn-random").addEventListener("click", () => randomUnsolved().catch((e) => toast(e.message, "bad")));
    $("#btn-reset-progress").addEventListener("click", () => resetProgress().catch((e) => toast(e.message, "bad")));
    $("#btn-reset-code").addEventListener("click", resetCode);
    $("#btn-timer-toggle").addEventListener("click", () => {
      if (!state.current) return;
      const t = timerFor(state.current.id);
      t.running = !t.running;
      t.lastTick = Date.now();
      renderTimer();
    });
    $("#btn-timer-reset").addEventListener("click", () => {
      if (!state.current) return;
      const t = timerFor(state.current.id);
      t.elapsed = 0;
      t.lastTick = Date.now();
      renderTimer();
    });
    document.querySelectorAll(".tab").forEach((t) => t.addEventListener("click", () => switchTab(t.dataset.tab)));
    ["#f-search", "#f-language", "#f-difficulty", "#f-status", "#f-tag"].forEach((sel) =>
      $(sel).addEventListener("input", renderList)
    );
    document.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        runTests();
      }
    });
    window.addEventListener("hashchange", () => {
      const id = decodeURIComponent(location.hash.slice(1));
      if (id && (!state.current || state.current.id !== id)) openProblem(id);
    });
  }

  async function boot() {
    initEditor();
    bind();
    try {
      await loadProblems();
    } catch (e) {
      toast(`Could not load problems: ${e.message}`, "bad");
      return;
    }
    const id = decodeURIComponent(location.hash.slice(1));
    if (id && state.problems.some((p) => p.id === id)) openProblem(id);
  }

  boot();
})();
