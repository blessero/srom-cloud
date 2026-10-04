"use strict";

/* =====================================================================
   Library — saved scholars in folders — and the relations map, which
   draws how any 2–12 scholars relate. The map can be opened from the
   Library, the Field directory or the Reviewer finder, and opens in the
   tool it was started from.
   ===================================================================== */

/* ---------- 15b. Library browser -------------------------------------- */

const LIBVIEW = { folder:"all", q:"", selected:new Set() };
const CMP_MAX = 12;

function renderLibrary(){
  if (CMP.host === "library") CMP.active = false;
  setAddress({}, "library");
  const all = Object.values(LIB.scholars)
    .sort((a,b) => String(b.savedAt).localeCompare(String(a.savedAt)));

  const counts = { all: all.length, none: all.filter(r => !(r.folders||[]).length).length };
  LIB.folders.forEach(f => counts[f.id] = all.filter(r => (r.folders||[]).includes(f.id)).length);
  if (LIBVIEW.folder !== "all" && LIBVIEW.folder !== "none" && !LIB.folders.some(f => f.id === LIBVIEW.folder)) LIBVIEW.folder = "all";

  const q = LIBVIEW.q.toLowerCase().trim();
  const list = all.filter(r => {
    if (LIBVIEW.folder === "none" && (r.folders||[]).length) return false;
    if (LIBVIEW.folder !== "all" && LIBVIEW.folder !== "none"
        && !(r.folders||[]).includes(LIBVIEW.folder)) return false;
    if (!q) return true;
    const themes = (r.coreIds || []).concat(r.secondaryIds || []).map(themeName);
    return [r.name, r.affiliation, r.headline, recordHeadline(r), (r.core||[]).join(" "),
            (r.secondary||[]).join(" "), themes.join(" "), r.note].join(" ").toLowerCase().includes(q);
  });

  const tab = (id, label, n) =>
    `<button class="fchip ${LIBVIEW.folder === id ? "on" : ""}" data-lf="${esc(id)}">${esc(label)}${n != null ? ` · ${n}` : ""}</button>`;

  setView("library", `
  <div class="card">
    <header><h3>${esc(t("Saved scholars"))}</h3><div class="sp"></div>
      <button class="icon-btn" id="btnLibNewFolder">${esc(t("New folder"))}</button>
      <button class="icon-btn" id="btnLibExport">${esc(t("Back up now"))}</button>
      <button class="icon-btn" id="btnLibImport">${esc(t("Restore"))}</button>
      <button class="icon-btn" id="btnLibSettings">${esc(t("Backup settings"))}</button>
    </header>
    <div class="body">
      <div class="folderbar">
        ${tab("all", t("All"), counts.all)}
        ${LIB.folders.map(f => tab(f.id, f.name, counts[f.id])).join("")}
        ${counts.none ? tab("none", t("Unfiled"), counts.none) : ""}
        <span class="ctl-sp"></span>
        <input type="text" id="libQ" class="libq" placeholder="${esc(t("Filter by name, theme, note…"))}" value="${esc(LIBVIEW.q)}">
      </div>
      ${LIBVIEW.folder !== "all" && LIBVIEW.folder !== "none" ? `<div class="savebar" style="margin-bottom:11px">
        <button class="icon-btn" id="btnRenameFolder">${esc(t("Rename folder"))}</button>
        <button class="icon-btn" id="btnDeleteFolder">${esc(t("Delete folder"))}</button>
      </div>` : ""}
      ${list.length ? `<div class="libgrid">${list.map(libCard).join("")}</div>
        <div class="cmpbar" id="cmpBar"></div>`
        : `<div class="empty">${all.length
             ? esc(t("No saved scholar matches this filter."))
             : `${t("lib.empty")}
                <div style="margin-top:11px">${esc(t("Had a library before? Browser data may have been cleared —"))}
                <button class="icon-btn" id="libRecover">${esc(t("restore from a backup"))}</button></div>`}</div>`}
    </div>
  </div>`);

  const V = "#view-library";
  $$(`${V} .fchip[data-lf]`).forEach(b => b.onclick = () => {
    LIBVIEW.folder = b.dataset.lf; renderLibrary();
  });
  const qi = $("#libQ");
  if (qi){
    let tm;
    qi.addEventListener("input", e => {
      clearTimeout(tm);
      const v = e.target.value;
      tm = setTimeout(() => {
        LIBVIEW.q = v; renderLibrary();
        const el = $("#libQ");
        if (el){ el.focus(); el.setSelectionRange(el.value.length, el.value.length); }
      }, 220);
    });
  }
  $$(`${V} [data-pick]`).forEach(cb => {
    cb.onclick = e => e.stopPropagation();
    cb.onchange = () => {
      cb.checked ? LIBVIEW.selected.add(cb.dataset.pick) : LIBVIEW.selected.delete(cb.dataset.pick);
      cb.closest(".libcard").classList.toggle("picked", cb.checked);
      renderCmpBar(list);
    };
  });
  renderCmpBar(list);

  $$(`${V} .libcard`).forEach(c => {
    c.onclick = e => {
      if (e.target.closest("[data-unsave]") || e.target.closest(".pick")) return;
      openScholar(c.dataset.id);
    };
    c.onkeydown = e => { if (e.key === "Enter" && e.target === c) openScholar(c.dataset.id); };
  });
  $$(`${V} [data-unsave]`).forEach(b => b.onclick = async e => {
    e.stopPropagation();
    delete LIB.scholars[b.dataset.unsave];
    await libSave(); renderLibrary();
  });

  const rec = $("#libRecover"); if (rec) rec.onclick = () => BK.canFolder && !BK.dir ? bkChooseFolder() : restoreFlow();
  $("#btnLibNewFolder").onclick = async () => {
    if (!await newFolder()) return;
    await libSave(); renderLibrary();
  };
  const rn = $("#btnRenameFolder");
  if (rn) rn.onclick = async () => {
    const f = LIB.folders.find(f => f.id === LIBVIEW.folder);
    if (!f) return;
    const name = await ask({ title:t("Rename folder"), input:{ value:f.name }, ok:t("Rename") });
    if (!name) return;
    f.name = name; await libSave(); renderLibrary();
  };
  const del = $("#btnDeleteFolder");
  if (del) del.onclick = async () => {
    const f = LIB.folders.find(f => f.id === LIBVIEW.folder);
    if (!f) return;
    if (!await ask({ title:t("Delete the folder “{name}”?", { name:f.name }),
                     text:t("The scholars in it stay in your library — only the folder goes."),
                     ok:t("Delete folder"), danger:true })) return;
    LIB.folders = LIB.folders.filter(x => x.id !== f.id);
    Object.values(LIB.scholars).forEach(r => {
      r.folders = (r.folders || []).filter(id => id !== f.id);
    });
    LIBVIEW.folder = "all";
    await libSave(); renderLibrary();
  };
  $("#btnLibExport").onclick = () => runBackup({ manual:true }).then(renderLibrary);
  $("#btnLibSettings").onclick = () => showView("settings");
  $("#btnLibImport").onclick = () => restoreFlow();
}

function renderCmpBar(list){
  const bar = $("#cmpBar");
  if (!bar) return;
  // Selections can outlive a scholar being removed from the library.
  for (const id of [...LIBVIEW.selected]) if (!LIB.scholars[id]) LIBVIEW.selected.delete(id);
  const n = LIBVIEW.selected.size;
  const inFolder = LIBVIEW.folder !== "all" && LIBVIEW.folder !== "none" ? list.length : 0;
  bar.innerHTML = `
    <span>${n ? esc(t("{n} selected", { n })) : esc(t("Tick two or more scholars to map how they relate"))}</span>
    <span class="ctl-sp"></span>
    ${n ? `<button class="icon-btn" id="cmpClear">${esc(t("Clear"))}</button>` : ""}
    ${inFolder >= 2 ? `<button class="icon-btn" id="cmpFolder">${esc(t("Map this folder ({n})", { n:Math.min(inFolder, CMP_MAX) }))}</button>` : ""}
    <button class="btn small" id="cmpGo" ${n < 2 ? "disabled" : ""}>${esc(t("Map relations"))}</button>`;
  bar.classList.toggle("active", n >= 2);
  $("#cmpGo").onclick = () => {
    if (n > CMP_MAX) return toast(t("Up to {n} at a time — beyond that the map stops being readable.", { n:CMP_MAX }), { bad:true });
    renderCompare([...LIBVIEW.selected], { host:"library" });
  };
  const cl = $("#cmpClear");
  if (cl) cl.onclick = () => { LIBVIEW.selected.clear(); renderLibrary(); };
  const cf = $("#cmpFolder");
  if (cf) cf.onclick = () => renderCompare(list.slice(0, CMP_MAX).map(r => r.id), { host:"library" });
}

function libCard(r){
  const fnames = (r.folders || [])
    .map(id => LIB.folders.find(f => f.id === id)?.name).filter(Boolean);
  const picked = LIBVIEW.selected.has(r.id);
  const head = recordHeadline(r);
  const entry = dcEntry(r.id);
  return `<div class="libcard ${picked ? "picked" : ""}" data-id="${esc(r.id)}" data-orcid="${esc(r.orcid || "")}" tabindex="0">
    <label class="pick" title="${esc(t("Select to compare"))}"><input type="checkbox" data-pick="${esc(r.id)}" ${picked ? "checked" : ""}></label>
    <h4>${esc(r.name)}</h4>
    <div class="sub">${esc(r.affiliation || t("No affiliation recorded"))}${r.country ? " · " + esc(countryName(r.country)) : ""}
      ${r.orcidInferred ? ` · <span class="warn-txt">${esc(t("name-matched ID"))}</span>` : ""}</div>
    ${head ? `<div class="head">${esc(head)}</div>`
      : r.light ? `<div class="head muted">${esc(t("Not evaluated yet — open to build the dossier."))}</div>` : ""}
    <div class="nums">
      ${r.works != null ? `<span><b>${num(r.works)}</b> ${esc(tw(r.works, "work"))}</span>` : ""}
      ${r.cites != null ? `<span><b>${num(r.cites)}</b> ${esc(tw(r.cites, "citation"))}</span>` : ""}
      ${r.hIndex != null ? `<span>h <b>${r.hIndex}</b></span>` : ""}
      ${r.relevantPct != null ? `<span><b>${r.relevantPct}%</b> ${esc(t("in field"))}</span>` : ""}
      ${r.lastYear ? `<span>→ <b>${r.lastYear}</b></span>` : ""}
    </div>
    ${r.note ? `<div class="head note-x">${esc(r.note.slice(0,150))}${r.note.length>150?"…":""}</div>` : ""}
    <div class="fl">
      ${fnames.map(n => `<span class="b manual">${esc(n)}</span>`).join("")}
      ${entry ? `<span class="b idx" title="${esc(t("Opens instantly from a copy stored {age}", { age:ageText(entry.at) }))}">${esc(t("stored"))}</span>` : ""}
      <span class="ctl-sp"></span>
      <button class="togg" data-unsave="${esc(r.id)}" title="${esc(t("Remove from library"))}">${esc(t("remove"))}</button>
    </div>
  </div>`;
}

/** Restore merges rather than replaces, so a backup from one device can be
    folded into another without losing what is already there. */
async function mergeLibrary(d){
  let added = 0, merged = 0;
  for (const f of (d.folders || []))
    if (!LIB.folders.some(x => x.id === f.id || x.name === f.name)) LIB.folders.push(f);
  for (const [id, rec] of Object.entries(d.scholars || {})){
    if (LIB.scholars[id]){
      const cur = LIB.scholars[id];
      cur.folders = [...new Set([...(cur.folders||[]), ...(rec.folders||[])])];
      if (!cur.note && rec.note) cur.note = rec.note;
      merged++;
    } else { LIB.scholars[id] = rec; added++; }
  }
  if (d.venueRegistry){ S.registry = { ...S.registry, ...d.venueRegistry }; saveRegistry(); }
  if (d.pins){ S.pins = { ...S.pins, ...d.pins }; savePins(); }
  await libSave();
  return { added, merged };
}

async function importLibrary(){
  const d = await pickJSON();
  if (!d) return;
  if (!d.scholars && !d.folders) return toast(t("That file is not a Scholar Audit library backup."), { bad:true });
  const { added, merged } = await mergeLibrary(d);
  toast(t("Restored {added}; {merged} merged with what was already here.", { added:tn(added, "scholar"), merged }));
  if (UI.view === "settings") renderSettings(); else renderLibrary();
}

async function restoreFlow(){
  const d = BK.dir ? await readFolderBackup() : null;
  const n = d ? Object.keys(d.scholars || {}).length : 0;
  const pick = await choose({ title:t("Restore a library"), text:t("Restoring merges into what is here — nothing is overwritten."),
    choices:[
      ...(d ? [{ value:"folder", label:t("From the backup folder “{name}”", { name:BK.dir.name }),
                 sub:t("{scholars}, saved {when}", { scholars:tn(n, "scholar"), when:fmtWhen(d.exported) }) }] : []),
      { value:"file", label:t("From a backup file…"), sub:t("a srom-library-….json you downloaded or copied across") },
    ] });
  if (pick === "folder"){
    const { added, merged } = await mergeLibrary(d);
    toast(t("Restored {added}; {merged} merged.", { added:tn(added, "scholar"), merged }));
    renderLibrary();
  } else if (pick === "file") importLibrary();
}

VIEW_ENTER.library = () => {
  if (CMP.active && CMP.host === "library") drawGraph();
  else renderLibrary();
};

/* ---------- 15c. Relations between scholars ---------------------------- */
/* Four kinds of tie, each measured separately because they mean different
   things and fail differently:

     citation      A's works cite B's. Works the two co-authored are excluded
                   on both ends, so a partnership citing its own output does
                   not read as influence.
     co-authorship works both are authors of.
     shared refs   works both cite (bibliographic coupling), co-authored
                   papers excluded — a shared intellectual base even where
                   they never cite each other.
     themes        cosine similarity of their Romani-studies theme profiles.

   Only about a quarter of humanities works carry reference lists in
   OpenAlex, so the first and third are minimums. The fourth does not depend
   on reference lists at all, which is why it is on equal footing. */

const CMP = { ids:[], data:new Map(), layer:"cites", focus:null, pair:null, pairs:[],
              host:null, active:false, ready:false, names:{} };

/** Back to what the map was opened from. */
const CMP_BACK = { library:"← Library", directory:"← Directory", reviewers:"← Reviewers" };
function cmpLeave(host){
  CMP.active = false;
  if (host === "library") renderLibrary();
  else if (host === "directory") renderDirectory();
  else if (host === "reviewers") renderReviewers();
}

const shortName = n => {
  const p = String(n || "").trim().split(/\s+/);
  return p.length > 1 ? p[0][0] + ". " + p.slice(1).join(" ") : (p[0] || "?");
};
const cmpName = id => LIB.scholars[id]?.name || CMP.names[id] || id;

async function loadCompareScholar(id, onStep, { fresh = false } = {}){
  if (!fresh && CMP.data.has(id)) return CMP.data.get(id);
  // A stored dossier already holds the works, merged identity and reference
  // lists — the map needs nothing more from the network.
  if (!fresh){
    const entry = dcEntry(id);
    const snap = entry && await dcGet(entry.id);
    if (snap?.hasRefs) return compareRecord(id,
      LIB.scholars[id] || { id, name:snap.author.display_name, orcid:orcidOf(snap.author.orcid) || null },
      snap.works.filter(w => !w.paratext), snap.at);
  }
  let rec = LIB.scholars[id];
  // A shared ?compare= link, the directory or the reviewer finder can name
  // scholars this browser never saved.
  if (!rec){
    const a = await getJSON(oa("/authors/" + id));
    rec = { id, name:a.display_name, orcid:orcidOf(a.orcid) || null };
  }
  // Same merged identity as the dossier; older library records predate
  // `siblings`, so look them up through the ORCID.
  let ids = [id, ...(rec.siblings || [])];
  if (!rec.siblings && rec.orcid && !rec.orcidInferred)
    ids = [...new Set([id, ...(await orcidProfiles(rec.orcid)).map(p => shortId(p.id))])];
  const works = (await fetchAllWorks(ids.join("|"), onStep, ["referenced_works"])).filter(w => !w.paratext);
  return compareRecord(id, rec, works, null);
}

function compareRecord(id, rec, works, storedAt){
  works.forEach(relevanceOf);
  const d = {
    id, rec, name: rec.name || id, works, storedAt,
    idset: new Set(works.map(w => w.id)),
    byId: new Map(works.map(w => [w.id, w])),
    x: computeExpertise(works),
    refCoverage: works.length ? Math.round(100 * works.filter(w => w.refs.length).length / works.length) : 0,
    inField: works.filter(w => w.relevant).length,
  };
  CMP.data.set(id, d);
  return d;
}

function citesBetween(a, b){
  const target = new Set([...b.idset].filter(id => !a.idset.has(id)));
  const citing = [];
  let links = 0;
  for (const w of a.works){
    if (b.idset.has(w.id)) continue;
    const hits = w.refs.filter(r => target.has(r));
    if (hits.length){ citing.push({ w, cited: hits.map(h => b.byId.get(h)).filter(Boolean) }); links += hits.length; }
  }
  return { citing, links };
}

function themeVector(d){
  const v = {};
  if (d.x.total) for (const r of d.x.all) v[r.id] = r.n / d.x.total;
  return v;
}
function cosine(u, v){
  let dot = 0, nu = 0, nv = 0;
  for (const k of new Set([...Object.keys(u), ...Object.keys(v)])){
    const a = u[k] || 0, b = v[k] || 0;
    dot += a*b; nu += a*a; nv += b*b;
  }
  return nu && nv ? dot / Math.sqrt(nu*nv) : 0;
}

function computePair(a, b){
  const co = a.works.filter(w => b.idset.has(w.id));
  const ab = citesBetween(a, b), ba = citesBetween(b, a);

  const refsOf = (x, y) => new Set(x.works.filter(w => !y.idset.has(w.id)).flatMap(w => w.refs));
  const ra = refsOf(a, b), rb = refsOf(b, a);
  const sharedRefs = [...ra].filter(r => rb.has(r));
  const salton = ra.size && rb.size ? sharedRefs.length / Math.sqrt(ra.size * rb.size) : 0;

  const sim = cosine(themeVector(a), themeVector(b));
  const strong = d => new Set(d.x.all.filter(r => r.tier !== "peripheral").map(r => r.id));
  const sa = strong(a), sb = strong(b);
  const sharedThemes = [...sa].filter(id => sb.has(id));

  const venuesOf = d => {
    const m = new Map();
    d.works.forEach(w => { if (w.venue && w.venue !== NO_VENUE) m.set(w.venue, (m.get(w.venue) || 0) + 1); });
    return m;
  };
  const va = venuesOf(a), vb = venuesOf(b);
  const venues = [...va.keys()].filter(v => vb.has(v))
    .map(v => ({ name:v, a:va.get(v), b:vb.get(v) }))
    .sort((x, y) => (y.a + y.b) - (x.a + x.b));

  return {
    key: a.id + "|" + b.id, a, b, co, ab, ba,
    shared: sharedRefs, salton, sim, sharedThemes, venues,
    lowSample: a.x.thin || b.x.thin,
  };
}

function computeAllPairs(ids){
  const ds = ids.map(id => CMP.data.get(id)).filter(Boolean);
  const pairs = [];
  for (let i = 0; i < ds.length; i++)
    for (let j = i + 1; j < ds.length; j++) pairs.push(computePair(ds[i], ds[j]));

  // One combined strength drives the layout, so nodes stay put when you
  // switch layers and only the drawn ties change.
  const mx = f => Math.max(1e-9, ...pairs.map(f));
  const mCo = mx(p => p.co.length), mCi = mx(p => p.ab.citing.length + p.ba.citing.length), mRf = mx(p => p.salton);
  // Co-authorship weighs double: it is the closest tie two scholars can have,
  // and because co-authored works are excluded from the citation and
  // shared-reference counts, a pure partnership would otherwise score zero
  // on both and rank below two people who merely cite each other.
  pairs.forEach(p => {
    p.strength = 2.0 * p.co.length / mCo
               + 1.0 * (p.ab.citing.length + p.ba.citing.length) / mCi
               + 0.8 * p.sim
               + 0.6 * p.salton / mRf;
  });
  return pairs;
}

/** Small force-directed layout. Deterministic — the same selection always
    draws the same map — and cheap at the dozen nodes this is capped to. */
function layoutNodes(ds, pairs, W, H, mSide = W < 600 ? 54 : 104){
  const n = ds.length, cx = W/2, cy = H/2;
  if (n === 2) return new Map([[ds[0].id, { x:W*0.28, y:cy }], [ds[1].id, { x:W*0.72, y:cy }]]);
  const P = ds.map((d, i) => ({ id:d.id,
    x: cx + Math.cos(-Math.PI/2 + i*2*Math.PI/n) * Math.min(W,H)*0.34,
    y: cy + Math.sin(-Math.PI/2 + i*2*Math.PI/n) * Math.min(W,H)*0.34 }));
  const idx = new Map(P.map((p, i) => [p.id, i]));
  const k = Math.sqrt(W*H/n) * 0.55;
  // Relative, not capped: a cap flattened the strongest ties into equals, so a
  // 94-work partnership sat no closer than two scholars who cite each other.
  const maxS = Math.max(1e-9, ...pairs.map(p => p.strength));
  const iters = 450;
  for (let it = 0; it < iters; it++){
    const disp = P.map(() => ({ x:0, y:0 }));
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++){
      let dx = P[i].x - P[j].x, dy = P[i].y - P[j].y;
      const dist = Math.max(1, Math.hypot(dx, dy)), f = k*k/dist;
      dx /= dist; dy /= dist;
      disp[i].x += dx*f; disp[i].y += dy*f; disp[j].x -= dx*f; disp[j].y -= dy*f;
    }
    for (const p of pairs){
      if (p.strength <= 0) continue;
      const i = idx.get(p.a.id), j = idx.get(p.b.id);
      let dx = P[i].x - P[j].x, dy = P[i].y - P[j].y;
      const dist = Math.max(1, Math.hypot(dx, dy)), f = dist*dist/k * (p.strength / maxS) * 1.3;
      dx /= dist; dy /= dist;
      disp[i].x -= dx*f; disp[i].y -= dy*f; disp[j].x += dx*f; disp[j].y += dy*f;
    }
    const tt = Math.min(W,H) * 0.08 * (1 - it/iters) + 0.5;
    P.forEach((p, i) => {
      disp[i].x += (cx - p.x) * 0.03; disp[i].y += (cy - p.y) * 0.03;
      const m = Math.max(1e-9, Math.hypot(disp[i].x, disp[i].y));
      p.x += disp[i].x/m * Math.min(m, tt); p.y += disp[i].y/m * Math.min(m, tt);
    });
  }
  // Fit into the frame, leaving room for labels under each node.
  const xs = P.map(p => p.x), ys = P.map(p => p.y);
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const mX = mSide, mT = 58, mB = 58;
  const sx = (W - 2*mX) / Math.max(1, x1 - x0), sy = (H - mT - mB) / Math.max(1, y1 - y0);
  const sc = Math.min(sx, sy);
  const ox = (W - (x1 - x0)*sc)/2, oy = mT + (H - mT - mB - (y1 - y0)*sc)/2;
  return new Map(P.map(p => [p.id, { x: ox + (p.x - x0)*sc, y: oy + (p.y - y0)*sc }]));
}

const LAYERS = {
  cites:  { label:"Citations",         color:"--tB" },
  co:     { label:"Co-authorship",     color:"--tA" },
  refs:   { label:"Shared references", color:"--tC" },
  themes: { label:"Thematic overlap",  color:"--tD" },
};
const layerLabel = k => t(LAYERS[k].label);
const layerNote  = k => t("layer." + k);

function layerEdges(layer){
  const E = [];
  for (const p of CMP.pairs){
    if (layer === "cites"){
      if (p.ab.citing.length) E.push({ p, from:p.a.id, to:p.b.id, v:p.ab.citing.length, label:String(p.ab.citing.length), dir:true });
      if (p.ba.citing.length) E.push({ p, from:p.b.id, to:p.a.id, v:p.ba.citing.length, label:String(p.ba.citing.length), dir:true });
    } else if (layer === "co"){
      if (p.co.length) E.push({ p, from:p.a.id, to:p.b.id, v:p.co.length, label:String(p.co.length) });
    } else if (layer === "refs"){
      if (p.shared.length) E.push({ p, from:p.a.id, to:p.b.id, v:p.shared.length, label:String(p.shared.length) });
    } else if (p.sim >= 0.15){
      E.push({ p, from:p.a.id, to:p.b.id, v:p.sim, label:Math.round(p.sim*100) + "%" });
    }
  }
  return E;
}

async function renderCompare(ids, { fresh = false, host = "library", names = {} } = {}){
  // One map at a time: its element ids are unique on the page.
  if (CMP.active && CMP.host && CMP.host !== host) cmpLeave(CMP.host);
  CMP.host = host; CMP.active = true; CMP.ready = false; CMP.names = { ...CMP.names, ...names };
  CMP.ids = ids; CMP.focus = null; CMP.pair = null;
  if (fresh){ ids.forEach(id => CMP.data.delete(id)); cache.clear(); }
  showView(host);
  setView(host, `<div id="cmpRoot"><div class="card"><header><h3>${esc(t("Mapping {scholars}", { scholars:tn(ids.length, "scholar") }))}</h3></header>
    <div class="body"><div class="note">${esc(t("cmp.loading"))}</div>
    <ul class="dd-list" id="cmpProg">${ids.map(id => `<li data-p="${esc(id)}">
      <span class="spinner"></span> ${esc(cmpName(id))} <span class="yr" data-s></span></li>`).join("")}</ul></div></div></div>`);
  scrollTo(0, 0);

  const ok = [];
  await Promise.all(ids.map(async id => {
    const li = $(`#cmpProg [data-p="${CSS.escape(id)}"]`);
    try {
      const d = await loadCompareScholar(id, msg => { const s = li?.querySelector("[data-s]"); if (s) s.textContent = msg; }, { fresh });
      ok.push(id);
      if (li) li.innerHTML = `✓ ${esc(d.name)} <span class="yr">${esc(tn(d.works.length, "work"))} · ${esc(t("{pct}% with reference lists", { pct:d.refCoverage }))}${
        d.storedAt ? " · " + esc(t("stored copy")) : ""}</span>`;
    } catch (e){
      if (li) li.innerHTML = `<span class="bad-txt">✕ ${esc(cmpName(id))} — ${esc(e.message)}</span>`;
    }
  }));
  if (!CMP.active || CMP.host !== host) return;   // left while it loaded

  CMP.ids = ids.filter(id => ok.includes(id));   // keep the order you chose
  if (CMP.ids.length < 2){
    $("#cmpProg").insertAdjacentHTML("afterend",
      `<div class="err" style="margin-top:10px">${esc(t("Fewer than two records could be loaded, so there is nothing to map. Try again in a moment."))}</div>
       <button class="icon-btn" id="cmpBack">${esc(t(CMP_BACK[host]))}</button>`);
    $("#cmpBack").onclick = () => cmpLeave(host);
    return;
  }
  CMP.pairs = computeAllPairs(CMP.ids);
  CMP.ready = true;
  setAddress({ compare: CMP.ids.join(",") }, host);
  drawCompare();
}

function drawCompare(){
  const ds = CMP.ids.map(id => CMP.data.get(id));
  const cov = ds.map(d => d.refCoverage);
  const counts = Object.fromEntries(Object.keys(LAYERS).map(k => [k, layerEdges(k).length]));
  const stored = ds.filter(d => d.storedAt);

  // Two columns on a wide screen: the map with the pair table under it on the
  // left; whatever you tap, then the theme profiles, on the right — so a
  // selection's detail appears beside the map rather than a scroll away.
  setView(CMP.host, `<div id="cmpRoot">
  <div class="card cmp-head">
    <header><h3>${esc(t("Relations between {scholars}", { scholars:tn(ds.length, "scholar") }))}</h3><div class="sp"></div>
      <button class="icon-btn" id="cmpBack">${esc(t(CMP_BACK[CMP.host]))}</button>
      <button class="icon-btn" id="cmpShare">${esc(t("Share link"))}</button>
      <button class="icon-btn" id="cmpExport">${esc(t("Export…"))}</button>
    </header>
    <div class="cmp-sub">
      <span>${t("cmp.cov", { min:Math.min(...cov), max:Math.max(...cov) })}</span>
      ${stored.length ? `<span class="muted">${esc(stored.length === ds.length ? t("All from stored copies") : t("{n} of {total} from stored copies", { n:stored.length, total:ds.length }))}
        · <button class="linkish" id="cmpRefresh">${esc(t("refresh"))}</button></span>` : ""}
    </div>
  </div>
  <div class="cmp-layout">
    <div class="cmp-col">
      <div class="card cmp-map">
        <header><div class="seg" id="cmpLayers">${Object.keys(LAYERS).map(k =>
          `<button data-layer="${k}" class="${CMP.layer === k ? "on" : ""}">${esc(layerLabel(k))} <span class="n">${counts[k]}</span></button>`).join("")}</div></header>
        <div class="cmp-graph" id="cmpGraph"></div>
        <div class="cmp-legend" id="cmpLegend"></div>
      </div>
      <div class="card cmp-pairs"><header><h3>${esc(t("Every pair"))}</h3><div class="sp"></div>
        <span class="hdr-note">${esc(t("strongest first · tap a row"))}</span></header>
        <div class="scrollx flush">${pairTable()}</div></div>
    </div>
    <div class="cmp-col">
      <div id="cmpDetail" class="cmp-detail"></div>
      <div class="card cmp-themes"><header><h3>${esc(t("Theme profiles"))}</h3><div class="sp"></div>
        <span class="hdr-note">${esc(t("share of in-field works · outlined = core"))}</span></header>
        <div class="scrollx flush">${themeGrid(ds)}</div></div>
    </div>
  </div></div>`);

  $("#cmpBack").onclick = () => cmpLeave(CMP.host);
  $("#cmpShare").onclick = () => shareLink(t("Relations between {scholars}", { scholars:tn(ds.length, "scholar") }) + " — Scholar Audit");
  $("#cmpExport").onclick = async () => {
    const k = await choose({ title:t("Export this map"), choices:[
      { value:"svg",  label:t("Map (SVG)"), sub:t("the {layer} layer as drawn — opens in any browser or Illustrator", { layer:layerLabel(CMP.layer).toLowerCase() }) },
      { value:"csv",  label:t("Pair table (CSV)"), sub:t("every pair and every measure — opens in Excel") },
      { value:"json", label:t("Everything (JSON)"), sub:t("including the works behind each tie") },
    ] });
    if (k === "svg") exportCompareSVG(); else if (k === "csv") exportCompareCSV(); else if (k === "json") exportCompareJSON();
  };
  const rf = $("#cmpRefresh");
  if (rf) rf.onclick = () => renderCompare(CMP.ids, { fresh:true, host:CMP.host });
  $$("#cmpLayers button").forEach(b => b.onclick = () => {
    CMP.layer = b.dataset.layer;
    $$("#cmpLayers button").forEach(x => x.classList.toggle("on", x === b));
    drawGraph();
  });
  $$("#cmpRoot tr[data-pair]").forEach(tr => tr.onclick = () => selectPair(tr.dataset.pair, true));
  drawGraph();
  if (CMP.pair) renderPairDetail(); else if (CMP.focus) renderNodeDetail();
}

function drawGraph(){
  const box = $("#cmpGraph");
  if (!box || !box.clientWidth) return;     // not drawn, or its tool is hidden
  const W = Math.round(Math.max(320, Math.min(1100, box.clientWidth || 800)));
  const n = CMP.ids.length;
  // Height follows the number of scholars, not the width of the screen: two
  // or three need little room, a dozen need more — never the whole viewport.
  const H = W < 600 ? Math.round(W * (n <= 3 ? 0.8 : 1.0))
                    : Math.round(Math.min(560, W * (n <= 3 ? 0.44 : n <= 6 ? 0.54 : 0.64)));
  const fs = curFs();
  const ds = CMP.ids.map(id => CMP.data.get(id));
  // Names and themes sit beside the outermost nodes on a wide map, so the
  // side margin must hold the longest label, or it is cut at the edge.
  const nodeTheme = d => { const top = d.x.core[0] || d.x.secondary[0];
    return d.x.thin ? t("thin record") : top ? themeName(top.id) : t("no dominant theme"); };
  const labelW = Math.max(...ds.map(d => Math.max(shortName(d.name).length * 7.2, nodeTheme(d).length * 5.9))) * fs;
  const pos = layoutNodes(ds, CMP.pairs, W, H, W < 600 ? Math.min(W * 0.3, Math.max(54, labelW / 2 + 10))
                                                  : Math.min(W * 0.26, Math.max(104, labelW + 30)));
  const maxIn = Math.max(1, ...ds.map(d => d.inField));
  const rad = d => (6 + 12 * Math.sqrt(d.inField / maxIn)) * (W < 600 ? 0.85 : 1);
  const R = new Map(ds.map(d => [d.id, rad(d)]));
  const L = LAYERS[CMP.layer];
  const LL = layerLabel(CMP.layer);
  const edges = layerEdges(CMP.layer);
  const maxV = Math.max(1e-9, ...edges.map(e => e.v));

  const F = CMP.focus;
  const nbr = new Set(F ? edges.filter(e => e.from === F || e.to === F).flatMap(e => [e.from, e.to]) : []);
  const edgeOn = e => (!F || e.from === F || e.to === F) && (!CMP.pair || e.p.key === CMP.pair);
  const nodeOn = d => (!F || d.id === F || nbr.has(d.id)) &&
                      (!CMP.pair || CMP.pair.split("|").includes(d.id));

  const unit = (x, y) => { const m = Math.hypot(x, y) || 1; return [x/m, y/m]; };
  const edgeSvg = edges.map(e => {
    const A = pos.get(e.from), B = pos.get(e.to), rA = R.get(e.from), rB = R.get(e.to);
    const w = 0.9 + 3.4 * (e.v / maxV);
    let d, lx, ly;
    if (e.dir){
      const dx = B.x - A.x, dy = B.y - A.y, len = Math.hypot(dx, dy) || 1;
      const C = { x:(A.x + B.x)/2 - dy/len * len*0.17, y:(A.y + B.y)/2 + dx/len * len*0.17 };
      const [ux, uy] = unit(C.x - A.x, C.y - A.y), [vx, vy] = unit(C.x - B.x, C.y - B.y);
      const S0 = { x:A.x + ux*(rA + 3), y:A.y + uy*(rA + 3) };
      const E0 = { x:B.x + vx*(rB + 9), y:B.y + vy*(rB + 9) };
      d = `M${S0.x.toFixed(1)} ${S0.y.toFixed(1)} Q${C.x.toFixed(1)} ${C.y.toFixed(1)} ${E0.x.toFixed(1)} ${E0.y.toFixed(1)}`;
      lx = 0.25*S0.x + 0.5*C.x + 0.25*E0.x; ly = 0.25*S0.y + 0.5*C.y + 0.25*E0.y;
    } else {
      const [ux, uy] = unit(B.x - A.x, B.y - A.y);
      const S0 = { x:A.x + ux*(rA + 2), y:A.y + uy*(rA + 2) }, E0 = { x:B.x - ux*(rB + 2), y:B.y - uy*(rB + 2) };
      d = `M${S0.x.toFixed(1)} ${S0.y.toFixed(1)} L${E0.x.toFixed(1)} ${E0.y.toFixed(1)}`;
      lx = (S0.x + E0.x)/2; ly = (S0.y + E0.y)/2;
    }
    const nm = id => CMP.data.get(id).name;
    const tip = e.dir ? t("{a} cites {b} in {works}", { a:nm(e.from), b:nm(e.to), works:tn(e.v, "work.loc") })
                      : `${nm(e.from)} — ${nm(e.to)}: ${e.label} (${LL.toLowerCase()})`;
    return `<g class="edge ${edgeOn(e) ? "" : "dim"}" data-pair="${esc(e.p.key)}" tabindex="0" role="button" aria-label="${esc(tip)}">
      <title>${esc(tip)}</title>
      <path d="${d}" fill="none" stroke="transparent" stroke-width="16"/>
      <path d="${d}" fill="none" style="stroke:var(${L.color})" stroke-opacity=".82" stroke-width="${w.toFixed(2)}"
        stroke-linecap="round" ${CMP.layer === "themes" ? 'stroke-dasharray="7 5"' : ""}
        ${e.dir ? 'marker-end="url(#arr)"' : ""}/>
      <text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" text-anchor="middle" dominant-baseline="central"
        style="font:600 ${(10.5*fs).toFixed(1)}px var(--mono);fill:var(${L.color});stroke:var(--card);stroke-width:3.5px;paint-order:stroke">${esc(e.label)}</text>
    </g>`;
  }).join("");

  const all = [...pos.values()];
  const gx = all.reduce((a, p) => a + p.x, 0) / all.length, gy = all.reduce((a, p) => a + p.y, 0) / all.length;
  // Put each name on the side facing away from the centre, where the lines
  // are not — a label under every node gets crossed by any edge running down.
  const labelAt = (P, r) => {
    const dx = P.x - gx, dy = P.y - gy, side = W >= 600 && Math.abs(dx) > Math.abs(dy) * 1.25;
    if (side){
      const s = dx >= 0 ? 1 : -1;
      return { x:P.x + s*(r + 7), y1:P.y - 1*fs, y2:P.y + 11*fs, anchor: s > 0 ? "start" : "end" };
    }
    return dy < 0 && ds.length > 2
      ? { x:P.x, y1:P.y - r - 19*fs, y2:P.y - r - 7*fs, anchor:"middle" }
      : { x:P.x, y1:P.y + r + 13*fs, y2:P.y + r + 25*fs, anchor:"middle" };
  };

  const nodeSvg = ds.map(d => {
    const P = pos.get(d.id), r = R.get(d.id), Lb = labelAt(P, r);
    // A centred label is held inside the frame however close its node sits to the edge.
    if (Lb.anchor === "middle"){
      const half = Math.max(shortName(d.name).length * 7.2, nodeTheme(d).length * 5.9) * fs / 2 + 4;
      Lb.x = Math.min(W - half, Math.max(half, Lb.x));
    }
    const share = d.works.length ? d.inField / d.works.length : 0;
    const theme = nodeTheme(d);
    const tip = t("{name} — {n} in-field of {works} ({pct}%) · {cov}% with reference lists",
      { name:d.name, n:d.inField, works:tn(d.works.length, "work"), pct:Math.round(share*100), cov:d.refCoverage });
    return `<g class="node ${nodeOn(d) ? "" : "dim"}" data-node="${esc(d.id)}" tabindex="0" role="button" aria-label="${esc(tip)}">
      <title>${esc(tip)}</title>
      <circle cx="${P.x.toFixed(1)}" cy="${P.y.toFixed(1)}" r="${r.toFixed(1)}"
        style="fill:var(--accent);fill-opacity:${(0.08 + 0.5*share).toFixed(2)};stroke:var(--accent)"
        stroke-width="${d.id === F ? 2.5 : 1.2}"/>
      <text x="${Lb.x.toFixed(1)}" y="${Lb.y1.toFixed(1)}" text-anchor="${Lb.anchor}"
        style="font:600 ${(12*fs).toFixed(1)}px var(--sans);fill:var(--ink);stroke:var(--card);stroke-width:3.5px;paint-order:stroke">${esc(shortName(d.name))}</text>
      <text x="${Lb.x.toFixed(1)}" y="${Lb.y2.toFixed(1)}" text-anchor="${Lb.anchor}"
        style="font:${(10.5*fs).toFixed(1)}px var(--sans);fill:var(--ink-3);stroke:var(--card);stroke-width:3px;paint-order:stroke">${esc(theme)}</text>
    </g>`;
  }).join("");

  box.innerHTML = `<svg id="cmpSvg" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img"
      aria-label="${esc(t("{layer} between {scholars}", { layer:LL, scholars:tn(ds.length, "scholar") }))}">
    <defs><marker id="arr" viewBox="0 0 10 10" refX="0" refY="5" markerUnits="userSpaceOnUse"
      markerWidth="${(8*Math.max(1,fs*0.9)).toFixed(1)}" markerHeight="${(8*Math.max(1,fs*0.9)).toFixed(1)}" orient="auto">
      <path d="M0 0 L10 5 L0 10 z" style="fill:var(${L.color})"/></marker></defs>
    <rect class="bg" x="0" y="0" width="${W}" height="${H}" fill="transparent"/>
    ${edgeSvg}${nodeSvg}
    ${edges.length ? "" : `<text x="${W/2}" y="${H - 22}" text-anchor="middle"
      style="font:${(12*fs).toFixed(1)}px var(--sans);fill:var(--ink-3)">${esc(t("No {layer} between these scholars in the indexed record — try another layer.", { layer:LL.toLowerCase() }))}</text>`}
  </svg>`;

  $("#cmpLegend").innerHTML = t("cmp.legend", { label:esc(LL), note:esc(layerNote(CMP.layer)) });

  const svg = $("#cmpSvg");
  const act = el => {
    const edge = el.closest(".edge"), node = el.closest(".node");
    if (edge) selectPair(edge.dataset.pair, false);
    else if (node){ CMP.pair = null; CMP.focus = CMP.focus === node.dataset.node ? null : node.dataset.node; drawGraph(); CMP.focus ? renderNodeDetail() : ($("#cmpDetail").innerHTML = ""); markRow(); }
    else { CMP.focus = null; CMP.pair = null; drawGraph(); $("#cmpDetail").innerHTML = ""; markRow(); }
  };
  svg.addEventListener("click", e => act(e.target));
  svg.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " "){ e.preventDefault(); act(e.target); } });
}

function selectPair(key, scroll){
  CMP.pair = CMP.pair === key && !scroll ? null : key;
  CMP.focus = null;
  // Opening a pair on a layer where it has no tie would grey out the whole
  // map; jump to the layer that shows how these two are actually connected.
  if (CMP.pair && !layerEdges(CMP.layer).some(e => e.p.key === CMP.pair)){
    const alt = ["co", "cites", "refs", "themes"].find(k => layerEdges(k).some(e => e.p.key === CMP.pair));
    if (alt){
      CMP.layer = alt;
      $$("#cmpLayers button").forEach(b => b.classList.toggle("on", b.dataset.layer === alt));
    }
  }
  drawGraph(); markRow();
  if (CMP.pair){ renderPairDetail(); if (scroll) $("#cmpDetail").scrollIntoView({ behavior:"smooth", block:"start" }); }
  else $("#cmpDetail").innerHTML = "";
}
function markRow(){ $$("#cmpRoot tr[data-pair]").forEach(tr => tr.classList.toggle("sel", tr.dataset.pair === CMP.pair)); }

const pct0 = v => Math.round(v * 100) + "%";

function pairTable(){
  const rows = CMP.pairs.slice().sort((a, b) => b.strength - a.strength);
  return `<table class="grid"><thead><tr>
    <th>${esc(t("Pair"))}</th><th class="num">${esc(t("Co-authored"))}</th>
    <th class="num" title="${esc(t("Works by the first scholar citing the second"))}">${esc(t("Cites →"))}</th>
    <th class="num" title="${esc(t("Works by the second scholar citing the first"))}">${esc(t("← Cites"))}</th>
    <th class="num" title="${esc(t("References both cite; coupling strength in brackets"))}">${esc(t("Shared refs"))}</th>
    <th class="num">${esc(t("Theme overlap"))}</th><th class="num">${esc(t("Shared venues"))}</th>
  </tr></thead><tbody>${rows.map(p => `
    <tr class="clickable ${CMP.pair === p.key ? "sel" : ""}" data-pair="${esc(p.key)}">
      <td><b>${esc(shortName(p.a.name))}</b> · <b>${esc(shortName(p.b.name))}</b></td>
      <td class="num">${p.co.length || "—"}</td>
      <td class="num">${p.ab.citing.length || "—"}</td>
      <td class="num">${p.ba.citing.length || "—"}</td>
      <td class="num">${p.shared.length ? `${p.shared.length} <span class="muted">(${(p.salton*100).toFixed(1)}%)</span>` : "—"}</td>
      <td class="num">${pct0(p.sim)}${p.lowSample ? ` <span title="${esc(t("One of the two has fewer than five in-field works"))}" class="warn-txt">*</span>` : ""}</td>
      <td class="num">${p.venues.length || "—"}</td>
    </tr>`).join("")}</tbody></table>`;
}

/** Surname only for column heads — unless two scholars share one. */
function colNames(ds){
  const sur = ds.map(d => String(d.name).trim().split(/\s+/).pop());
  return ds.map((d, i) => sur.filter(x => x === sur[i]).length > 1 ? shortName(d.name) : sur[i]);
}

/* Compact labels, so each theme holds one line and the grid fits half the
   screen; the full name is on hover. */
function themeGrid(ds){
  const ids = new Set(ds.flatMap(d => d.x.all.map(r => r.id)));
  const rows = THEMES.filter(th => ids.has(th.id)).map(th => {
    const cells = ds.map(d => {
      const r = d.x.all.find(x => x.id === th.id);
      return { v: r && d.x.total ? r.n / d.x.total : 0, n: r?.n || 0, core: r?.tier === "core" };
    });
    return { th, cells, sum: cells.reduce((a, c) => a + c.v, 0) };
  }).sort((a, b) => b.sum - a.sum);
  if (!rows.length) return `<div class="empty">${esc(t("None of these scholars has in-field works to profile."))}</div>`;
  const heads = colNames(ds);
  return `<table class="grid tgrid"><thead><tr><th>${esc(t("Theme"))}</th>${ds.map((d, i) =>
      `<th class="sch" title="${esc(d.name)} — ${esc(tn(d.inField, "in-field work"))}">${esc(heads[i])}</th>`).join("")}</tr></thead>
    <tbody>${rows.map(r => `<tr><td class="tlab" title="${esc(themeName(r.th.id))}">${esc(themeGridLabel(r.th.id))}</td>${r.cells.map(c => {
      const p = Math.round(c.v * 100);
      return `<td class="cell ${c.core ? "core" : ""}" title="${esc(tn(c.n, "work"))}"
        style="background:color-mix(in srgb, var(--accent) ${Math.min(90, p * 1.1)}%, transparent);${p > 48 ? "color:#fff" : ""}">${p ? p + "%" : "·"}</td>`;
    }).join("")}</tr>`).join("")}</tbody></table>`;
}

function workLi(w, extra = ""){
  const href = w.doi ? "https://doi.org/" + w.doi : (w.landing || "");
  return `<li><span class="yr">${w.year || esc(t("n.d."))}</span>${href
    ? `<a href="${esc(href)}" target="_blank" rel="noopener">${esc(w.title)}</a>` : esc(w.title)}${extra}</li>`;
}
function capList(items, n, render){
  return items.slice(0, n).map(render).join("") +
    (items.length > n ? `<li class="dd-empty">${esc(t("+ {n} more — in the JSON export", { n:items.length - n }))}</li>` : "");
}

function renderPairDetail(){
  const p = CMP.pairs.find(x => x.key === CMP.pair);
  if (!p) return;
  const A = shortName(p.a.name), B = shortName(p.b.name);
  const bits = [];
  if (p.co.length) bits.push(t("{n} co-authored {works}", { n:p.co.length, works:tw(p.co.length, "work") }));
  if (p.ab.citing.length || p.ba.citing.length)
    bits.push(t("pair.cites", { a:A, b:B, ab:p.ab.citing.length, ba:p.ba.citing.length, abWorks:tn(p.ab.citing.length, "work.loc") }));
  else bits.push(t("no citations either way in the indexed reference lists"));
  bits.push(t("{pct} thematic overlap", { pct:pct0(p.sim) }));
  const cite = list => list.length
    ? `<ul class="dd-list">${capList(list, 12, c => workLi(c.w,
        `<div class="cited">→ ${esc(t("cites"))} ${c.cited.map(x => `<i>${esc(x.title)}</i> (${x.year || esc(t("n.d."))})`).join("; ")}</div>`))}</ul>`
    : `<div class="dd-empty">${esc(t("None found in the indexed reference lists."))}</div>`;

  $("#cmpDetail").innerHTML = `<div class="card"><header><h3>${esc(p.a.name)} ↔ ${esc(p.b.name)}</h3><div class="sp"></div>
      <button class="icon-btn" id="ddClose">${esc(t("Close"))}</button></header>
    <div class="body">
      <div class="dd-sum">${esc(bits.join("; "))}.</div>
      <div class="dd-grid">
        <div class="dd-sec"><h5>${esc(t("{a} cites {b}", { a:A, b:B }))} · ${p.ab.citing.length}</h5>${cite(p.ab.citing)}</div>
        <div class="dd-sec"><h5>${esc(t("{a} cites {b}", { a:B, b:A }))} · ${p.ba.citing.length}</h5>${cite(p.ba.citing)}</div>
        <div class="dd-sec"><h5>${esc(t("Co-authored"))} · ${p.co.length}</h5>${p.co.length
          ? `<ul class="dd-list">${capList(p.co.slice().sort((x,y)=>(y.year||0)-(x.year||0)), 12, w => workLi(w))}</ul>`
          : `<div class="dd-empty">${esc(t("No shared works under these two profiles."))}</div>`}</div>
        <div class="dd-sec"><h5>${esc(t("Where they overlap"))}</h5>
          ${p.sharedThemes.length ? `<div class="themes" style="margin-bottom:10px">${p.sharedThemes.map(id =>
             `<span class="theme"><span class="tn" style="font-size:0.875rem">${esc(themeName(id))}</span></span>`).join("")}</div>`
             : `<div class="dd-empty" style="margin-bottom:10px">${esc(t("No core or secondary theme in common."))}</div>`}
          ${p.venues.length ? `<ul class="dd-list">${capList(p.venues, 8, v =>
             `<li>${esc(venueLabel(v.name))} <span class="yr" style="margin-left:6px">${v.a} · ${v.b}</span></li>`)}</ul>`
             : `<div class="dd-empty">${esc(t("No venue in common."))}</div>`}
        </div>
        <div class="dd-sec"><h5>${esc(t("Shared references"))} · ${p.shared.length}</h5>
          ${p.shared.length ? `<div class="dd-empty" style="margin-bottom:7px">${esc(t("Works both have cited"))}${p.salton ? esc(t("; coupling {pct}%", { pct:(p.salton*100).toFixed(1) })) : ""}.</div>
            <button class="icon-btn" id="ddRefs">${esc(t("List them"))}</button><ul class="dd-list" id="ddRefList"></ul>`
            : `<div class="dd-empty">${esc(t("None in the indexed reference lists."))}</div>`}</div>
      </div>
    </div></div>`;
  $("#ddClose").onclick = () => selectPair(CMP.pair, false);
  const rb = $("#ddRefs");
  if (rb) rb.onclick = async () => {
    rb.disabled = true; rb.textContent = t("Loading…");
    const ids = p.shared.slice(0, 50);
    const d = await getJSON(oa("/works", { filter:"ids.openalex:" + ids.join("|"), per_page:50,
      select:"id,title,publication_year,authorships,doi" }), { optional:true });
    const list = (d?.results || []).sort((x, y) => (y.publication_year||0) - (x.publication_year||0));
    $("#ddRefList").innerHTML = list.map(w => {
      const au = (w.authorships || []).map(a => a.author?.display_name).filter(Boolean);
      const by = au.length ? esc(au[0].split(" ").pop()) + (au.length > 1 ? " " + esc(t("et al.")) : "") + " — " : "";
      return `<li><span class="yr">${w.publication_year || esc(t("n.d."))}</span>${by}${w.doi
        ? `<a href="${esc(w.doi)}" target="_blank" rel="noopener">${esc(w.title || "[untitled]")}</a>` : esc(w.title || "[untitled]")}</li>`;
    }).join("") + (p.shared.length > 50 ? `<li class="dd-empty">${esc(t("+ {n} more", { n:p.shared.length - 50 }))}</li>` : "");
    rb.remove();
  };
}

function renderNodeDetail(){
  const d = CMP.data.get(CMP.focus);
  if (!d) return;
  const rel = CMP.pairs.filter(p => p.a.id === d.id || p.b.id === d.id).map(p => {
    const other = p.a.id === d.id ? p.b : p.a, out = p.a.id === d.id ? p.ab : p.ba, inn = p.a.id === d.id ? p.ba : p.ab;
    return { p, other, out:out.citing.length, inn:inn.citing.length };
  }).sort((x, y) => y.p.strength - x.p.strength);
  $("#cmpDetail").innerHTML = `<div class="card"><header><h3>${esc(d.name)}</h3><div class="sp"></div>
      <button class="icon-btn" id="ddOpen">${esc(t("Open dossier"))}</button><button class="icon-btn" id="ddClose">${esc(t("Close"))}</button></header>
    <div class="body">
      <div class="dd-sum">${esc(expertiseHeadline(d.x, { relevantPct: d.works.length ? Math.round(100*d.inField/d.works.length) : 0 }))}</div>
      <div class="note">${esc(t("{n} in-field of {works} · reference lists for {pct}% of them.", { n:d.inField, works:tn(d.works.length, "work"), pct:d.refCoverage }))}</div>
      <div class="scrollx flush"><table class="grid"><thead><tr><th>${esc(t("With"))}</th><th class="num">${esc(t("Co-authored"))}</th><th class="num">${esc(t("Cites them"))}</th>
        <th class="num">${esc(t("Cited by them"))}</th><th class="num">${esc(t("Theme overlap"))}</th></tr></thead>
      <tbody>${rel.map(r => `<tr class="clickable" data-pair="${esc(r.p.key)}"><td>${esc(r.other.name)}</td>
        <td class="num">${r.p.co.length || "—"}</td><td class="num">${r.out || "—"}</td>
        <td class="num">${r.inn || "—"}</td><td class="num">${pct0(r.p.sim)}</td></tr>`).join("")}</tbody></table></div>
    </div></div>`;
  $("#ddClose").onclick = () => { CMP.focus = null; drawGraph(); $("#cmpDetail").innerHTML = ""; };
  $("#ddOpen").onclick = () => openScholar(d.id);
  $$("#cmpDetail tr[data-pair]").forEach(tr => tr.onclick = () => selectPair(tr.dataset.pair, true));
}

/* Exports resolve the theme's CSS variables into literal colours — a
   standalone SVG has no stylesheet to look them up in. */
function exportCompareSVG(){
  const svg = $("#cmpSvg");
  if (!svg) return;
  const cs = getComputedStyle(document.documentElement);
  let txt = new XMLSerializer().serializeToString(svg)
    .replace(/var\((--[\w-]+)\)/g, (m, v) => cs.getPropertyValue(v).trim() || m)
    .replace('<rect class="bg" x="0" y="0"', `<rect class="bg" x="0" y="0" style="fill:${cs.getPropertyValue("--card").trim()}"`);
  txt = txt.replace(/font:([^;"]*)var\(--(sans|mono)\)/g, "font:$1sans-serif");
  download(`srom-relations-${CMP.layer}-${stamp()}.svg`, txt, "image/svg+xml");
}
function exportCompareCSV(){
  const head = ["scholar_a","scholar_b","co_authored","a_cites_b_works","b_cites_a_works","a_cites_b_links","b_cites_a_links",
                "shared_references","coupling_pct","theme_overlap_pct","shared_venues","shared_themes","low_sample"];
  const rows = CMP.pairs.map(p => [p.a.name, p.b.name, p.co.length, p.ab.citing.length, p.ba.citing.length, p.ab.links, p.ba.links,
    p.shared.length, (p.salton*100).toFixed(2), Math.round(p.sim*100), p.venues.map(v => v.name).join("; "),
    p.sharedThemes.map(themeName).join("; "), p.lowSample ? "yes" : ""].map(csvCell).join(","));
  download(`srom-relations-${stamp()}.csv`, "﻿" + head.join(",") + "\n" + rows.join("\n"), "text/csv;charset=utf-8");
}
function exportCompareJSON(){
  const w = x => ({ year:x.year, title:x.title, doi:x.doi ? "https://doi.org/" + x.doi : null });
  const out = {
    generated:new Date().toISOString(), tool:"SROM Scholar Audit — relations", language:I18N.lang,
    method:Object.fromEntries(Object.keys(LAYERS).map(k => [k, layerNote(k)])),
    scholars:CMP.ids.map(id => { const d = CMP.data.get(id); return { openalex:id, name:d.name, works:d.works.length,
      inField:d.inField, referenceCoverage:d.refCoverage, themes:d.x.all.map(r => ({ theme:themeName(r.id), works:r.n, tier:r.tier })) }; }),
    pairs:CMP.pairs.map(p => ({ a:p.a.name, b:p.b.name, coAuthored:p.co.map(w),
      aCitesB:p.ab.citing.map(c => ({ citing:w(c.w), cited:c.cited.map(w) })),
      bCitesA:p.ba.citing.map(c => ({ citing:w(c.w), cited:c.cited.map(w) })),
      sharedReferences:p.shared.map(id => "https://openalex.org/" + id), coupling:+p.salton.toFixed(4),
      themeOverlap:+p.sim.toFixed(3), sharedThemes:p.sharedThemes.map(themeName), sharedVenues:p.venues, lowSample:p.lowSample })),
  };
  download(`srom-relations-${stamp()}.json`, JSON.stringify(out, null, 2), "application/json");
}

let cmpResizeT;
addEventListener("resize", () => {
  clearTimeout(cmpResizeT);
  cmpResizeT = setTimeout(() => { if (CMP.active && $("#cmpGraph")) drawGraph(); }, 220);
});
