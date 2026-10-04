"use strict";

/* =====================================================================
   Check a scholar — the dossier.
   Type a name, ORCID or OpenAlex ID; get the publication record with its
   indexing, the field expertise, identifiers and routes of contact, and
   observations for an editor to weigh.
   ===================================================================== */

/* What the Check view is showing, so a language switch can redraw it. */
const CHECK = { stage:"landing", render:null };

const langName = code => {
  try { return new Intl.DisplayNames([LOCALE()], { type:"language" }).of(code) || code; } catch (e) { return code; }
};

/** OpenAlex work and source types, in the interface language. */
const TYPE_NAMES = {
  "article":"article", "book-chapter":"book chapter", "book":"book", "review":"review", "dissertation":"dissertation",
  "preprint":"preprint", "report":"report", "dataset":"dataset", "editorial":"editorial", "letter":"letter",
  "other":"other", "erratum":"erratum", "reference-entry":"reference entry", "peer-review":"peer review",
  "journal":"journal", "repository":"repository", "book series":"book series", "conference":"conference",
  "ebook platform":"ebook platform", "libguides":"library guide", "standard":"standard", "retraction":"retraction",
  "supplementary-materials":"supplementary materials", "paratext":"paratext",
};
const typeName = k => TYPE_NAMES[k] ? t(TYPE_NAMES[k]) : (k || "");

/* ---------- 10. Rendering: dossier head ------------------------------ */

function renderDossier(){
  const A  = S.author;
  const sm = computeSummary();
  const orcid = orcidOf(A.orcid);

  // One line per institution, most recent first: the first is shown as current.
  const byInst = new Map();
  for (const a of A.affiliations || []){
    const k = a.institution?.id || a.institution?.display_name || "";
    const cur = byInst.get(k);
    if (cur) cur.years = [...new Set([...cur.years, ...(a.years || [])])];
    else byInst.set(k, { inst:a.institution || {}, years:[...(a.years || [])] });
  }
  const affils = [...byInst.values()]
    .sort((x, y) => Math.max(0, ...y.years) - Math.max(0, ...x.years))
    .slice(0, 6).map(({ inst, years }) => {
      const yrs = years.sort((x,y)=>y-x);
      const span = yrs.length ? (yrs.length === 1 ? yrs[0] : yrs[yrs.length-1] + "–" + yrs[0]) : "";
      return `<div>${esc(inst.display_name || "—")}
        ${inst.country_code ? `<span class="yr" title="${esc(countryName(inst.country_code))}"> · ${esc(inst.country_code)}</span>` : ""}
        ${span ? `<span class="yr"> · ${esc(span)}</span>` : ""}</div>`;
    });

  const aka = (A.raw_author_names || []).filter(n => n !== A.display_name);
  const hist = yearHistogram();
  const maxH = Math.max(1, ...hist.map(h => h.n));

  const x = computeExpertise();
  const thisYear = new Date().getFullYear();
  const themeChip = r => {
    const stale = r.last && thisYear - r.last >= 10;
    return `<span class="theme ${stale ? "stale" : ""}" title="${esc(tn(r.n, "work"))} · ${esc(tn(r.cites, "citation"))} · ${r.first}–${r.last}${stale ? " · " + esc(t("nothing in the last decade")) : ""}">
      <span class="tn">${esc(themeName(r.id))}</span>
      <span class="tm">${r.n} · ${r.first === r.last ? r.first : r.first + "–" + r.last}</span></span>`;
  };
  const tierRow = (cls, label, list) => list.length
    ? `<div class="exp-tier ${cls}"><div class="lab">${esc(label)}</div>
         <div class="themes">${list.map(themeChip).join("")}</div></div>` : "";

  const expertise = `
  <div class="card">
    <header><h3>${esc(t("Expertise in Romani studies"))}</h3><div class="sp"></div>
      <span class="hdr-note" title="${esc(t("from {works} · chip shows works · years", { works:tn(x.total, "in-field work") }))}">${esc(tn(x.total, "in-field work"))}</span>
    </header>
    <div class="body">
      <div class="exp-head">${esc(expertiseHeadline(x, sm))}</div>
      ${x.total ? `
        ${x.thin ? `<div class="note" style="margin:0 0 9px">${esc(t("exp.thin"))}</div>` : ""}
        ${tierRow("core", t("Core expertise"), x.core)}
        ${tierRow("sec", t("Secondary"), x.secondary)}
        ${x.peripheral.length || x.topics.length ? `<details class="exp-more" ${S.expMore ? "open" : ""}>
          <summary>${esc([x.peripheral.length ? t("Touched on") + " · " + x.peripheral.length : "",
                          x.topics.length ? t("Machine topics") + " · " + x.topics.length : ""].filter(Boolean).join("   ·   "))}</summary>
        ${tierRow("periph", t("Touched on"), x.peripheral)}
        ${x.topics.length ? `<div class="exp-tier periph">
          <div class="lab">${esc(t("Machine topics"))}</div>
          <div class="themes" style="align-items:center">
            ${x.topics.map(tp=>`<span class="theme"><span class="tn" style="font-weight:500">${esc(tp.name)}</span><span class="tm">${tp.n}</span></span>`).join("")}
          </div></div>` : ""}
        </details>` : ""}
      ` : `<div class="muted">${esc(t("exp.none"))}</div>`}
    </div>
  </div>`;

  const saved = LIB.scholars[shortId(A.id)];
  const stale = S.storedAt && daysSince(S.storedAt) >= DC.STALE_DAYS;
  const storedLine = S.storedAt ? `<span class="stored-note ${stale ? "stale" : ""}"
      title="${esc(t("Opened from a copy kept in this browser"))} · ${esc(fmtWhen(S.storedAt))}">
      ${esc(t("Updated {when}", { when:ageText(S.storedAt) }))}
      <button class="btn small ${stale ? "" : "ghost"}" id="btnUpdate">${esc(t("Update"))}</button></span>` : "";
  const iconBtn = (id, icon, label) =>
    `<button class="icon-btn sq" id="${id}" title="${esc(label)}" aria-label="${esc(label)}">${ICON[icon]}</button>`;
  const actions = `
  <div class="savebar">
    <button class="btn-save ${saved ? "on" : ""}" id="btnSave" aria-pressed="${saved ? "true" : "false"}">
      ${saved ? "★ " + esc(t("Saved")) : "☆ " + esc(t("Save to library"))}
    </button>
    ${iconBtn("btnShare", "link", t("Share link"))}
    ${iconBtn("btnExport", "download", t("Export…"))}
    ${saved && !saved.note && !S.noteOpen ? iconBtn("btnAddNote", "note", t("Add note")) : ""}
    ${saved ? `<div class="folder-pick">
      ${LIB.folders.map(f => `<button class="fchip ${(saved.folders||[]).includes(f.id) ? "on" : ""}"
        data-folder="${f.id}">${esc(f.name)}</button>`).join("")}
      <button class="fchip add" id="btnNewFolderInline">+ ${esc(t("folder"))}</button>
    </div>` : ""}
    ${storedLine}
  </div>
  ${saved && (saved.note || S.noteOpen) ? `<textarea class="libnote" id="libNote" placeholder="${esc(t("Note on this scholar — why you saved them, what to check, who suggested them…"))}">${esc(saved.note || "")}</textarea>` : ""}`;

  // Four figures an editor reads first; the rest sits beside the output chart.
  const relTone = sm.relevantPct >= 50 ? "ok" : sm.relevantPct >= 20 ? "warn" : "bad";
  const stat = (v, l, s, tone = "") =>
    `<div class="stat ${tone}"><div class="v">${esc(v)}</div><div class="l">${esc(l)}</div>${s ? `<div class="s">${esc(s)}</div>` : ""}</div>`;
  const fact = (k, v, s) =>
    `<div class="fact"><span class="k">${esc(k)}</span><span class="v">${esc(v)}</span>${s ? `<span class="s">${esc(s)}</span>` : ""}</div>`;

  const recent = sm.recent ? " " + t("relev.recent", { n:sm.recentRelevant, total:sm.recent }) : "";
  const current = affils[0] || `<span class="muted">${esc(t("No affiliation recorded"))}</span>`;
  const moreBits = [
    affils.length > 1 ? tn(affils.length - 1, "earlier affiliation") : "",
    aka.length ? tn(aka.length, "name variant") : "",
  ].filter(Boolean);

  const html = `
  <div class="d-hero">
    <div class="idrow">
      ${orcid
        ? `<a class="idchip verified" href="https://orcid.org/${esc(orcid)}" target="_blank" rel="noopener">ORCID <b>${esc(orcid)}</b> ✓</a>`
        : `<span class="idchip">ORCID <b>${esc(t("not on record"))}</b></span>`}
      <a class="idchip" href="${esc(A.id)}" target="_blank" rel="noopener">OpenAlex <b>${esc(shortId(A.id))}</b></a>
      ${sm.langs.length ? `<span class="idchip">${esc(t("Publishes in"))} <b>${esc(sm.langs.slice(0,5).map(langName).join(", "))}</b></span>` : ""}
    </div>
    <h1 class="scholar-name">${esc(A.display_name)}</h1>
    <div class="affil">${current}</div>
    ${moreBits.length ? `<details class="d-more"><summary>${esc(moreBits.join(" · "))}</summary>
      ${affils.length > 1 ? `<div class="affil">${affils.slice(1).join("")}</div>` : ""}
      ${aka.length ? `<div class="aka">${esc(t("Also indexed as:"))} ${esc(aka.slice(0,6).join(" · "))}</div>` : ""}
    </details>` : ""}
    ${actions}
  </div>

  <div class="statrow">
    ${stat(num(sm.total), t("Works"), tn(sm.venues, "venue"))}
    ${stat(num(sm.cites), t("Citations"), sm.meanFwci ? "FWCI " + sm.meanFwci.toFixed(2) : "")}
    ${stat(sm.hIndex ?? "—", t("h-index"), sm.i10 != null ? "i10 " + sm.i10 : "")}
    ${stat(sm.relevantPct + "%", t("In Romani studies"), t("{n} of {total}", { n:num(sm.relevant), total:num(sm.total) }), relTone)}
  </div>

  <div class="dossier-head">
    ${expertise}
    <div class="card out-card">
      <header><h3>${esc(t("Output and reach"))}</h3></header>
      <div class="body">
        <p class="relev-txt">${t("relev.main", { n:num(sm.relevant), total:num(sm.total), works:tn(sm.total, "work"),
                                worksGen:tw(sm.total, "work.gen"), times:tn(sm.relCited, "time"), cites:num(sm.relCited) })}${esc(recent)}</p>
        ${hist.length > 1 ? `
        <div class="sparkwrap" role="img" aria-label="${esc(t("Output {from}–{to}", { from:hist[0].year, to:hist[hist.length-1].year }))}">
          ${hist.map(h=>`<i style="height:${Math.round((h.n/maxH)*100)}%" title="${h.year}: ${h.n}"></i>`).join("")}
        </div>
        <div class="spark-axis"><span>${hist[0].year}</span><span>${hist[hist.length-1].year}</span></div>` : ""}
        <div class="facts">
          ${fact(t("Active"), sm.firstYear ? sm.firstYear + "–" + sm.lastYear : "—", sm.span ? tn(sm.span, "year") : "")}
          ${fact(t("Tier A–B"), sm.topTierPct + "%", sm.byTier.A + " A · " + sm.byTier.B + " B")}
          ${fact(t("Open access"), sm.oaPct + "%", tn(sm.oa, "work"))}
        </div>
      </div>
    </div>
  </div>`;

  return html;
}

/** Line icons for compact actions; stroke follows the text colour. */
const ICON = {
  link:`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/></svg>`,
  download:`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11"/><path d="m7 10 5 5 5-5"/><path d="M5 20h14"/></svg>`,
  note:`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h10l4 4v12H5z"/><path d="M9 12h6M9 16h4"/></svg>`,
};

const metric = (v, l, s) =>
  `<div class="metric"><div class="v">${esc(v)}</div><div class="l">${esc(l)}</div>${s?`<div class="s">${esc(s)}</div>`:""}</div>`;

/* ---------- 11. Publication record ----------------------------------- */

function filteredWorks(){
  const f = S.filters;
  const q = f.text.toLowerCase().trim();
  return S.works.filter(w => {
    if (w.paratext) return false;
    if (f.fieldOnly && !w.relevant) return false;
    if (f.oaOnly && !w.oa) return false;
    if (f.type && w.type !== f.type) return false;
    if (f.tier && tierOf(w) !== f.tier) return false;
    if (f.venue && w.venue !== f.venue) return false;
    if (f.from && (!w.year || w.year < f.from)) return false;
    if (f.to   && (!w.year || w.year > f.to)) return false;
    if (q && !(w.title.toLowerCase().includes(q)
            || w.venue.toLowerCase().includes(q)
            || w.coauthors.join(" ").toLowerCase().includes(q))) return false;
    return true;
  });
}

function renderRecord(){
  const works = filteredWorks();
  const all   = S.works.filter(w => !w.paratext);
  const types = [...new Set(all.map(w => w.type))].sort();
  const venues = [...new Set(all.map(w => w.venue))].filter(v => v !== NO_VENUE).sort();
  const yrs = all.map(w => w.year).filter(Boolean);
  const f = S.filters;
  const sm = computeSummary();

  const controls = `
  <div class="rec-sum">
    <span>${t("rec.doi", { p:sm.doiPct })}</span>
    <span>${t("rec.first", { p:pct(sm.firstAuthor, sm.total) })}</span>
    <span>${t("rec.solo", { n:sm.solo })}</span>
  </div>
  <div class="controls">
    <div class="seg" id="viewSeg">
      <button data-view="chrono" class="${S.view==="chrono"?"on":""}">${esc(t("Chronological"))}</button>
      <button data-view="venue"  class="${S.view==="venue"?"on":""}">${esc(t("By venue"))}</button>
      <button data-view="tier"   class="${S.view==="tier"?"on":""}">${esc(t("By indexing tier"))}</button>
    </div>
    <label class="ctl">${esc(t("Years"))}
      <input type="number" id="fFrom" placeholder="${yrs.length?Math.min(...yrs):""}" value="${f.from??""}">
      <span>–</span>
      <input type="number" id="fTo" placeholder="${yrs.length?Math.max(...yrs):""}" value="${f.to??""}">
    </label>
    <label class="ctl">${esc(t("Type"))}
      <select id="fType"><option value="">${esc(t("All"))}</option>
        ${types.map(k=>`<option value="${esc(k)}" ${f.type===k?"selected":""}>${esc(typeName(k))}</option>`).join("")}
      </select>
    </label>
    <label class="ctl">${esc(t("Tier"))}
      <select id="fTier"><option value="">${esc(t("All"))}</option>
        ${Object.keys(TIERS).map(k=>`<option value="${k}" ${f.tier===k?"selected":""}>${k} — ${esc(tierName(k))}</option>`).join("")}
      </select>
    </label>
    <label class="ctl">${esc(t("Venue"))}
      <select id="fVenue"><option value="">${esc(t("All"))}</option>
        ${venues.map(v=>`<option value="${esc(v)}" ${f.venue===v?"selected":""}>${esc(venueLabel(v))}</option>`).join("")}
      </select>
    </label>
    <label class="ctl"><input type="text" id="fText" placeholder="${esc(t("Filter title, venue, co-author"))}" value="${esc(f.text)}" style="width:190px"></label>
    <label class="chk"><input type="checkbox" id="fField" ${f.fieldOnly?"checked":""}> ${esc(t("Romani studies only"))}</label>
    <label class="chk"><input type="checkbox" id="fOA" ${f.oaOnly?"checked":""}> ${esc(t("Open access only"))}</label>
    <div class="ctl-sp"></div>
    <span class="ctl muted">${esc(t("{n} of {total}", { n:works.length, total:all.length }))}</span>
  </div>`;

  if (!works.length)
    return controls + `<div class="card"><div class="empty">${esc(t("No works match these filters."))}</div></div>`;

  let groups;
  if (S.view === "chrono"){
    const byYear = new Map();
    works.slice().sort((a,b) =>
      (b.year||0)-(a.year||0) || String(b.date||"").localeCompare(String(a.date||""))
    ).forEach(w => {
      const k = w.year || t("Undated");
      if (!byYear.has(k)) byYear.set(k, []);
      byYear.get(k).push(w);
    });
    groups = [...byYear.entries()].map(([k,v]) => ({ title:String(k), sub:"", items:v }));

  } else if (S.view === "venue"){
    const byV = new Map();
    works.forEach(w => {
      if (!byV.has(w.venue)) byV.set(w.venue, []);
      byV.get(w.venue).push(w);
    });
    groups = [...byV.entries()]
      .sort((a,b) => b[1].length - a[1].length || a[0].localeCompare(b[0]))
      .map(([k,v]) => {
        const best = v.slice().sort((x,y)=>tierRank(y)-tierRank(x))[0];
        const ys = v.map(w=>w.year).filter(Boolean);
        return {
          title: venueLabel(k),
          sub: `<span class="b t${tierOf(best)}">${tierOf(best)} · ${esc(tierName(tierOf(best)))}</span>`
             + (ys.length ? ` <span class="c">${Math.min(...ys)}–${Math.max(...ys)}</span>` : "")
             + ` <span class="c">${esc(tn(v.reduce((a,b)=>a+b.cites,0), "citation"))}</span>`,
          items: v.slice().sort((a,b)=>(b.year||0)-(a.year||0)),
        };
      });

  } else {
    groups = Object.keys(TIERS)
      .sort((a,b)=>TIERS[b].rank-TIERS[a].rank)
      .map(k => ({
        title: t("Tier {k} — {name}", { k, name:tierName(k) }),
        sub: `<span class="b t${k}">${k}</span>`,
        items: works.filter(w=>tierOf(w)===k).sort((a,b)=>(b.year||0)-(a.year||0)),
      }))
      .filter(g => g.items.length);
  }

  // Grouped by year, so the year is not repeated on every row and the
  // per-year count adds nothing; the other views keep both.
  const byYear = S.view === "chrono";
  return controls + groups.map(g => `
    <div class="grouphead">
      <h4>${esc(g.title)}</h4>${g.sub || ""}
      ${byYear ? "" : `<div class="gsp"></div><span class="c">${g.items.length}</span>`}
    </div>
    <div class="worklist ${byYear ? "no-yr" : ""}">${g.items.map(w => workRow(w, !byYear)).join("")}</div>
  `).join("");
}

function workRow(w, showYear = true){
  const link = w.doi ? "https://doi.org/" + w.doi : (w.landing || "");
  const co = !w.coauthors.length ? esc(t("sole author"))
    : esc(w.coauthors.slice(0, 3).join(", ")) + (w.coauthors.length > 3 ? ` +${w.coauthors.length - 3}` : "");
  const short = { "Web of Science":"WoS", "ERIH PLUS":"ERIH+" };
  const verdict = w.manualBadges.length
    ? `<span class="b ${w.manualSeed ? "seed" : "manual"}" title="${esc(w.manualSeed
        ? t("SROM seed list — not yet confirmed by you in Venues") : t("Your recorded verdict for this venue"))}: ${esc(w.manualBadges.join(", "))}">${
        esc(w.manualBadges.map(m => short[m] || m).join("·"))}</span>` : "";

  return `<div class="work ${w.retracted ? "flagged" : ""}" title="${esc(w.tierWhy.join(" · "))}">
    ${showYear ? `<div class="work-yr">${w.year || esc(t("n.d."))}</div>` : ""}
    <div>
      <div class="work-title">${link ? `<a href="${esc(link)}" target="_blank" rel="noopener">${esc(w.title)}</a>` : esc(w.title)}
        ${w.retracted ? `<span class="b bad">${esc(t("retracted"))}</span>` : ""}</div>
      <div class="work-venue">
        <span class="b tier t${tierOf(w)}">${tierOf(w)}</span>
        <em>${esc(venueLabel(w.venue))}</em>
        ${w.publisher && String(w.venueFrom).startsWith("crossref") ? `<span class="by" title="${esc(t("Parent record resolved via Crossref"))}">${esc(w.publisher)}</span>` : ""}
        ${w.volume ? `<span>${esc(w.volume)}${w.issue ? "(" + esc(w.issue) + ")" : ""}${w.pages ? ": " + esc(w.pages) : ""}</span>` : ""}
        ${verdict}
        ${w.doajSeal ? `<span class="b oa">${esc(t("DOAJ seal"))}</span>` : ""}
        ${w.oa ? `<span class="b oa">${esc(w.oaStatus)} OA</span>` : ""}
        ${w.relevant ? `<span class="b rel" title="${esc(w.relevanceWhy)}">${esc(t("Romani studies"))}</span>` : ""}
        ${w.indexedIn.map(i => `<span class="b idx">${esc(i)}</span>`).join("")}
        ${!w.doi ? `<span class="nodoi">${esc(t("no DOI"))}</span>` : ""}
        <span class="by">· ${co}${w.authorPos ? " · " + esc(t(w.authorPos)) : ""}</span>
      </div>
    </div>
    <div class="work-right">
      <span class="cit ${w.cites ? "" : "zero"}">${w.cites}</span><span class="cit-l">${esc(tw(w.cites, "citation"))}</span>
      ${w.fwci != null && w.cites ? `<div title="${esc(t("Field-Weighted Citation Impact"))}">FWCI ${w.fwci.toFixed(2)}</div>` : ""}
    </div>
  </div>`;
}

/* ---------- 12. Venues panel + registry ------------------------------ */
/* ERIH PLUS, Scopus, Web of Science and the Polish ministerial list have
   no open, CORS-accessible API. Rather than fake those lookups, the tool
   lets you record a verdict once per venue and reuses it for every
   scholar you evaluate afterwards. The registry is yours, exportable,
   and always labelled as an assertion rather than a retrieved fact. */

function renderVenues(){
  const rows = new Map();
  S.works.filter(w => !w.paratext).forEach(w => {
    const key = w.sourceId || w.venue;
    if (!rows.has(key))
      rows.set(key, { w, n:0, cites:0, years:[], rel:0 });
    const r = rows.get(key);
    r.n++; r.cites += w.cites;
    if (w.year) r.years.push(w.year);
    if (w.relevant) r.rel++;
  });

  const list = [...rows.values()].sort((a,b) =>
    tierRank(b.w) - tierRank(a.w) || b.n - a.n);

  return `
  <div class="note">${t("note.venues")}</div>
  <div class="scrollx"><table class="grid">
    <thead><tr>
      <th>${esc(t("Venue"))}</th><th>${esc(t("Type"))}</th><th>ISSN</th><th>${esc(t("Publisher"))}</th>
      <th class="num">${esc(t("Works"))}</th><th class="num">${esc(t("In field"))}</th><th class="num">${esc(t("Cites"))}</th>
      <th class="num">${esc(t("Years"))}</th><th>${esc(t("Automatic signals"))}</th><th>${esc(t("Your verdict"))}</th><th>${esc(t("Tier"))}</th>
    </tr></thead>
    <tbody>${list.map(venueRow).join("")}</tbody>
  </table></div>`;
}

function venueRow(r){
  const w = r.w;
  const src = w.sourceId ? S.sources.get(w.sourceId) : null;
  const { issn, rec } = registryFor(w);
  const auto = [];
  if (src?.is_in_doaj) auto.push(`<span class="b oa">DOAJ</span>`);
  const dj = doajFor(w);
  if (dj) auto.push(`<span class="b oa">DOAJ ✓</span>`);
  if (dj?.seal) auto.push(`<span class="b oa">${esc(t("seal"))}</span>`);
  if (src?.is_core) auto.push(`<span class="b idx">${esc(t("OA core"))}</span>`);
  if (src?.is_ojs) auto.push(`<span class="b idx">OJS</span>`);
  if (src?.is_preprint_repository) auto.push(`<span class="b idx">${esc(t("repository"))}</span>`);
  const h = src?.summary_stats?.h_index;
  if (h) auto.push(`<span class="b idx">h ${h}</span>`);

  const ys = r.years.length ? Math.min(...r.years) + "–" + Math.max(...r.years) : "—";
  const lookup = issn
    ? `https://kanalregister.hkdir.no/publiseringskanaler/erihplus/periodical/listing?query=${encodeURIComponent(issn)}`
    : null;

  const tgl = (field, label) => issn
    ? `<button class="togg ${rec?.[field]?"on":"off"}" data-issn="${esc(issn)}" data-field="${field}">${label}</button>`
    : "";

  return `<tr>
    <td><b>${esc(venueLabel(w.venue))}</b>
      ${src ? `<div class="vlinks"><a href="${esc(src.id)}" target="_blank" rel="noopener">OpenAlex</a>
        ${src.homepage_url?` · <a href="${esc(src.homepage_url)}" target="_blank" rel="noopener">${esc(t("homepage"))}</a>`:""}
        ${lookup?` · <a href="${esc(lookup)}" target="_blank" rel="noopener">${esc(t("check ERIH+"))}</a>`:""}
      </div>` : ""}</td>
    <td class="small2">${esc(typeName(src?.type || w.type))}</td>
    <td class="mono small3">${esc(issn || w.isbn?.[0] || "—")}</td>
    <td class="small2">${esc(w.publisher || "—")}</td>
    <td class="num">${r.n}</td>
    <td class="num">${r.rel}<div class="bar"><i style="width:${pct(r.rel,r.n)}%"></i></div></td>
    <td class="num">${num(r.cites)}</td>
    <td class="num small3">${esc(ys)}</td>
    <td>${auto.join(" ") || `<span class="muted small3">${esc(t("none"))}</span>`}</td>
    <td><div class="regfield">
      ${tgl("erih","ERIH+")} ${tgl("scopus","Scopus")} ${tgl("wos","WoS")}
      ${issn ? `<input type="text" placeholder="MEiN" value="${esc(rec?.mein || "")}"
                 data-issn="${esc(issn)}" data-field="mein" class="reg-mein">` : ""}
    </div></td>
    <td><span class="b t${tierOf(w)}">${tierOf(w)}</span></td>
  </tr>`;
}

/* ---------- 13. Identity panel --------------------------------------- */

/* How to reach a scholar — routes they have made public themselves.
   Addresses are not scraped from the web: on a public EU site, harvesting
   and republishing personal emails needs a lawful basis this tool does not
   have, and a browser cannot read arbitrary pages anyway. What a scholar
   published on ORCID, their institution's site and their own pages are
   theirs to have published; an address you already hold stays in your
   browser. */
function renderContact(){
  const P = S.orcid?.person || {};
  const emails = (P.emails?.email || []).map(e => e.email).filter(Boolean);
  const pinned = myPins().email;
  const pages = (P["researcher-urls"]?.["researcher-url"] || []).map(u => u.url?.value).filter(Boolean);
  if (S.wikidata?.ids?.website) pages.push(S.wikidata.ids.website);
  const host = u => { try { return new URL(u).hostname.replace(/^www\./, ""); } catch (e) { return u; } };
  const latest = S.works.filter(w => w.doi && !w.paratext).sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")))[0];
  const net = [["academia","Academia.edu"],["rg","ResearchGate"],["linkedin","LinkedIn"]]
    .map(([k, label]) => { const v = myPins()[k] || S.wikidata?.ids?.[k];
      const def = PINNABLE.find(d => d.key === k) || Object.values(WD_PROPS).find(d => d.key === k);
      return v && def ? `<a href="${esc(def.url(v))}" target="_blank" rel="noopener">${label}</a>` : ""; })
    .filter(Boolean);
  const orcid = orcidOf(S.author.orcid);

  const row = (k, v) => `<div class="contact-row"><div class="k">${esc(k)}</div><div class="v">${v}</div></div>`;
  return `<div class="card">
    <header><h3>${esc(t("How to reach them"))}</h3><div class="sp"></div>
      <span class="hdr-note">${esc(t("only routes the scholar made public"))}</span></header>
    <div class="body"><div class="contact-list">
      ${row(t("Email"), emails.length
          ? emails.map(e => `<a href="mailto:${esc(e)}">${esc(e)}</a>`).join("<br>") + `<small>${esc(t("published on their ORCID record"))}</small>`
          : pinned
            ? `<a href="mailto:${esc(pinned)}">${esc(pinned)}</a><small>${esc(t("recorded by you — kept in this browser only"))}</small>`
            : `<span class="muted">${esc(t("Not published on ORCID."))}</span><small>${esc(t("contact.noEmail"))}</small>`)}
      ${S.inst ? row(t("Institution"), `${esc(S.inst.name)}${S.inst.country ? " · " + esc(countryName(S.inst.country)) : ""}${S.inst.year ? ` <span class="muted">(${S.inst.year})</span>` : ""}
          ${S.inst.homepage ? `<br><a href="${esc(S.inst.homepage)}" target="_blank" rel="noopener">${esc(host(S.inst.homepage))}</a>` : ""}
          <small>${esc(t("most recent affiliation in the indexed record"))}</small>`) : ""}
      ${pages.length ? row(t("Own pages"), pages.slice(0, 5).map(u =>
          `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(host(u))}</a>`).join(" · ") + `<small>${esc(t("listed by the scholar on ORCID or Wikidata"))}</small>`) : ""}
      ${latest ? row(t("Latest paper"), `<a href="https://doi.org/${esc(latest.doi)}" target="_blank" rel="noopener">${esc(latest.title)}</a>
          <small>${latest.year || ""} · ${esc(t("journals usually print the corresponding author's email on the article"))}</small>`) : ""}
      ${net.length ? row(t("Messaging"), net.join(" · ") + `<small>${esc(t("profiles that accept messages"))}</small>`) : ""}
      ${orcid ? row("ORCID", `<a href="https://orcid.org/${esc(orcid)}" target="_blank" rel="noopener">orcid.org/${esc(orcid)}</a>`) : ""}
    </div></div>
  </div>`;
}

function renderIdentity(){
  const links = profileLinks();
  const resolved = links.filter(l => l.kind === "resolved");
  const inferred = links.filter(l => l.kind === "inferred");
  const pinned   = links.filter(l => l.kind === "pinned");
  const search   = links.filter(l => l.kind === "search");
  const pins = myPins();
  const cell = l => `<a class="linkcell ${l.kind}" href="${esc(l.url)}" target="_blank" rel="noopener">
      <span class="dot"></span><span>${esc(l.label)}<small>${esc(l.sub)}</small></span></a>`;

  let orcidMetrics = "";
  let orcidBlock = `<div class="empty">${esc(t("No ORCID on the OpenAlex profile, so no ORCID record could be retrieved."))}</div>`;
  if (S.orcid){
    const p = S.orcid.person || {};
    const act = S.orcid["activities-summary"] || {};
    const bio = p.biography?.content;
    const emp = affRows(act.employments);
    const edu = affRows(act.educations);
    const others = (p["other-names"]?.["other-name"] || []).map(o => o.content).filter(Boolean);
    const kw = (p.keywords?.keyword || []).map(k => k.content).filter(Boolean);
    const nWorks = orcidWorkCount();

    orcidMetrics = `
      <div class="metrics" style="border-bottom:1px solid var(--rule)">
        ${metric(num(nWorks), t("Works claimed"), t("on ORCID"))}
        ${metric(num(S.works.length), t("Works indexed"), t("on OpenAlex"))}
        ${metric(num(emp.length), t("Employments"), "")}
        ${metric(num(edu.length), t("Education"), "")}
        ${metric(num(S.reviews.length), t("Review venues"), "")}
      </div>`;
    orcidBlock = `
      ${others.length ? `<p class="orcid-p"><b>${esc(t("Other names:"))}</b> ${esc(others.join(" · "))}</p>` : ""}
      ${kw.length ? `<p class="orcid-p"><b>${esc(t("Self-declared keywords:"))}</b> ${esc(kw.join(" · "))}</p>` : ""}
      ${bio ? `<p class="orcid-bio">${esc(bio.slice(0,700))}${bio.length>700?"…":""}</p>` : ""}
      ${emp.length ? `<h4 class="orcid-h">${esc(t("Employment"))}</h4>${emp.join("")}` : ""}
      ${edu.length ? `<h4 class="orcid-h">${esc(t("Education"))}</h4>${edu.join("")}` : ""}`;
  }

  return `${renderContact()}
  <div class="card">
    <header><h3>${esc(t("Resolved identifiers"))}</h3><div class="sp"></div>
      <span class="legend"><span><i style="background:var(--ok)"></i>${esc(t("resolved — certain"))}</span>
      <span><i style="background:var(--warn)"></i>${esc(t("inferred from name — verify"))}</span>
      <span><i style="background:var(--tD)"></i>${esc(t("pinned by you"))}</span>
      <span><i style="background:var(--warn)"></i>${esc(t("search"))}</span></span>
    </header>
    <div class="body">
      <div class="linkgrid">${resolved.concat(inferred, pinned).map(cell).join("")}</div>
      ${inferred.length ? `<div class="note warn-edge" style="margin:9px 0 0">
        ${t("id.inferred", { count:esc(tn(inferred.length, "identifier")), verb:inferred.length > 1 ? "were" : "was" })}
      </div>` : ""}
      ${S.wikidata ? `<div class="note" style="margin:9px 0 0">
        ${t(S.wikidata.matchedBy === "ORCID" ? "id.wd.orcid" : "id.wd.name", { id:esc(S.wikidata.id) })}
        ${Object.keys(S.wikidata.ids).length ? esc(t("id.wd.hub")) : t("id.wd.noIds")}
      </div>` : `<div class="note" style="margin:9px 0 0">${esc(t("id.noWd"))}</div>`}
    </div>
  </div>

  <div class="card">
    <header><h3>${esc(t("Pin identifiers by hand"))}</h3><div class="sp"></div>
      <span class="hdr-note">${esc(t("saved locally, exports with the dossier"))}</span>
    </header>
    <div class="body">
      <div class="note" style="margin-bottom:9px">${t("id.pinNote")}</div>
      ${PINNABLE.map(d => `<div class="pinrow">
        <label>${esc(t(d.label))}</label>
        <input type="text" class="pin-in" data-key="${d.key}"
               value="${esc(pins[d.key] || "")}" placeholder="${esc(t(d.ph))}">
      </div>`).join("")}
    </div>
  </div>

  ${search.length ? `<div class="card">
    <header><h3>${esc(t("Search these manually"))}</h3></header>
    <div class="body">
      <div class="note" style="margin-bottom:9px">${esc(t("id.searchNote"))}</div>
      <div class="linkgrid">${search.map(cell).join("")}</div>
    </div>
  </div>` : ""}
  <div class="card">
    <header><h3>${esc(t("ORCID record"))}</h3>
      ${S.author.orcid?`<div class="sp"></div><a href="${esc(S.author.orcid)}" target="_blank" rel="noopener" class="hdr-link">${esc(t("open on orcid.org →"))}</a>`:""}
    </header>
    ${orcidMetrics}<div class="body">${orcidBlock}</div>
  </div>`;
}

function affRows(block){
  const out = [];
  for (const g of (block?.["affiliation-group"] || [])){
    for (const s of (g.summaries || [])){
      const v = s["employment-summary"] || s["education-summary"] || s["qualification-summary"];
      if (!v) continue;
      const org = v.organization?.name || "—";
      const city = [v.organization?.address?.city, v.organization?.address?.country]
                     .filter(Boolean).join(", ");
      const sy = v["start-date"]?.year?.value;
      const ey = v["end-date"]?.year?.value;
      const span = sy ? sy + "–" + (ey || t("present")) : (ey || "");
      out.push(`<div class="aff-row">
        <span class="aff-yr">${esc(span || "—")}</span>
        <span><b>${esc(v["role-title"] || "—")}</b>, ${esc(org)}
        ${city?`<span class="muted"> · ${esc(city)}</span>`:""}
        ${v["department-name"]?`<div class="muted small2">${esc(v["department-name"])}</div>`:""}
        </span></div>`);
    }
  }
  return out;
}

/* ---------- 14. Peer review + flags ---------------------------------- */

function renderReviews(){
  if (!S.reviews.length)
    return `<div class="card"><div class="empty">${t("rev.none")}</div></div>`;

  const total = S.reviews.reduce((a,b)=>a+b.count,0);
  return `
  <div class="note">${t("rev.note", { reviews:esc(tn(total, "review")), venues:esc(tn(S.reviews.length, "venue")) })}</div>
  <div class="scrollx"><table class="grid">
    <thead><tr><th>${esc(t("Venue reviewed for"))}</th><th>ISSN</th><th class="num">${esc(t("Reviews"))}</th><th>${esc(t("Years"))}</th><th>${esc(t("In field"))}</th></tr></thead>
    <tbody>${S.reviews.map(r => {
      const src = r.sourceId ? S.sources.get(r.sourceId) : null;
      const rel = inLexicon(r.name);
      const ys = r.years.length ? Math.min(...r.years) + "–" + Math.max(...r.years) : "—";
      return `<tr>
        <td><b>${esc(r.name === "Undisclosed venue" ? t(r.name) : r.name)}</b>${src?.host_organization_name
             ? `<div class="muted small3">${esc(src.host_organization_name)}</div>`:""}</td>
        <td class="mono small3">${esc(r.issn||"—")}</td>
        <td class="num">${r.count}</td>
        <td class="mono small3">${esc(ys)}</td>
        <td>${rel?`<span class="b rel">${esc(t("Romani studies"))}</span>`:'<span class="muted">—</span>'}</td>
      </tr>`;
    }).join("")}</tbody>
  </table></div>`;
}

function renderFlags(){
  const flags = computeFlags(computeSummary());
  return `<div class="note">${esc(t("flags.note"))}</div>
  <div class="card">${flags.map(f => `
    <div class="flag sev-${f.sev}">
      <div class="ic">${f.ic}</div>
      <div><b>${esc(f.t)}</b><p>${esc(f.d)}</p></div>
    </div>`).join("")}</div>`;
}

/* ---------- 15. Shell: tabs and wiring -------------------------------- */

const TABS = [
  { id:"record",   label:"Publication record", count:() => S.works.filter(w=>!w.paratext).length, render:renderRecord },
  { id:"venues",   label:"Venues & indexing",  count:() => new Set(S.works.map(w=>w.sourceId||w.venue)).size, render:renderVenues },
  { id:"identity", label:"Identity & profiles",count:() => null, render:renderIdentity },
  { id:"reviews",  label:"Peer review",        count:() => S.reviews.length || null, render:renderReviews },
  { id:"flags",    label:"Editorial notes",    count:() => null, render:renderFlags },
];

function renderShell(){
  CHECK.stage = "dossier";
  $("#view-check").classList.add("in-dossier");
  $("#stage").innerHTML =
    renderDossier() +
    `<div class="tabs">${TABS.map(tb => {
      const c = tb.count();
      return `<button class="tab ${S.tab===tb.id?"on":""}" data-tab="${tb.id}">${esc(t(tb.label))}${c?`<span class="n">${c}</span>`:""}</button>`;
    }).join("")}</div>
    <div id="panel" class="panel on"></div>`;
  renderPanel();
  $$("#stage .tab").forEach(b => b.onclick = () => { S.tab = b.dataset.tab; renderShell(); });
  const em = $("#stage .exp-more");
  if (em) em.ontoggle = () => { S.expMore = em.open; };

  const save = $("#btnSave");
  if (save) save.onclick = libToggleSave;
  const up = $("#btnUpdate");
  if (up) up.onclick = () => loadAuthor(S.author, { fresh:true });
  const an = $("#btnAddNote");
  if (an) an.onclick = () => { S.noteOpen = true; renderShell(); $("#libNote")?.focus(); };
  const sh = $("#btnShare");
  if (sh) sh.onclick = () => shareLink(S.author.display_name + " — Scholar Audit");
  const ex = $("#btnExport");
  if (ex) ex.onclick = exportDossier;

  $$("#stage .fchip[data-folder]").forEach(b => b.onclick = async () => {
    const on = !b.classList.contains("on");
    b.classList.toggle("on", on);
    await libSetFolder(shortId(S.author.id), b.dataset.folder, on);
  });

  const nf = $("#btnNewFolderInline");
  if (nf) nf.onclick = async () => {
    const f = await newFolder();
    if (!f) return;
    await libSetFolder(shortId(S.author.id), f.id, true);
    renderShell();
  };

  const note = $("#libNote");
  if (note){
    let tm;
    note.addEventListener("input", () => {
      clearTimeout(tm);
      tm = setTimeout(async () => {
        const rec = LIB.scholars[shortId(S.author.id)];
        if (rec){ rec.note = note.value; await libSave(); }
      }, 450);
    });
  }
}

function renderPanel(){
  const tab = TABS.find(tb => tb.id === S.tab) || TABS[0];
  $("#panel").innerHTML = tab.render();
  wirePanel();
}

function wirePanel(){
  // Record filters
  const on = (sel, ev, fn) => { const el = $(sel); if (el) el.addEventListener(ev, fn); };
  $$("#viewSeg button").forEach(b => b.onclick = () => { S.view = b.dataset.view; renderPanel(); });
  on("#fFrom","change", e => { S.filters.from = e.target.value ? +e.target.value : null; renderPanel(); });
  on("#fTo","change",   e => { S.filters.to   = e.target.value ? +e.target.value : null; renderPanel(); });
  on("#fType","change", e => { S.filters.type = e.target.value; renderPanel(); });
  on("#fTier","change", e => { S.filters.tier = e.target.value; renderPanel(); });
  on("#fVenue","change",e => { S.filters.venue= e.target.value; renderPanel(); });
  on("#fField","change",e => { S.filters.fieldOnly = e.target.checked; renderPanel(); });
  on("#fOA","change",   e => { S.filters.oaOnly    = e.target.checked; renderPanel(); });

  const ft = $("#fText");
  if (ft){
    let timer;
    ft.addEventListener("input", e => {
      clearTimeout(timer);
      const v = e.target.value;
      timer = setTimeout(() => {
        S.filters.text = v;
        renderPanel();
        const el = $("#fText");
        if (el){ el.focus(); el.setSelectionRange(el.value.length, el.value.length); }
      }, 220);
    });
  }

  // Venue registry edits — re-score, because a verdict changes every tier.
  $$(".togg[data-issn]").forEach(b => b.onclick = () => {
    const { issn, field } = b.dataset;
    const rec = S.registry[issn] || (S.registry[issn] = {});
    rec[field] = !rec[field];
    delete rec.seeded;
    saveRegistry();
    S.works.forEach(scoreWork);
    renderShell();
  });
  $$(".pin-in").forEach(i => i.onchange = () => {
    const id = shortId(S.author?.id);
    if (!id) return;
    const rec = S.pins[id] || (S.pins[id] = {});
    const v = i.value.trim();
    if (v) rec[i.dataset.key] = v; else delete rec[i.dataset.key];
    if (!Object.keys(rec).length) delete S.pins[id];
    savePins();
    renderPanel();
  });

  $$(".reg-mein").forEach(i => i.onchange = () => {
    const { issn, field } = i.dataset;
    const rec = S.registry[issn] || (S.registry[issn] = {});
    rec[field] = i.value.trim();
    delete rec.seeded;
    saveRegistry();
    S.works.forEach(scoreWork);
    renderShell();
  });
}

/* ---------- 16. Search flow ------------------------------------------ */

function setErr(msg){
  $("#err").innerHTML = msg ? `<div class="err">${esc(msg)}</div>` : "";
}
function setStage(html){ $("#view-check").classList.remove("in-dossier"); $("#stage").innerHTML = html; }
function progress(msg){
  CHECK.stage = "progress";
  setStage(`<div class="card"><div class="progress">
    <span class="spinner"></span> ${esc(t("Building dossier"))}
    <div class="step">${esc(msg)}</div></div></div>`);
}
/** A message in place of a dossier — kept as a function so it can be redrawn. */
function stageMessage(render){
  CHECK.stage = "message"; CHECK.render = render;
  setStage(render());
}

/** The Check view with nothing open: the other tools, and the scholars you
    opened recently, one tap away. */
function renderCheckLanding(){
  CHECK.stage = "landing";
  S.author = null;
  const recent = DC.index.slice(0, 8);
  setStage(`
  <div class="landing">
    ${recent.length ? `<div class="recent">
      <span class="eyebrow">${esc(t("Recently opened"))}</span>
      ${recent.map(e => `<button class="fchip" data-open="${esc(e.id)}" title="${esc(t("Stored copy"))} · ${esc(ageText(e.at))}">${esc(e.name)}</button>`).join("")}
    </div>` : ""}
    <div class="guide">
      <a class="guide-card" href="?tool=reviewers" data-go="reviewers">
        <span class="eyebrow">${esc(t("Find reviewers"))}</span>
        <b>${esc(t("guide.reviewers.t"))}</b><span>${esc(t("guide.reviewers.d"))}</span></a>
      <a class="guide-card" href="?tool=directory" data-go="directory">
        <span class="eyebrow">${esc(t("Field directory"))}</span>
        <b>${esc(t("guide.directory.t"))}</b><span>${esc(t("guide.directory.d"))}</span></a>
      <a class="guide-card" href="?tool=library" data-go="library">
        <span class="eyebrow">${esc(t("Library"))}</span>
        <b>${esc(t("guide.library.t"))}</b><span>${esc(t("guide.library.d"))}</span></a>
    </div>
  </div>`);
  $$("#stage [data-open]").forEach(b => b.onclick = () => openScholar(b.dataset.open));
  $$("#stage [data-go]").forEach(a => a.onclick = e => { e.preventDefault(); showView(a.dataset.go); });
}

/** Open a scholar's dossier from anywhere in the app. */
function openScholar(id){
  $("#q").value = id;     // exact; a name-matched ORCID could open someone else
  runSearch();
}

async function runSearch(){
  const q = $("#q").value.trim();
  if (!q) return;
  showView("check");
  setErr("");
  $("#btnSearch").disabled = true;

  try {
    const stored = await openStored(dcEntry(q));
    if (stored) return;
    progress(t("Resolving identity…"));
    const res = await resolveQuery(q);

    if (res.kind === "none"){
      stageMessage(() => `<div class="card"><div class="empty">${t("search.none", { q:esc(q) })}</div></div>`);
      return;
    }

    if (res.kind === "orcid-only"){
      stageMessage(() => `<div class="card"><div class="empty">${t("search.orcidOnly", { orcid:esc(res.orcid) })}</div></div>`);
      return;
    }

    if (res.kind === "candidates"){
      S.candidateCount = res.list.length;
      await renderCandidates(res.list);
      return;
    }

    S.candidateCount = 1;
    await loadAuthor(res.author);

  } catch (e){
    setErr(t("Lookup failed: {msg}", { msg:e.message }) + "  — " +
      t("if this persists, the API may be rate-limiting; wait a moment and retry."));
    renderCheckLanding();
  } finally {
    $("#btnSearch").disabled = false;
  }
}

async function renderCandidates(list){
  CHECK.stage = "candidates";
  CHECK.cands = { list, counts:null };
  drawCandidates();
  // The field count is what makes this list decidable at a glance.
  const counts = await Promise.all(list.map(a => fieldCountFor(a.id).catch(() => 0)));
  if (CHECK.cands?.list !== list) return;
  CHECK.cands.counts = counts;
  drawCandidates();
}

function drawCandidates(){
  const { list, counts } = CHECK.cands;
  setStage(`<div class="card">
    <header><h3>${esc(t("{profiles} match this name — choose one", { profiles:tn(list.length, "profile") }))}</h3></header>
    <div id="cands">${!counts ? `<div class="progress"><span class="spinner"></span> ${esc(t("Counting field output…"))}</div>` :
      list.map((a, i) => {
        const inst = a.last_known_institutions?.[0]?.display_name
                  || a.affiliations?.[0]?.institution?.display_name || t("No affiliation recorded");
        const orcid = orcidOf(a.orcid);
        return `<div class="cand" data-i="${i}" tabindex="0" role="button">
          <div>
            <div class="cand-name">${esc(a.display_name)}</div>
            <div class="cand-meta">
              ${orcid ? `<span class="idchip verified tight">ORCID ${esc(orcid)}</span>` : `<span class="idchip tight">${esc(t("no ORCID"))}</span>`}
              <span>${esc(inst)}</span>
              ${counts[i] ? `<span class="b rel">${esc(t("{n} in Romani studies", { n:counts[i] }))}</span>` : ""}
            </div>
          </div>
          <div class="cand-nums">
            <b>${num(a.works_count)}</b> ${esc(tw(a.works_count, "work"))}<br>
            <b>${num(a.cited_by_count)}</b> ${esc(tw(a.cited_by_count, "citation"))} · h ${a.summary_stats?.h_index ?? "—"}
          </div>
        </div>`;
      }).join("")}</div>
  </div>
  <div class="note">${esc(t("cand.note"))}</div>`);

  $$("#cands .cand").forEach(el => {
    el.onclick = () => loadAuthor(list[+el.dataset.i]);
    el.onkeydown = e => { if (e.key === "Enter") el.click(); };
  });
}

/** Opens a stored dossier if there is one and the chosen mode allows.
    Resolves "opened", "cancelled" (dialog dismissed), or null (go to the network). */
async function openStored(entry){
  if (!entry || DC.mode === "fresh") return null;
  if (DC.mode === "ask"){
    const k = await choose({ title:entry.name,
      text:t("A stored copy of this dossier exists, from {when} ({age}).", { when:fmtWhen(entry.at), age:ageText(entry.at) }),
      choices:[
        { value:"stored", label:t("Open the stored copy"), sub:t("instant — no requests to any service") },
        { value:"fresh",  label:t("Fetch fresh data"), sub:t("about a hundred requests; up to half a minute") },
      ] });
    if (k === null) return "cancelled";
    if (k === "fresh") return null;
  }
  const snap = await dcGet(entry.id);
  if (!snap) return null;
  dcRestore(snap);
  showDossier();
  return "opened";
}

function showDossier(){
  showView("check");
  setAddress({ q: (!S.orcidInferred && orcidOf(S.author.orcid)) || shortId(S.author.id) }, "check");
  S.tab = "record";
  S.noteOpen = false;
  S.filters = { text:"", from:null, to:null, type:"", tier:"", venue:"", oaOnly:false, fieldOnly:false };
  renderShell();
  libRefreshFromDossier();
  window.scrollTo({ top:0, behavior:"smooth" });
}

async function loadAuthor(author, { fresh = false } = {}){
  setErr("");
  showView("check");
  if (!fresh){
    const r = await openStored(dcEntry(shortId(author.id)));
    if (r) return;
  } else {
    cache.clear();                      // past this session's response cache too
  }
  try {
    // Candidate objects from a search are complete enough, but a direct
    // fetch guarantees the full affiliation history.
    let full = await getJSON(oa("/authors/" + shortId(author.id)), { optional:true }) || author;
    // Whichever profile was picked, lead with the largest one sharing its
    // ORCID and pull in the works of the rest.
    const prof = await orcidProfiles(orcidOf(full.orcid));
    let siblings = [];
    if (prof.length > 1){
      if (shortId(prof[0].id) !== shortId(full.id))
        full = await getJSON(oa("/authors/" + shortId(prof[0].id)), { optional:true }) || prof[0];
      siblings = prof.filter(x => shortId(x.id) !== shortId(full.id));
    }
    await buildDossier(full, progress, siblings);
    await dcPut();
    showDossier();
  } catch (e){
    setErr(t("Could not build the dossier: {msg}", { msg:e.message }));
    renderCheckLanding();
  }
}

/** Redraw whatever the Check view shows — after a language switch. */
function redrawCheck(){
  if (CHECK.stage === "dossier" && S.author){ S.works.forEach(scoreWork); renderShell(); }
  else if (CHECK.stage === "candidates" && CHECK.cands) drawCandidates();
  else if (CHECK.stage === "message" && CHECK.render) setStage(CHECK.render());
  else if (CHECK.stage === "landing") renderCheckLanding();
}

/* ---------- 17. Export ------------------------------------------------ */

async function exportDossier(){
  if (!S.author) return toast(t("Evaluate a scholar first — there is nothing to export yet."));
  const k = await choose({ title:t("Export {name}", { name:S.author.display_name }), choices:[
    { value:"json", label:t("Full dossier (JSON)"), sub:t("metrics, expertise, notes, every work with its rationale, identifiers") },
    { value:"csv",  label:t("Publication list (CSV)"), sub:t("one row per work — opens in Excel") },
    { value:"ris",  label:t("Publication list (RIS)"), sub:t("imports into Zotero, EndNote, Mendeley") },
    { value:"print",label:t("Print or save as PDF"), sub:t("the dossier as it stands on screen") },
  ] });
  if (k === "csv") download(`srom-audit-${slug()}.csv`, toCSV(), "text/csv;charset=utf-8");
  else if (k === "ris") download(`srom-audit-${slug()}.ris`, toRIS(), "application/x-research-info-systems");
  else if (k === "print") window.print();
  else if (k === "json") download(`srom-audit-${slug()}.json`, JSON.stringify(exportPayload(), null, 2), "application/json");
}

function exportPayload(){
  const sm = computeSummary();
  return {
    generated: new Date().toISOString(),
    tool: "SROM Scholar Audit",
    language: I18N.lang,
    sources: ["OpenAlex", "ORCID", "Crossref", "DOAJ", "Wikidata", "Semantic Scholar"],
    scholar: {
      name: S.author.display_name,
      openalex: S.author.id,
      orcid: S.author.orcid || (S.orcidInferred && S.orcid
        ? "https://orcid.org/" + S.orcid["orcid-identifier"]?.path : null),
      orcidMatchedByName: !!S.orcidInferred,
      wikidata: S.wikidata
        ? { id:S.wikidata.id, description:S.wikidata.description,
            matchedBy:S.wikidata.matchedBy, identifiers:S.wikidata.ids }
        : null,
      semanticScholar: S.s2 || null,
      pinnedIdentifiers: myPins(),
      profileLinks: profileLinks().map(l => ({ source:l.kind, label:l.label, url:l.url })),
      affiliations: (S.author.affiliations || []).map(a => ({
        institution: a.institution?.display_name,
        country: a.institution?.country_code,
        ror: a.institution?.ror,
        years: a.years,
      })),
    },
    summary: sm,
    expertise: (() => {
      const x = computeExpertise();
      const pack = list => list.map(r => ({
        theme:themeName(r.id), works:r.n, share:+(r.share*100).toFixed(1),
        citations:r.cites, firstYear:r.first, lastYear:r.last, recentWorks:r.recent,
      }));
      return {
        headline: expertiseHeadline(x, sm),
        inFieldWorks: x.total,
        core: pack(x.core), secondary: pack(x.secondary), peripheral: pack(x.peripheral),
        machineTopics: x.topics,
      };
    })(),
    flags: computeFlags(sm).map(f => ({ severity:f.sev, note:f.t, detail:f.d })),
    peerReview: S.reviews,
    works: S.works.filter(w => !w.paratext).map(w => ({
      year:w.year, title:w.title, venue:w.venue, issn:w.issn, publisher:w.publisher,
      type:w.type, doi:w.doi ? "https://doi.org/" + w.doi : null,
      tier:w.tier, tierRationale:w.tierWhy, indexedIn:w.indexedIn,
      openAccess:w.oa ? w.oaStatus : null, citations:w.cites, fwci:w.fwci,
      inField:w.relevant, fieldEvidence:w.relevanceWhy,
      authorPosition:w.authorPos, authors:w.nAuthors, retracted:w.retracted,
    })),
    venueRegistry: S.registry,
  };
}

function toCSV(){
  const cols = ["year","title","venue","issn","publisher","type","tier","tier_rationale",
                "doi","indexed_in","open_access","citations","fwci","in_field","field_evidence",
                "author_position","n_authors","retracted"];
  const rows = S.works.filter(w=>!w.paratext)
    .sort((a,b)=>(b.year||0)-(a.year||0))
    .map(w => [
      w.year, w.title, w.venue, w.issn, w.publisher, w.type, w.tier, w.tierWhy.join("; "),
      w.doi ? "https://doi.org/" + w.doi : "", w.indexedIn.join(";"),
      w.oa ? w.oaStatus : "", w.cites, w.fwci ?? "", w.relevant ? "yes" : "no",
      w.relevanceWhy, w.authorPos, w.nAuthors, w.retracted ? "yes" : "",
    ].map(csvCell).join(","));
  return "﻿" + cols.join(",") + "\n" + rows.join("\n");
}

/** RIS for reference managers (Zotero, EndNote, Mendeley). */
function toRIS(){
  const TY = { "article":"JOUR", "review":"JOUR", "letter":"JOUR", "editorial":"JOUR", "book-chapter":"CHAP",
               "book":"BOOK", "dissertation":"THES", "preprint":"UNPB", "report":"RPRT", "dataset":"DATA" };
  const nm = n => { const p = String(n).trim().split(/\s+/); return p.length > 1 ? p.pop() + ", " + p.join(" ") : n; };
  const line = (k, v) => v ? `${k}  - ${String(v).replace(/[\r\n]+/g, " ")}\r\n` : "";
  return S.works.filter(w => !w.paratext).sort((a, b) => (b.year||0) - (a.year||0)).map(w => {
    const [sp, ep] = String(w.pages || "").split(/[–-]/);
    return line("TY", TY[w.type] || "GEN")
      + (w.authors.length ? w.authors : [S.author.display_name]).map(a => line("AU", nm(a))).join("")
      + line("TI", w.title)
      + line(w.type === "book-chapter" ? "T2" : "JO", w.venue !== NO_VENUE ? w.venue : "")
      + line("PY", w.year) + line("DA", w.date) + line("VL", w.volume) + line("IS", w.issue)
      + line("SP", sp) + line("EP", ep) + line("PB", w.publisher)
      + line("SN", w.issn || w.isbn?.[0]) + line("LA", w.lang)
      + line("DO", w.doi) + line("UR", w.doi ? "https://doi.org/" + w.doi : w.landing)
      + "ER  - \r\n";
  }).join("\r\n");
}

function slug(){
  return (S.author?.display_name || "scholar")
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-zA-Z0-9]+/g, "-").replace(/^-|-$/g, "").toLowerCase();
}
