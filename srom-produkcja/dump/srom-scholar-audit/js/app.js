"use strict";

/* =====================================================================
   The shell: masthead, the four tools, language, settings, start-up.
   Loaded last, so everything it wires up already exists.
   ===================================================================== */

/* ---------- 15d. Settings --------------------------------------------- */

async function renderSettings(){
  const persisted = navigator.storage?.persisted ? await navigator.storage.persisted() : null;
  const est = navigator.storage?.estimate ? await navigator.storage.estimate() : null;
  const libKB = Math.round(JSON.stringify(libraryPayload()).length / 1024);
  const nS = Object.keys(LIB.scholars).length;
  const folderState = !BK.dir ? t("not chosen")
    : BK.perm === "granted" ? t("connected") : t("needs permission");

  const radio = (name, val, label, sub, disabled) => `
    <label class="opt ${disabled ? "dis" : ""}">
      <input type="radio" name="${name}" value="${val}" ${BK.settings[name] === val ? "checked" : ""} ${disabled ? "disabled" : ""}>
      <span><b>${esc(label)}</b>${sub ? `<small>${esc(sub)}</small>` : ""}</span>
    </label>`;
  const savedN = DC.index.filter(e => LIB.scholars[e.id]).length, otherN = DC.index.length - savedN;

  setView("settings", `
  <div class="card" id="settingsPanel">
    <header><h3>${esc(t("Settings"))}</h3><div class="sp"></div>
      <button class="icon-btn" id="setClose">${esc(t("Close"))}</button></header>
    <div class="body">

      <h4 class="set-h">${esc(t("Interface language"))}</h4>
      <div class="set-grid">
        <div class="set-lab">${esc(t("Language"))}</div>
        <div>
          ${[["en","English"],["pl","Polski"]].map(([v, l]) => `<label class="opt"><input type="radio" name="lang" value="${v}" ${I18N.lang === v ? "checked" : ""}>
            <span><b>${l}</b></span></label>`).join("")}
          <small class="muted set-small">${esc(t("Names of works, journals and institutions stay as the sources record them."))}</small>
        </div>
      </div>

      <h4 class="set-h">${esc(t("Automatic backup"))}</h4>
      <div class="note">${t("set.backup.note")}</div>

      <div class="set-grid">
        <div class="set-lab">${esc(t("Save to"))}</div>
        <div>
          ${radio("dest","folder",t("A folder you choose"),
             BK.canFolder
               ? (BK.dir ? `“${BK.dir.name}” — ${folderState}` : t("written silently; one current file plus a dated copy per day, 30 days kept"))
               : t("not available in this browser — Chrome or Edge on a computer can do this; Safari, Firefox and Android cannot"),
             !BK.canFolder)}
          ${BK.canFolder ? `<div class="set-sub-btns">
             <button class="icon-btn" id="setPick">${esc(BK.dir ? t("Change folder…") : t("Choose folder…"))}</button>
             ${BK.dir && BK.perm !== "granted" ? `<button class="icon-btn" id="setPerm">${esc(t("Allow access"))}</button>` : ""}
           </div>` : ""}
          ${radio("dest","download",t("Downloads folder"),
             t("a timestamped file is downloaded each time — the browser may ask once to allow multiple downloads"))}
        </div>

        <div class="set-lab">${esc(t("When"))}</div>
        <div>
          ${radio("when","change",t("After every change"), BK.settings.dest === "folder" ? t("within a couple of seconds") : t("grouped: one file per burst of edits, 30 s after the last one"))}
          ${radio("when","5",t("Every 5 minutes"),t("only if something changed"))}
          ${radio("when","15",t("Every 15 minutes"),t("only if something changed"))}
          ${radio("when","manual",t("Only when I press Back up now"),"")}
        </div>

        <div class="set-lab">${esc(t("Status"))}</div>
        <div class="set-status">
          ${esc(t("Last backup:"))} <b>${esc(fmtWhen(BK.lastAt))}</b>${BK.lastWhere ? " → " + esc(whereText(BK.lastWhere)) : ""}
          ${BK.dirty ? `<br><span class="warn-txt">${esc(t("Unsaved changes since then."))}</span>` : ""}
          ${BK.lastError ? `<br><span class="bad-txt">${esc(t("Last attempt failed: {msg}", { msg:BK.lastError }))}</span>` : ""}
          <div class="row-btns">
            <button class="btn small" id="setNow">${esc(t("Back up now"))}</button>
            <button class="icon-btn" id="setRestore">${esc(t("Restore…"))}</button>
          </div>
        </div>
      </div>

      <h4 class="set-h">${esc(t("Stored dossiers"))}</h4>
      <div class="set-grid">
        <div class="set-lab">${esc(t("Opening a scholar"))}</div>
        <div>
          ${[["cached", t("Open the stored copy, offer an update"), t("instant; a line on the dossier shows its age and an Update now button")],
             ["ask", t("Ask each time"), t("choose between the stored copy and fresh data whenever one exists")],
             ["fresh", t("Always fetch fresh data"), t("ignore stored copies — the slowest, always current")]]
            .map(([v, b, sm]) => `<label class="opt"><input type="radio" name="dcmode" value="${v}" ${DC.mode === v ? "checked" : ""}>
               <span><b>${esc(b)}</b><small>${esc(sm)}</small></span></label>`).join("")}
        </div>
        <div class="set-lab">${esc(t("Kept"))}</div>
        <div>${esc(t("set.kept", { dossiers:tn(DC.index.length, "dossier"), saved:tn(savedN, "saved scholar"), other:otherN, keep:DC.KEEP_OTHERS }))}
          <small class="muted set-small">${esc(t("set.kept.note", { n:DC.STALE_DAYS }))}</small>
          ${DC.index.length ? `<div class="row-btns"><button class="icon-btn" id="setDcClear">${esc(t("Clear stored dossiers"))}</button></div>` : ""}
        </div>
      </div>

      <h4 class="set-h">${esc(t("Storage in this browser"))}</h4>
      <div class="set-grid">
        <div class="set-lab">${esc(t("Library"))}</div>
        <div>${esc(tn(nS, "scholar"))} · ${esc(tn(LIB.folders.length, "folder"))} · ${libKB} KB</div>
        <div class="set-lab">${esc(t("Protection"))}</div>
        <div>${persisted === true
            ? t("set.persist.yes")
            : persisted === false
              ? `${esc(t("Not persistent — the browser may evict it under storage pressure."))} <button class="icon-btn" id="setPersist">${esc(t("Request persistence"))}</button>`
              : esc(t("This browser does not report persistence."))}
          ${est ? `<div class="muted set-small">${esc(t("Using {used} KB of {quota} MB available.", { used:num(Math.round((est.usage||0)/1024)), quota:num(Math.round((est.quota||0)/1048576)) }))}</div>` : ""}
        </div>
      </div>
    </div>
  </div>`);

  $("#setClose").onclick = () => showView(UI.prev || "check");
  $$('#settingsPanel input[name="lang"]').forEach(r => r.onchange = () => setLang(r.value));
  $$('#settingsPanel input[name="dest"]').forEach(r => r.onchange = async () => {
    if (r.value === "folder" && !BK.dir) return bkChooseFolder();
    BK.settings.dest = r.value; await bkSaveSettings(); renderSettings();
  });
  $$('#settingsPanel input[name="when"]').forEach(r => r.onchange = async () => {
    BK.settings.when = r.value; await bkSaveSettings(); renderSettings();
  });
  const pick = $("#setPick"); if (pick) pick.onclick = bkChooseFolder;
  const perm = $("#setPerm"); if (perm) perm.onclick = async () => {
    BK.perm = await BK.dir.requestPermission({ mode:"readwrite" });
    if (BK.perm === "granted" && BK.dirty) await runBackup({ manual:true });
    bkBanner(); renderSettings();
  };
  $("#setNow").onclick = () => runBackup({ manual:true });
  $("#setRestore").onclick = restoreFlow;
  const ps = $("#setPersist"); if (ps) ps.onclick = async () => {
    await navigator.storage.persist(); renderSettings();
  };
  $$('#settingsPanel input[name="dcmode"]').forEach(r => r.onchange = async () => {
    DC.mode = r.value; await DB.set("dossierMode", DC.mode);
  });
  const dcc = $("#setDcClear"); if (dcc) dcc.onclick = async () => {
    if (!await ask({ title:t("Clear stored dossiers?"), text:t("Your library, folders and notes stay. Each scholar is fetched again the next time you open them."), ok:t("Clear"), danger:true })) return;
    await dcClear(); toast(t("Stored dossiers cleared.")); renderSettings();
  };
}
VIEW_ENTER.settings = () => renderSettings();

/* ---------- Language -------------------------------------------------- */

/** Switch the interface language and redraw every tool from its state —
    nothing is fetched again. */
function setLang(l){
  if (l !== "pl" && l !== "en") return;
  I18N.lang = l;
  try { localStorage.setItem("srom.lang", l); } catch (e) {}
  applyStatic();
  redrawCheck();
  const drawn = v => $("#view-" + v)?.innerHTML.trim();
  const cmpHere = v => CMP.active && CMP.host === v;
  for (const v of ["library", "directory", "reviewers"]){
    if (cmpHere(v)){ if (CMP.ready) drawCompare(); continue; }
    if (!drawn(v)) continue;
    if (v === "library") renderLibrary();
    else if (v === "directory") renderDirectory();
    else renderReviewers();
  }
  if (UI.view === "settings") renderSettings();
  bkBanner();
  syncMastHeight();
}

/** The masthead, the search form and the footer are static HTML; their
    text comes from data-i18n attributes. */
function applyStatic(){
  document.documentElement.lang = I18N.lang;
  $$("[data-i18n]").forEach(el => { el.textContent = t(el.dataset.i18n); });
  $$("[data-i18n-html]").forEach(el => { el.innerHTML = t(el.dataset.i18nHtml); });
  $$("[data-i18n-ph]").forEach(el => { el.placeholder = t(el.dataset.i18nPh); });
  $$("[data-i18n-title]").forEach(el => { el.title = t(el.dataset.i18nTitle); });
  $$("[data-i18n-aria]").forEach(el => { el.setAttribute("aria-label", t(el.dataset.i18nAria)); });
  document.title = t("Scholar Audit · Studia Romologica");
  $$("#langSeg button").forEach(b => {
    const on = b.dataset.lang === I18N.lang;
    b.classList.toggle("on", on); b.setAttribute("aria-pressed", String(on));
  });
}

/* ---------- Masthead -------------------------------------------------- */

/* One multiplier drives every font size, so the whole interface scales
   together rather than drifting out of proportion. */
function setFs(v){
  const fs = Math.min(2.2, Math.max(0.8, Math.round(v * 100) / 100));
  document.documentElement.style.setProperty("--fs", fs);
  try { localStorage.setItem("srom.fs", fs); } catch (e) {}
  syncMastHeight();
  if (CMP.active) drawGraph();
}
const curFs = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--fs")) || 1;

/* The masthead height depends on the rendered font, so measure it and let
   sticky table headers dock exactly beneath it. */
function syncMastHeight(){
  const h = document.querySelector(".masthead")?.offsetHeight;
  if (h) document.documentElement.style.setProperty("--mast-h", h + "px");
}

async function venueDialog(){
  const mine = userVerdictCount();
  const k = await choose({ title:t("Venue verdicts"),
    text:t("Your ERIH PLUS, Scopus, Web of Science and MEiN verdicts — {venues} recorded. Record them on a dossier's Venues tab.", { venues:tn(mine, "venue") }),
    choices:[
      { value:"export", label:t("Download as JSON"), sub:t("to back up or share with a colleague") },
      { value:"import", label:t("Import from a file…"), sub:t("merges with what you have") },
      { value:"reset",  label:t("Reset to the SROM seed list"), sub:t("discards your own verdicts") },
    ] });
  if (k === "export") download("srom-venue-registry.json", JSON.stringify(S.registry, null, 2), "application/json");
  else if (k === "import"){
    const inc = await pickJSON();
    if (!inc) return;
    const reg = inc.venueRegistry || inc;           // a full library backup also works
    for (const [issn, v] of Object.entries(reg)) S.registry[issn] = { ...(S.registry[issn] || {}), ...v };
    saveRegistry();
    if (S.author && CHECK.stage === "dossier"){ S.works.forEach(scoreWork); renderShell(); }
    toast(t("Merged {venues}.", { venues:tn(Object.keys(reg).length, "venue") }));
  } else if (k === "reset"){
    if (!await ask({ title:t("Discard your venue verdicts?"), text:t("The registry returns to the SROM seed list."), ok:t("Reset"), danger:true })) return;
    try { localStorage.removeItem("srom.venueRegistry"); } catch (e) {}
    S.registry = loadRegistry();
    saveRegistry();
    if (S.author && CHECK.stage === "dossier"){ S.works.forEach(scoreWork); renderShell(); }
  }
}

function wireMasthead(){
  $$("#toolNav [data-view]").forEach(a => a.onclick = e => {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return;   // a new tab gets the address
    e.preventDefault();
    showView(a.dataset.view);
  });
  $(".brand").onclick = e => {
    if (e.metaKey || e.ctrlKey) return;
    e.preventDefault();
    showView("check");
    $("#q").focus();
  };
  $$("#langSeg button").forEach(b => b.onclick = () => setLang(b.dataset.lang));

  $("#btnFsUp").onclick   = () => setFs(curFs() + 0.1);
  $("#btnFsDown").onclick = () => setFs(curFs() - 0.1);
  $("#btnTheme").onclick = () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem("srom.theme", next); } catch(e){}
  };
  $("#btnSettings").onclick = () => showView("settings");
  $("#btnRegistry").onclick = venueDialog;

  /* The utilities collapse into a panel on narrow screens; it must close
     once something in it is used, or it covers the result. */
  const menu = $("#mastActions"), burger = $("#btnMenu");
  burger.onclick = () => {
    const open = menu.classList.toggle("open");
    burger.setAttribute("aria-expanded", String(open));
  };
  menu.addEventListener("click", e => {
    if (e.target.closest(".icon-btn") && getComputedStyle(burger).display !== "none"){
      menu.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
    }
  });
  document.addEventListener("click", e => {
    if (!e.target.closest(".masthead")){ menu.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); }
  });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && menu.classList.contains("open")){ menu.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); burger.focus(); }
  });

  $("#searchForm").addEventListener("submit", e => { e.preventDefault(); runSearch(); });
  $("#btnClear").onclick = () => {
    setAddress({}, "check");
    $("#q").value = ""; setErr("");
    renderCheckLanding();
    $("#q").focus();
  };
}

/* ---------- 18. Boot -------------------------------------------------- */

try {
  const savedFs = parseFloat(localStorage.getItem("srom.fs"));
  if (savedFs) document.documentElement.style.setProperty("--fs", savedFs);
  const theme = localStorage.getItem("srom.theme");
  if (theme) document.documentElement.dataset.theme = theme;
  else if (matchMedia("(prefers-color-scheme: dark)").matches) document.documentElement.dataset.theme = "dark";
} catch (e) {}

applyStatic();
wireMasthead();
syncMastHeight();
addEventListener("resize", syncMastHeight);
updateRegCount();

/* Installable app shell. Only possible from a secure origin, so this is a
   no-op while the file is opened directly from disk — the tool still works,
   it simply cannot be installed to a home screen until it is hosted. */
if ("serviceWorker" in navigator && location.protocol.startsWith("http")){
  addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js").catch(() => {});
  });
}

let deferredInstall = null;
addEventListener("beforeinstallprompt", e => {
  e.preventDefault();
  deferredInstall = e;
  if ($("#btnInstall")) return;
  const b = document.createElement("button");
  b.className = "icon-btn"; b.id = "btnInstall";
  b.dataset.i18n = "Install app";
  b.textContent = t("Install app");
  b.onclick = async () => {
    b.remove();
    deferredInstall.prompt();
    await deferredInstall.userChoice;
    deferredInstall = null;
  };
  $("#mastActions").prepend(b);
});

const libLoadDone = libLoad().then(dcLoad);
libLoadDone.then(bkLoad).then(() => {
  if (navigator.storage?.persist) navigator.storage.persist().catch(() => {});
});
// Last chance to flush a pending folder write before the page goes away.
addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden" && BK.dirty && BK.settings.dest === "folder"
      && BK.perm === "granted" && BK.settings.when !== "manual") runBackup({ manual:false });
});

/* Deep links. Every view has one:
     ?q=0000-0001-5333-2330                     a dossier
     ?tool=reviewers                            the reviewer finder (the manuscript is never in the address)
     ?tool=directory&theme=holocaust&country=PL the directory, filtered
     ?tool=library                              the library
     ?compare=A…,A…                             a relations map (with &tool= for the tool it belongs to) */
(function route(){
  const params = new URLSearchParams(location.search);
  const tool = params.get("tool");
  const compare = (params.get("compare") || "").split(",").map(x => x.trim()).filter(x => RX_OPENALEX.test(x)).slice(0, CMP_MAX);
  const q = params.get("q");

  if (tool === "directory"){
    const th = params.get("theme"), cc = (params.get("country") || "").toUpperCase(), yr = params.get("years"), so = params.get("sort");
    if (themeById(th)) DIR.f.theme = th;
    if (/^[A-Z]{2}$/.test(cc)) DIR.f.country = cc;
    if (DIR_YEARS.includes(yr)) DIR.f.years = yr;
    if (DIR_SORTS.some(([v]) => v === so)) DIR.f.sort = so;
  }

  renderCheckLanding();
  if (compare.length >= 2){
    const host = ["directory", "reviewers"].includes(tool) ? tool : "library";
    libLoadDone.then(() => renderCompare(compare.map(x => shortId(x.toUpperCase())), { host }));
  } else if (q){
    $("#q").value = q;
    libLoadDone.then(runSearch);
  } else if (["reviewers", "directory", "library"].includes(tool)){
    if (tool === "library") libLoadDone.then(() => showView("library"));
    else showView(tool);
  } else {
    showView("check");
    libLoadDone.then(() => { if (CHECK.stage === "landing" && UI.view === "check") renderCheckLanding(); });
    $("#q").focus();
  }
})();
