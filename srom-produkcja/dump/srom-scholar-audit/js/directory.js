"use strict";

/* =====================================================================
   Field directory — who publishes in Romani studies: by theme, by the
   country they are based in, over a chosen period. For finding
   collaborators, contributors, board members, speakers, supervisors.

   One OpenAlex query groups the field's works by author and counts them;
   a second fills in each person's record, fifty at a time. Six requests,
   a couple of seconds.
   ===================================================================== */

const DIR = {
  f: { theme:"", country:"", years:"10", sort:"field", hideUncited:true, q:"" },
  status: "idle",     // idle | loading | done | error
  rows: [],           // [{ id, count, a }]
  countries: [],      // [{ code, n }] — for the country list
  total: 0,           // matching works
  dropped: 0,         // co-authors based in another country
  selected: new Set(),
  shown: 50,
  runId: 0,
  error: "",
};

const DIR_YEARS = ["5", "10", "15", "25", "any"];
const DIR_SORTS = [["field","Most in-field works"], ["h","h-index"], ["cites","Citations"], ["recent","Most recently active"], ["name","Name"]];

const dirSince = () => DIR.f.years === "any" ? null : THIS_YEAR - (+DIR.f.years || 10);

function dirFilter({ withCountry = true } = {}){
  const parts = ["topics.id:" + FIELD.topicIds.join("|")];
  const since = dirSince();
  if (since) parts.push("from_publication_date:" + since + "-01-01");
  if (withCountry && DIR.f.country) parts.push("authorships.institutions.country_code:" + DIR.f.country);
  return parts.join(",");
}
/** A theme's search: whole words OR'd — OpenAlex matches words, not the
    substrings the expertise profile uses. */
function themeQuery(id){ const th = themeById(id); return th ? "(" + th.q.join(" OR ") + ")" : undefined; }

/** Based in the country: their current institution, or one they were at in
    the last three years. A work counts toward a country if any co-author is
    there, so the list is narrowed to people who actually are. */
function basedIn(a, cc){
  if (currentInstOf(a)?.country_code === cc) return true;
  return (a.affiliations || []).some(af => af.institution?.country_code === cc && (af.years || []).some(y => y >= THIS_YEAR - 3));
}

function dirAddress(){
  const f = DIR.f;
  setAddress({ theme:f.theme, country:f.country, years:f.years !== "10" ? f.years : "", sort:f.sort !== "field" ? f.sort : "" }, "directory");
}

async function runDirectory(){
  const run = ++DIR.runId;
  DIR.status = "loading"; DIR.error = ""; DIR.shown = 50; DIR.selected.clear();
  dirAddress();
  renderDirectory();
  try {
    const search = DIR.f.theme ? themeQuery(DIR.f.theme) : undefined;
    const [g, c] = await Promise.all([
      getJSON(oa("/works", { filter:dirFilter(), search, group_by:"authorships.author.id", per_page:200 })),
      getJSON(oa("/works", { filter:dirFilter({ withCountry:false }), search,
                             group_by:"authorships.institutions.country_code", per_page:200 }), { optional:true }),
    ]);
    if (run !== DIR.runId) return;
    DIR.total = g.meta?.count || 0;
    DIR.countries = (c?.group_by || []).map(x => ({ code:shortId(x.key).toUpperCase(), n:x.count }))
      .filter(x => /^[A-Z]{2}$/.test(x.code));
    const groups = (g.group_by || []).filter(x => /\/A\d+$/.test(x.key || ""));
    const authors = await fetchAuthors(groups.map(x => shortId(x.key)));
    if (run !== DIR.runId) return;
    let rows = groups.map(x => ({ id:shortId(x.key), count:x.count, a:authors.get(shortId(x.key)) })).filter(r => r.a);
    DIR.dropped = 0;
    if (DIR.f.country){
      const n = rows.length;
      rows = rows.filter(r => basedIn(r.a, DIR.f.country));
      DIR.dropped = n - rows.length;
    }
    DIR.rows = rows;
    DIR.status = "done";
  } catch (e){
    if (run !== DIR.runId) return;
    DIR.status = "error"; DIR.error = e.message;
  }
  renderDirectory();
}

function dirSorted(){
  const q = DIR.f.q.toLowerCase().trim();
  const rows = DIR.rows.filter(r => {
    if (DIR.f.hideUncited && !(r.a.cited_by_count > 0)) return false;
    if (!q) return true;
    return [r.a.display_name, currentInstOf(r.a)?.display_name].join(" ").toLowerCase().includes(q);
  });
  const by = {
    field:  (a, b) => b.count - a.count || (b.a.summary_stats?.h_index || 0) - (a.a.summary_stats?.h_index || 0),
    h:      (a, b) => (b.a.summary_stats?.h_index || 0) - (a.a.summary_stats?.h_index || 0) || b.count - a.count,
    cites:  (a, b) => (b.a.cited_by_count || 0) - (a.a.cited_by_count || 0),
    recent: (a, b) => (activeSpan(b.a)[1] || 0) - (activeSpan(a.a)[1] || 0) || b.count - a.count,
    name:   (a, b) => String(a.a.display_name).localeCompare(String(b.a.display_name), LOCALE()),
  }[DIR.f.sort] || (() => 0);
  return rows.sort(by);
}

function renderDirectory(){
  if (CMP.host === "directory") CMP.active = false;
  const f = DIR.f;
  const opt = (v, label, cur) => `<option value="${esc(v)}" ${String(cur) === String(v) ? "selected" : ""}>${esc(label)}</option>`;
  const countries = DIR.countries.slice().sort((a, b) => b.n - a.n);
  if (f.country && !countries.some(c => c.code === f.country)) countries.unshift({ code:f.country, n:null });
  const since = dirSince();

  let body;
  if (DIR.status === "loading" || DIR.status === "idle")
    body = `<div class="progress"><span class="spinner"></span> ${esc(t("Reading the field's works in OpenAlex…"))}</div>`;
  else if (DIR.status === "error")
    body = `<div class="err">${esc(t("Lookup failed: {msg}", { msg:DIR.error }))} <button class="icon-btn" id="dirRetry">${esc(t("Try again"))}</button></div>`;
  else {
    const rows = dirSorted();
    const hidden = DIR.rows.length - rows.length;
    body = `
      <div class="dir-sum">
        <span>${esc(t("{scholars} from {works}", { scholars:tn(rows.length, "scholar"), works:tn(DIR.total, "work") }))}
          ${f.theme ? " · " + esc(themeName(f.theme)) : ""}${f.country ? " · " + esc(countryName(f.country)) : ""}
          · ${esc(since ? t("since {year}", { year:since }) : t("all years"))}</span>
        ${hidden && f.hideUncited && !f.q ? `<span class="muted">${esc(t("{n} uncited profiles hidden", { n:hidden }))}</span>` : ""}
        ${DIR.dropped ? `<span class="muted">${esc(t("{n} co-authors based elsewhere left out", { n:DIR.dropped }))}</span>` : ""}
      </div>
      ${rows.length ? `<div class="dir-list" role="list">
        <div class="dir-row dir-headrow" aria-hidden="true">
          <span></span><span>${esc(t("Scholar"))}</span><span class="dn">${esc(t("In field"))}</span><span class="dn">h</span>
          <span class="dn">${esc(t("Works"))}</span><span class="dn">${esc(t("Cites"))}</span><span class="dn">${esc(t("Active"))}</span><span></span>
        </div>
        ${rows.slice(0, DIR.shown).map(dirRow).join("")}
      </div>
      ${rows.length > DIR.shown ? `<div class="more-row"><button class="icon-btn" id="dirMore">${esc(t("Show {n} more", { n:Math.min(50, rows.length - DIR.shown) }))}</button></div>` : ""}
      <div class="cmpbar" id="dirBar"></div>`
      : `<div class="empty">${esc(t("Nobody matches these filters. Widen the period or clear the theme."))}</div>`}`;
  }

  setView("directory", `
  <div class="card">
    <header><h3>${esc(t("Field directory"))}</h3><div class="sp"></div>
      <span class="hdr-note">${esc(t("who publishes in Romani studies — by theme, country and period"))}</span></header>
    <div class="body">
      <div class="controls">
        <label class="ctl">${esc(t("Theme"))}
          <select id="dirTheme">${opt("", t("All themes"), f.theme)}${THEMES.map(th => opt(th.id, themeName(th.id), f.theme)).join("")}</select></label>
        <label class="ctl">${esc(t("Based in"))}
          <select id="dirCountry">${opt("", t("All countries"), f.country)}${countries.map(c =>
            opt(c.code, countryName(c.code) + (c.n != null ? " · " + num(c.n) : ""), f.country)).join("")}</select></label>
        <label class="ctl">${esc(t("Publishing in the last"))}
          <select id="dirYears">${DIR_YEARS.map(y => opt(y, y === "any" ? t("any period") : tn(+y, "year"), f.years)).join("")}</select></label>
        <label class="ctl">${esc(t("Sort"))}
          <select id="dirSort">${DIR_SORTS.map(([v, l]) => opt(v, t(l), f.sort)).join("")}</select></label>
        <label class="chk"><input type="checkbox" id="dirUncited" ${f.hideUncited ? "checked" : ""}> ${esc(t("Hide uncited profiles"))}</label>
        <span class="ctl-sp"></span>
        <label class="ctl"><input type="text" id="dirQ" placeholder="${esc(t("Filter by name or institution"))}" value="${esc(f.q)}"></label>
      </div>
      ${body}
      <p class="fine">${esc(t("dir.fine"))}</p>
    </div>
  </div>`);

  wireDirectory();
}

function dirRow(r){
  const a = r.a, inst = currentInstOf(a), [first, last] = activeSpan(a);
  const saved = LIB.scholars[r.id];
  const picked = DIR.selected.has(r.id);
  const also = (a.topics || []).filter(tp => !FIELD.topicIds.includes(shortId(tp.id))).slice(0, 2).map(tp => tp.display_name);
  return `<div class="dir-row ${picked ? "picked" : ""}" role="listitem" data-id="${esc(r.id)}">
    <label class="pick" title="${esc(t("Select"))}"><input type="checkbox" data-dpick="${esc(r.id)}" ${picked ? "checked" : ""}></label>
    <div class="dir-main">
      <button class="pname" data-open="${esc(r.id)}">${esc(a.display_name)}</button>
      ${a.orcid ? `<span class="b oa" title="ORCID ${esc(orcidOf(a.orcid))}">ORCID</span>` : ""}
      ${saved ? `<span class="b manual">★ ${esc(t("saved"))}</span>` : ""}
      <div class="psub">${esc(inst?.display_name || t("No affiliation recorded"))}${inst?.country_code ? " · " + esc(countryName(inst.country_code)) : ""}</div>
      ${also.length ? `<div class="pmeta">${esc(t("also:"))} ${esc(also.join(" · "))}</div>` : ""}
    </div>
    <div class="dn" data-l="${esc(t("In field"))}"><b>${num(r.count)}</b></div>
    <div class="dn" data-l="h">${a.summary_stats?.h_index ?? "—"}</div>
    <div class="dn" data-l="${esc(t("Works"))}">${num(a.works_count)}</div>
    <div class="dn" data-l="${esc(t("Cites"))}">${num(a.cited_by_count)}</div>
    <div class="dn" data-l="${esc(t("Active"))}">${first ? (first === last ? first : first + "–" + last) : "—"}</div>
    <div class="dir-act"><button class="icon-btn" data-save="${esc(r.id)}" title="${esc(saved ? t("Add to a folder") : t("Save to library"))}">${saved ? "★" : "☆"}</button></div>
  </div>`;
}

function wireDirectory(){
  const V = "#view-directory";
  const set = (k, v, rerun = true) => { DIR.f[k] = v; if (rerun) runDirectory(); else { dirAddress(); renderDirectory(); } };
  $("#dirTheme").onchange   = e => set("theme", e.target.value);
  $("#dirCountry").onchange = e => set("country", e.target.value);
  $("#dirYears").onchange   = e => set("years", e.target.value);
  $("#dirSort").onchange    = e => set("sort", e.target.value, false);
  $("#dirUncited").onchange = e => set("hideUncited", e.target.checked, false);
  const qi = $("#dirQ");
  let tm;
  qi.addEventListener("input", e => {
    clearTimeout(tm);
    const v = e.target.value;
    tm = setTimeout(() => {
      DIR.f.q = v; renderDirectory();
      const el = $("#dirQ"); if (el){ el.focus(); el.setSelectionRange(el.value.length, el.value.length); }
    }, 220);
  });
  const rt = $("#dirRetry"); if (rt) rt.onclick = runDirectory;
  const mo = $("#dirMore"); if (mo) mo.onclick = () => { DIR.shown += 50; renderDirectory(); };

  $$(`${V} [data-open]`).forEach(b => b.onclick = () => openScholar(b.dataset.open));
  $$(`${V} [data-dpick]`).forEach(cb => cb.onchange = () => {
    cb.checked ? DIR.selected.add(cb.dataset.dpick) : DIR.selected.delete(cb.dataset.dpick);
    cb.closest(".dir-row").classList.toggle("picked", cb.checked);
    dirBar();
  });
  $$(`${V} [data-save]`).forEach(b => b.onclick = async () => {
    const r = DIR.rows.find(x => x.id === b.dataset.save);
    if (!r) return;
    const fid = await pickFolder({ title:t("Save {name}", { name:r.a.display_name }) });
    if (fid === null) return;
    await libSaveAuthors([r.a], fid);
    toast(t("Saved to your library."));
    renderDirectory();
  });
  dirBar();
}

function dirBar(){
  const bar = $("#dirBar");
  if (!bar) return;
  const n = DIR.selected.size;
  bar.innerHTML = `
    <span>${n ? esc(t("{n} selected", { n })) : esc(t("Tick scholars to save them together or map how they relate"))}</span>
    <span class="ctl-sp"></span>
    ${n ? `<button class="icon-btn" id="dirClear">${esc(t("Clear"))}</button>
           <button class="icon-btn" id="dirSaveSel">${esc(t("Save to folder…"))}</button>` : ""}
    <button class="icon-btn" id="dirCsv">${esc(t("Export CSV"))}</button>
    <button class="btn small" id="dirMap" ${n < 2 ? "disabled" : ""}>${esc(t("Map relations"))}</button>`;
  bar.classList.toggle("active", n >= 2);
  const sel = () => DIR.rows.filter(r => DIR.selected.has(r.id));
  const cl = $("#dirClear"); if (cl) cl.onclick = () => { DIR.selected.clear(); renderDirectory(); };
  const sv = $("#dirSaveSel"); if (sv) sv.onclick = async () => {
    const fid = await pickFolder({ title:t("Save {n} to the library", { n:tn(n, "scholar") }) });
    if (fid === null) return;
    const added = await libSaveAuthors(sel().map(r => r.a), fid);
    toast(t("Saved: {n} new in the library.", { n:added }));
    DIR.selected.clear(); renderDirectory();
  };
  $("#dirCsv").onclick = () => exportDirectoryCSV(DIR.selected.size ? sel() : dirSorted());
  $("#dirMap").onclick = () => {
    if (n > CMP_MAX) return toast(t("Up to {n} at a time — beyond that the map stops being readable.", { n:CMP_MAX }), { bad:true });
    const rows = sel();
    renderCompare(rows.map(r => r.id), { host:"directory", names:Object.fromEntries(rows.map(r => [r.id, r.a.display_name])) });
  };
}

function exportDirectoryCSV(rows){
  const head = ["name","openalex","orcid","institution","country","in_field_works_in_period","works","citations","h_index","first_year","last_year"];
  const lines = rows.map(r => { const a = r.a, inst = currentInstOf(a), [first, last] = activeSpan(a);
    return [a.display_name, "https://openalex.org/" + r.id, a.orcid || "", inst?.display_name || "", inst?.country_code || "",
            r.count, a.works_count, a.cited_by_count, a.summary_stats?.h_index ?? "", first ?? "", last ?? ""].map(csvCell).join(","); });
  const tag = [DIR.f.theme, DIR.f.country].filter(Boolean).join("-") || "all";
  download(`srom-directory-${tag}-${stamp()}.csv`, "﻿" + head.join(",") + "\n" + lines.join("\n"), "text/csv;charset=utf-8");
}

VIEW_ENTER.directory = () => {
  if (CMP.active && CMP.host === "directory") return drawGraph();
  if (DIR.status === "idle") runDirectory();
  else dirAddress();
};
