"use strict";

/* =====================================================================
   Find reviewers — for a manuscript, the people who publish on the same
   thing, ranked by how closely and how recently, with conflicts of
   interest checked against the manuscript's authors.

   Confidentiality. The title and abstract stay in the browser: key terms
   are picked out here, and only those terms are sent to OpenAlex, as a
   search. The authors' names or ORCIDs are sent too, to look up their
   co-authors and institutions. Nothing is saved — leave the page and the
   manuscript is gone.

   What the conflict check can see: co-authorship and shared institutions
   in the indexed record. What it cannot: supervision, friendship, joint
   grants, rivalry. It narrows the list; reviewers still declare.
   ===================================================================== */

const RV = {
  f: { title:"", abstract:"", keywords:"", authors:"", years:"10", coi:"5", otherCountries:false, hideThin:true },
  terms: [], termsFor: "",   // [{ text, forms, on, src }] and the text they were picked from
  themes: [],                // theme ids the manuscript touches
  people: [], peopleFor: "", // the manuscript's authors, resolved, and the text they came from
  cands: [],                 // ranked candidates
  worksN: 0,
  status: "idle",            // idle | running | done | error
  step: "", error: "",
  excluded: new Set(),
  selected: new Set(),
  showAside: false,
  shown: 25,
  runId: 0,
  enrich: new Map(),         // ORCID → { emails, venues } | "loading"
};

/* ---------- Key terms ------------------------------------------------- */

const STOP = new Set((
  // English
  "a about above across after again against all almost along also although always am among an and another any are around " +
  "as at be because been before being below between both but by can cannot could did do does doing done down during each " +
  "either else even ever every few for from further had has have having he her here hers him his how however i if in into " +
  "is it its itself just less made make many may me might more most much must my neither no nor not now of off often on " +
  "once one only onto or other others our out over own per perhaps rather same several shall she should since so some such " +
  "than that the their them themselves then there therefore these they this those though through throughout thus to too " +
  "toward towards under until up upon us very via was we well were what when where whereas whether which while who whom " +
  "whose why will with within without would yet you your " +
  // academic boilerplate
  "abstract article articles paper papers study studies research analysis analyses analyse analyze analysed analyzed " +
  "analysing analyzing based result results finding findings discuss discusses discussed discussing argue argues argued " +
  "examine examines examined examining explore explores explored exploring approach approaches data case cases context " +
  "contexts aspect aspects issue issues role roles new use uses used using particular particularly author authors chapter " +
  "chapters text texts focus focuses focused focusing show shows showed shown present presents presented provide provides " +
  "provided aim aims aimed work works first second third two three four different various main number part parts general " +
  "specific special important significant key recent current way ways order related relation relations concerning " +
  "regarding terms term including include includes included especially mainly indeed given contribution contributes " +
  "contribute demonstrate demonstrates suggest suggests offer offers offered consider considers considered question " +
  "questions problem problems process processes level levels form forms type types example examples period time times " +
  "year years today century centuries within among across " +
  // Polish
  "aby ale albo ani aż bardzo bez bo bowiem by być był była było byli były będzie będą czy czyli dla do dwa dwie gdy gdyż " +
  "gdzie go ich im inne inny innych jak jaka jaki jakie jako je jego jej jest jeszcze jeśli jeżeli już ją każdy kiedy kto " +
  "która które którego której który których którym którzy lub ma mają mi między mnie może można na nad nam nas nie nich " +
  "niej nim niż od oraz po pod podczas ponad ponieważ poprzez przed przez przy również się sobie sposób są ta tak także tam " +
  "te tego tej ten to tu tych tylko tym tymi tę we więc wszystko wśród za zaś że żeby jednak natomiast według wobec dzięki " +
  "wraz temu artykuł artykule artykułu tekst tekście tekstu autor autora autorka autorki autorzy badanie badania badań " +
  "badaniach analiza analizy analizie analizę celem cel praca pracy pracę przykład przykładzie przykładu kontekst " +
  "kontekście problem problemu problematyka problematyki wyniki wyników rola roli ramach szczególnie zwłaszcza sytuacji " +
  "sytuacja kwestii kwestia kwestie aspekt aspekty aspektów okres okresie czasie roku wieku wieków część części sprawa " +
  "spraw sprawy " +
  // German, French, Spanish — the commonest function words
  "der die das und zu den von mit des sich im nicht ist ein eine einer als auch auf für dem aus bei nach über um wie zur " +
  "zum le la les du de et en un une dans pour sur par au aux est qui que ce ces son sa ses il elle el los las del y por " +
  "para con una se lo"
).split(/\s+/).filter(Boolean));

/* Words that name the field itself: in every in-field work, so as search
   terms they rank nothing. The in-field filter does their job. */
const FIELD_WORD = /^(roma|romani|romany|romanies|rroma|roms?|romów|romowie|romom|romami|romach|romsk\p{L}*|cyga[nń]\p{L}*|gyps\p{L}*|sinti|traveller?s?|zigeuner\p{L}*|tsigan\p{L}*|tzigan\p{L}*|gitan\p{L}*)$/u;
const isFieldWord = w => FIELD_WORD.test(w);

const SUFFIXES = ["ościach","ościami","ations","ation","ności","ność","ością","ities","ments","ings","ions","ment","ness",
  "ists","isms","ity","ism","ist","ing","ion","ies","ied","ers","ach","ami","owie","ego","emu","ych","ymi","ich","imi",
  "iej","ów","om","ej","ym","ią","ie","ed","es","er","al","ly","s","ę","ą","a","y","i","u","o","e"];
/** A light stem, only to count "school", "schools" and "schooling" as one term. */
function stem(w){
  if (w.length <= 5) return w;
  for (const s of SUFFIXES) if (w.endsWith(s) && w.length - s.length >= 4) return w.slice(0, -s.length);
  return w;
}

/** Sentence-ish segments of lower-case words, so no pair spans a full stop. */
function segments(text){
  return String(text || "").toLowerCase().replace(/[’`]/g, "'")
    .split(/[.!?;:()[\]{}"“”„«»\n\r\t•·–—]+/)
    .map(seg => (seg.match(/\p{L}[\p{L}'-]*\p{L}|\p{L}/gu) || []).map(w => w.replace(/'s$/, "")));
}
const usable = w => w && w.length >= 4 && !STOP.has(w) && !isFieldWord(w) && !/\d/.test(w);

/** Pick the terms that characterise a manuscript: your keywords first, then
    word pairs that recur or sit in the title, then single words weighted by
    frequency and by appearing in the title. */
function extractTerms({ title, abstract, keywords }){
  const uni = new Map(), bi = new Map();
  const feed = (text, weight, inTitle) => {
    for (const seg of segments(text)){
      seg.forEach((w, i) => {
        if (!usable(w)) return;
        const k = stem(w);
        const g = uni.get(k) || { forms:new Map(), score:0, n:0, inTitle:false };
        g.forms.set(w, (g.forms.get(w) || 0) + 1);
        g.score += weight * (w.length >= 8 ? 1.2 : 1); g.n++; g.inTitle ||= inTitle;
        uni.set(k, g);
        const v = seg[i + 1];
        if (usable(v)){
          const bk = k + " " + stem(v);
          const b = bi.get(bk) || { forms:new Map(), score:0, n:0, inTitle:false };
          b.forms.set(w + " " + v, (b.forms.get(w + " " + v) || 0) + 1);
          b.score += weight * 2.2; b.n++; b.inTitle ||= inTitle;
          bi.set(bk, b);
        }
      });
    }
  };
  feed(title, 3, true);
  feed(abstract, 1, false);

  const top = forms => [...forms.entries()].sort((a, b) => b[1] - a[1] || a[0].length - b[0].length).map(([f]) => f);
  const out = [];
  const seen = new Set();
  const push = (text, forms, src, on) => {
    const k = text.toLowerCase();
    if (seen.has(k)) return;
    seen.add(k);
    out.push({ text, forms, src, on });
  };

  for (const k of String(keywords || "").split(/[,;\n]+/).map(s => s.trim()).filter(s => s.length >= 3).slice(0, 6))
    push(k, [k.toLowerCase()], "kw", true);

  const pairs = [...bi.values()].filter(b => b.n >= 2 || b.inTitle).sort((a, b) => b.score - a.score).slice(0, 4);
  pairs.forEach(b => push(top(b.forms)[0], top(b.forms).slice(0, 2), "auto", true));

  const inPairs = w => pairs.reduce((a, b) => a + ([...b.forms.keys()].some(f => f.split(" ").includes(w)) ? b.n : 0), 0);
  const singles = [...uni.values()]
    .filter(g => g.n - inPairs(top(g.forms)[0]) > 0 || g.inTitle)
    .sort((a, b) => b.score - a.score);
  let on = out.filter(x => x.on).length;
  for (const g of singles){
    if (out.length >= 14) break;
    const f = top(g.forms);
    const strong = on < 8 && (g.score >= 2 || on < 4);
    push(f[0], f.slice(0, 3), "auto", strong);
    if (strong) on++;
  }
  return out;
}

const quoteForm = f => /[^\p{L}]/u.test(f) ? `"${f.replace(/"/g, "")}"` : f;
function termQuery(){
  return RV.terms.filter(x => x.on).map(x => {
    const forms = x.forms.slice(0, 3).map(quoteForm);
    return forms.length > 1 ? "(" + forms.join(" OR ") + ")" : forms[0];
  }).join(" OR ");
}

/* ---------- Search and ranking --------------------------------------- */

const RV_SELECT = "id,title,display_name,publication_year,authorships,relevance_score,primary_location,doi";

async function searchWorks(){
  const since = RV.f.years === "any" ? null : THIS_YEAR - (+RV.f.years || 10);
  const filter = [since ? `from_publication_date:${since}-01-01` : null, "is_paratext:false",
                  "topics.id:" + FIELD.topicIds.join("|")].filter(Boolean).join(",");
  const search = "(" + termQuery() + ")";
  // Inside the field's topic only. OpenAlex does not honour AND between OR
  // groups, so a "Roma AND school" search outside the topic returns any work
  // on schools — robotics and hotel chatbots included — and was dropped.
  const [p1, p2] = await Promise.all([
    getJSON(oa("/works", { filter, search, per_page:200, page:1, select:RV_SELECT })),
    getJSON(oa("/works", { filter, search, per_page:200, page:2, select:RV_SELECT }), { optional:true }),
  ]);
  // Both pages are scored against page one's best match.
  const max = Math.max(1e-9, ...(p1?.results || []).map(w => w.relevance_score || 0));
  return [...(p1?.results || []), ...(p2?.results || [])].map(w => ({ w, rel:(w.relevance_score || 0) / max }));
}

/** Everyone who wrote the matching works, scored: each work counts by how
    well it matches, how recent it is, and the person's share of its
    authorship — a sole author gets the whole work, one of nine a third.
    Breadth then counts: one matching paper is a lead, not an expert, so a
    single-paper score keeps two thirds of its value, two papers nine tenths. */
function rankAuthors(hits){
  const by = new Map();
  for (const { w, rel } of hits){
    const au = (w.authorships || []).filter(a => a.author?.id);
    if (!au.length || au.length > 20) continue;          // consortium papers say little about any one author
    const age = THIS_YEAR - (w.publication_year || THIS_YEAR);
    const rec = age <= 4 ? 1 : age <= 9 ? 0.8 : 0.6;
    const share = 1 / Math.sqrt(au.length);
    for (const a of au){
      const id = shortId(a.author.id);
      const r = by.get(id) || { id, name:a.author.display_name, orcid:orcidOf(a.author.orcid) || null, score:0, works:[] };
      r.score += rel * rec * share;
      if (!r.works.some(x => x.id === shortId(w.id)))
        r.works.push({ id:shortId(w.id), title:w.title || w.display_name || "[untitled]", year:w.publication_year,
                       venue:tidyVenue(w.primary_location?.source?.display_name) || "", doi:doiOf(w.doi), rel });
      by.set(id, r);
    }
  }
  for (const r of by.values()) r.score *= 1 - Math.pow(0.35, r.works.length);
  return [...by.values()].sort((a, b) => b.score - a.score);
}

function buildCand(r, a){
  if (!a) return null;
  const inst = currentInstOf(a), span = activeSpan(a);
  const years = r.works.map(w => w.year).filter(Boolean);
  const hay = r.works.map(w => w.title).join(" . ");
  return {
    id:r.id, name:a.display_name || r.name, a, score:r.score,
    works:r.works.sort((x, y) => y.rel - x.rel || (y.year || 0) - (x.year || 0)),
    from:years.length ? Math.min(...years) : null, to:years.length ? Math.max(...years) : null,
    themes:themeHits(hay, 3).map(h => h.th.id),
    orcid:orcidOf(a.orcid) || r.orcid || null,
    inst, country:inst?.country_code || null,
    h:a.summary_stats?.h_index ?? null, worksCount:a.works_count ?? 0, cites:a.cited_by_count ?? 0, span,
    fieldN:fieldTopicCount(a),
    coi:{ level:"ok", reasons:[] }, isAuthor:false, sameCountry:false,
  };
}

/* ---------- Conflicts of interest ------------------------------------- */

/** Each line of the authors box: an ORCID or OpenAlex ID resolves exactly;
    a name is matched to the likeliest profile — one in the field, with the
    most works — and shown, so you can pick another. */
async function resolvePeople(text){
  const lines = String(text || "").split(/\n|;/).map(s => s.trim()).filter(Boolean).slice(0, 12);
  return Promise.all(lines.map(async line => {
    const p = { line, how:"none", a:null, alts:[], ids:[], profiles:[] };
    try {
      const mo = line.match(/(\d{4}-\d{4}-\d{4}-\d{3}[\dX])/i), mx = line.match(/\b(A\d{5,})\b/i);
      if (mo){
        const prof = await orcidProfiles(mo[1].toUpperCase());
        if (prof.length){ p.a = prof[0]; p.profiles = prof; p.how = "orcid"; }
      } else if (mx){
        const a = await getJSON(oa("/authors/" + mx[1].toUpperCase()), { optional:true });
        if (a){ p.a = a; p.how = "openalex"; p.profiles = [a, ...(await orcidProfiles(orcidOf(a.orcid))).filter(x => shortId(x.id) !== shortId(a.id))]; }
      } else {
        const d = await getJSON(oa("/authors", { search:line, per_page:8 }), { optional:true });
        p.alts = (d?.results || []).sort((x, y) => (fieldTopicCount(y) > 0) - (fieldTopicCount(x) > 0) || (y.works_count || 0) - (x.works_count || 0));
        if (p.alts.length){ await setPerson(p, p.alts[0], "name"); }
      }
    } catch (e) { /* unresolved: shown as not found */ }
    p.ids = p.profiles.map(x => shortId(x.id));
    return p;
  }));
}

async function setPerson(p, a, how){
  p.a = a; p.how = how; p.co = null;
  const sib = a?.orcid ? (await orcidProfiles(orcidOf(a.orcid))).filter(x => shortId(x.id) !== shortId(a.id)) : [];
  p.profiles = a ? [a, ...sib] : [];
  p.ids = p.profiles.map(x => shortId(x.id));
}

/** Everyone the person has published with, and when — from their own works. */
async function loadPersonCoi(p){
  const map = new Map(), orcids = new Map();
  let cursor = "*";
  for (let page = 0; page < 5 && cursor && p.ids.length; page++){
    const d = await getJSON(oa("/works", { filter:"author.id:" + p.ids.join("|"), select:"id,publication_year,authorships",
                                           per_page:200, cursor }), { optional:true });
    if (!d) break;
    for (const w of d.results || []) for (const au of w.authorships || []){
      const id = shortId(au.author?.id);
      if (!id || p.ids.includes(id)) continue;
      const r = map.get(id) || { n:0, first:9999, last:0 };
      r.n++;
      if (w.publication_year){ r.first = Math.min(r.first, w.publication_year); r.last = Math.max(r.last, w.publication_year); }
      map.set(id, r);
      const oc = orcidOf(au.author?.orcid);
      if (oc) orcids.set(oc, r);
    }
    cursor = d.meta?.next_cursor;
    if (!(d.results || []).length) break;
  }
  p.co = { map, orcids };
  p.insts = instYears(p.profiles);
}

/** Institutions with the years a person was there; "current" means the last
    known institution or one recorded in the last two years. */
function instYears(profiles){
  const m = new Map();
  for (const a of [].concat(profiles).filter(Boolean)){
    for (const af of a.affiliations || []){
      const id = shortId(af.institution?.id);
      if (!id) continue;
      const v = m.get(id) || { name:af.institution.display_name, country:af.institution.country_code, years:new Set() };
      (af.years || []).forEach(y => v.years.add(y));
      m.set(id, v);
    }
    for (const li of a.last_known_institutions || []){
      const id = shortId(li.id);
      if (!id) continue;
      const v = m.get(id) || { name:li.display_name, country:li.country_code, years:new Set() };
      v.current = true;
      m.set(id, v);
    }
  }
  for (const v of m.values()) if ([...v.years].some(y => y >= THIS_YEAR - 1)) v.current = true;
  return m;
}
const yearSpan = ys => { const s = [...ys].sort((a, b) => a - b); return s.length ? (s[0] === s[s.length - 1] ? String(s[0]) : s[0] + "–" + s[s.length - 1]) : ""; };

function applyCoi(){
  const win = +RV.f.coi || 5;
  const people = RV.people.filter(p => p.a);
  const countries = new Set(people.flatMap(p => [...(p.insts || new Map()).values()].filter(v => v.current).map(v => v.country)).filter(Boolean));
  const authorIds = new Set(people.flatMap(p => p.ids));
  const authorOrcids = new Set(people.flatMap(p => p.profiles.map(x => orcidOf(x.orcid))).filter(Boolean));
  for (const c of RV.cands){
    c.isAuthor = authorIds.has(c.id) || (!!c.orcid && authorOrcids.has(c.orcid));
    c.sameCountry = !!c.country && countries.has(c.country);
    const reasons = [];
    if (!c.isAuthor) for (const p of people){
      const who = p.a.display_name;
      const co = p.co?.map.get(c.id) || (c.orcid && p.co?.orcids.get(c.orcid));
      if (co){
        if (co.last >= THIS_YEAR - win) reasons.push({ level:"bad", k:"coi.co.recent", v:{ name:who, n:co.n, year:co.last } });
        else reasons.push({ level:"warn", k:"coi.co.old", v:{ name:who, n:co.n, years:co.first === co.last ? co.last : co.first + "–" + co.last, win } });
      }
      // OpenAlex can hold one institution under two ids; one line per name,
      // "same institution now" taking precedence over "there at the same time".
      const mine = instYears(c.a), byName = new Map();
      for (const [id, pi] of p.insts || []){
        const ci = mine.get(id);
        if (!ci) continue;
        const cur = byName.get(pi.name) || { now:false, years:new Set() };
        if (pi.current && ci.current) cur.now = true;
        [...pi.years].filter(y => ci.years.has(y) && y >= THIS_YEAR - win).forEach(y => cur.years.add(y));
        byName.set(pi.name, cur);
      }
      for (const [inst, v] of byName){
        if (v.now) reasons.push({ level:"bad", k:"coi.inst.now", v:{ name:who, inst } });
        else if (v.years.size) reasons.push({ level:"warn", k:"coi.inst.past", v:{ name:who, inst, years:yearSpan(v.years) } });
      }
    }
    c.coi = { level: reasons.some(r => r.level === "bad") ? "bad" : reasons.length ? "warn" : "ok", reasons };
  }
}
function reasonText(r){
  const v = { ...r.v };
  if (v.n != null) v.works = tn(v.n, "work");
  if (v.win != null) v.win = tn(v.win, "year");
  return t(r.k, v);
}

/* ---------- Running ---------------------------------------------------- */

const rvText = f => [f.title, f.abstract, f.keywords].join("\u0000");

function rvStep(msg){
  RV.step = msg;
  const el = $("#rvStep");
  if (el) el.textContent = msg;
}

async function runReviewers(){
  const f = RV.f;
  if (!f.title.trim() && !f.abstract.trim() && !f.keywords.trim()) return toast(t("Paste at least a title or an abstract."), { bad:true });
  const run = ++RV.runId;
  if (RV.termsFor !== rvText(f)){ RV.terms = extractTerms(f); RV.termsFor = rvText(f); }
  RV.themes = themeHits([f.title, f.abstract, f.keywords].join(" "), 3).map(h => h.th.id);
  if (!RV.terms.some(x => x.on)){
    RV.status = "error"; RV.error = t("No usable search terms were found. Add a few keywords.");
    return renderReviewers();
  }
  RV.status = "running"; RV.error = ""; RV.shown = 25; RV.selected.clear();
  RV.step = t("Searching OpenAlex for works on these terms…");
  renderReviewers();
  try {
    const sameAuthors = RV.peopleFor === f.authors.trim();
    const peopleP = sameAuthors ? Promise.resolve(RV.people) : resolvePeople(f.authors);
    const hits = await searchWorks();
    if (run !== RV.runId) return;
    RV.worksN = hits.length;
    const ranked = rankAuthors(hits).slice(0, 80);
    rvStep(t("Reading {n} candidates' records…", { n:ranked.length }));
    const [authors, people] = await Promise.all([fetchAuthors(ranked.map(r => r.id)), peopleP]);
    if (run !== RV.runId) return;
    RV.people = people; RV.peopleFor = f.authors.trim();
    if (people.some(p => p.a && !p.co)){
      rvStep(t("Looking up the authors' co-authors and institutions…"));
      await Promise.all(people.filter(p => p.a && !p.co).map(loadPersonCoi));
    }
    if (run !== RV.runId) return;
    // Someone whose own record OpenAlex files under Romani studies ranks a
    // little above an equally matched newcomer to the field.
    RV.cands = ranked.map(r => buildCand(r, authors.get(r.id))).filter(Boolean)
      .map(c => { if (c.fieldN > 0) c.score *= 1.15; return c; }).sort((a, b) => b.score - a.score);
    applyCoi();
    RV.status = "done";
  } catch (e){
    if (run !== RV.runId) return;
    RV.status = "error"; RV.error = t("Lookup failed: {msg}", { msg:e.message });
  }
  renderReviewers();
  // Stacked on a narrow screen, the results sit below a long form.
  const res = $(".rv-results");
  if (RV.status === "done" && res && getComputedStyle($(".rv-layout")).gridTemplateColumns.split(" ").length < 2)
    scrollTo({ top:res.getBoundingClientRect().top + scrollY - (parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--mast-h")) || 60) - 8, behavior:"smooth" });
}

let rvRerunT;
const rvRerun = () => { clearTimeout(rvRerunT); rvRerunT = setTimeout(runReviewers, 650); };

/* ---------- Rendering -------------------------------------------------- */

function rvSplit(){
  const main = [], aside = [];
  let thin = 0, same = 0;
  for (const c of RV.cands){
    if (c.isAuthor){ aside.push({ c, why:"author" }); continue; }
    if (RV.excluded.has(c.id)){ aside.push({ c, why:"excluded" }); continue; }
    if (c.coi.level === "bad"){ aside.push({ c, why:"conflict" }); continue; }
    if (RV.f.hideThin && c.worksCount < 5){ thin++; continue; }
    if (RV.f.otherCountries && c.sameCountry){ same++; continue; }
    main.push(c);
  }
  return { main, aside, thin, same };
}

function renderReviewers(){
  if (CMP.host === "reviewers") CMP.active = false;
  setAddress({}, "reviewers");
  const f = RV.f;
  const opt = (v, label, cur) => `<option value="${esc(v)}" ${String(cur) === String(v) ? "selected" : ""}>${esc(label)}</option>`;
  setView("reviewers", `
  <div class="rv-layout">
    <form class="card rv-form" id="rvForm" autocomplete="off">
      <header><h3>${esc(t("Manuscript"))}</h3><div class="sp"></div><span class="hdr-note">${esc(t("stays in this browser"))}</span></header>
      <div class="body">
        <label class="fld"><span>${esc(t("Title"))}</span>
          <input type="text" id="rvTitle" value="${esc(f.title)}" spellcheck="false"></label>
        <label class="fld"><span>${esc(t("Abstract"))}</span>
          <textarea id="rvAbstract" rows="8">${esc(f.abstract)}</textarea>
          <small>${esc(t("The English abstract finds more, if there is one — most indexed work is in English."))}</small></label>
        <label class="fld"><span>${esc(t("Keywords"))} <i>${esc(t("optional"))}</i></span>
          <input type="text" id="rvKeywords" value="${esc(f.keywords)}" placeholder="${esc(t("separated by commas"))}"></label>
        <label class="fld"><span>${esc(t("Authors of the manuscript"))} <i>${esc(t("for the conflict check"))}</i></span>
          <textarea id="rvAuthors" rows="3" placeholder="${esc(t("One per line: name, ORCID or OpenAlex ID"))}">${esc(f.authors)}</textarea></label>
        <div class="fld-opts">
          <label class="ctl">${esc(t("Matching work from the last"))}
            <select id="rvYears">${["5","10","15","20","any"].map(y => opt(y, y === "any" ? t("any period") : tn(+y, "year"), f.years)).join("")}</select></label>
          <label class="ctl">${esc(t("Co-authorship is a conflict within"))}
            <select id="rvCoi">${["3","5","10"].map(y => opt(y, tn(+y, "year"), f.coi)).join("")}</select></label>
          <label class="chk"><input type="checkbox" id="rvOther" ${f.otherCountries ? "checked" : ""}> ${esc(t("Only reviewers outside the authors' countries"))}</label>
          <label class="chk"><input type="checkbox" id="rvThin" ${f.hideThin ? "checked" : ""}> ${esc(t("Hide records with fewer than five works"))}</label>
        </div>
        <div class="rv-acts">
          <button class="btn" type="submit" id="rvGo" ${RV.status === "running" ? "disabled" : ""}>${esc(t("Find reviewers"))}</button>
          <button class="btn ghost" type="button" id="rvReset">${esc(t("Clear"))}</button>
        </div>
        <p class="fine">${esc(t("rv.privacy"))}</p>
      </div>
    </form>
    <div class="rv-results">${rvResults()}</div>
  </div>`);
  wireReviewers();
  if (RV.status === "done") rvEnrichVisible();
}

function rvResults(){
  if (RV.status === "idle") return `<div class="card"><header><h3>${esc(t("How it works"))}</h3></header>
    <div class="body rv-how">
      <ol>
        <li>${esc(t("rv.how.1"))}</li>
        <li>${esc(t("rv.how.2"))}</li>
        <li>${esc(t("rv.how.3"))}</li>
      </ol>
      <div class="note">${esc(t("rv.limits"))}</div>
    </div></div>`;
  if (RV.status === "running") return `<div class="card"><div class="progress"><span class="spinner"></span> ${esc(t("Finding reviewers"))}
    <div class="step" id="rvStep">${esc(RV.step)}</div></div></div>`;
  if (RV.status === "error") return `${RV.terms.length ? rvCriteria() : ""}<div class="err">${esc(RV.error)}</div>`;

  const { main, aside, thin, same } = rvSplit();
  const topScore = Math.max(1e-9, ...main.map(c => c.score));
  const since = RV.f.years === "any" ? null : THIS_YEAR - (+RV.f.years || 10);
  const list = main.slice(0, RV.shown);
  return `${rvCriteria()}
  <div class="card">
    <header><h3>${esc(t("Candidates"))}</h3><div class="sp"></div>
      <span class="hdr-note">${esc(t("ranked from {works}", { works:tn(RV.worksN, "matching work") }))} · ${esc(since ? t("since {year}", { year:since }) : t("all years"))}</span></header>
    ${(thin || same) ? `<div class="rv-hidden muted">${[
        thin ? t("{n} with fewer than five works hidden", { n:thin }) : "",
        same ? t("{n} in the authors' countries hidden", { n:same }) : "" ].filter(Boolean).map(esc).join(" · ")}</div>` : ""}
    ${list.length ? `<div class="rv-list">${list.map((c, i) => rvRow(c, i + 1, c.score / topScore)).join("")}</div>
      ${main.length > RV.shown ? `<div class="more-row"><button class="icon-btn" id="rvMore">${esc(t("Show {n} more", { n:Math.min(25, main.length - RV.shown) }))}</button></div>` : ""}
      <div class="cmpbar" id="rvBar"></div>`
      : `<div class="empty">${esc(t("No authors found for these terms. Switch some terms off, add a keyword, or widen the period."))}</div>`}
  </div>
  ${aside.length ? `<div class="card rv-aside">
    <header><h3>${esc(t("Set aside"))} · ${aside.length}</h3><div class="sp"></div>
      <span class="hdr-note">${esc(t("conflicts, the manuscript's own authors, and anyone you excluded"))}</span>
      <button class="icon-btn" id="rvAsideT">${esc(RV.showAside ? t("Hide") : t("Show"))}</button></header>
    ${RV.showAside ? `<div class="rv-list">${aside.map(({ c, why }) => rvRow(c, null, c.score / topScore, why)).join("")}</div>` : ""}
  </div>` : ""}`;
}

/** What the search used: the terms (switchable), the manuscript's themes,
    and who the conflict check ran against. */
function rvCriteria(){
  const how = { orcid:t("ORCID — exact"), openalex:t("OpenAlex ID — exact"), name:t("matched by name — check"),
                picked:t("chosen by you"), none:t("not found"), skipped:t("skipped") };
  return `<div class="card rv-crit"><div class="body">
    <div class="crit-row"><span class="eyebrow">${esc(t("Search terms"))}</span>
      <div class="terms">${RV.terms.map((x, i) => `<button type="button" class="term ${x.on ? "on" : ""}" data-term="${i}" aria-pressed="${x.on}"
          title="${esc(x.forms.join(" · "))}">${esc(x.text)}</button>`).join("")}
        <form class="term-add" id="rvAddTerm"><input type="text" id="rvNewTerm" placeholder="${esc(t("add a term"))}" aria-label="${esc(t("add a term"))}"></form>
      </div></div>
    ${RV.themes.length ? `<div class="crit-row"><span class="eyebrow">${esc(t("Themes in the manuscript"))}</span>
      <div class="terms">${RV.themes.map(id => `<span class="theme-tag">${esc(themeName(id))}</span>`).join("")}</div></div>` : ""}
    <div class="crit-row"><span class="eyebrow">${esc(t("Conflict check against"))}</span>
      <div class="terms">${RV.people.length ? RV.people.map((p, i) => `<span class="person how-${p.how}">
          <b>${esc(p.a?.display_name || p.line)}</b>${p.a ? `<small>${esc(currentInstOf(p.a)?.display_name || "")}${p.a.works_count != null ? " · " + esc(tn(p.a.works_count, "work")) : ""}</small>` : ""}
          <small class="how">${esc(how[p.how] || "")}</small>
          ${p.alts.length > 1 || p.how === "skipped" ? `<button type="button" class="linkish" data-person="${i}">${esc(t("change"))}</button>` : ""}
        </span>`).join("")
        : `<span class="muted">${esc(t("No authors given — add them to the form to check for conflicts."))}</span>`}</div></div>
  </div></div>`;
}

function rvRow(c, rank, rel, why = null){
  const strength = rel >= 0.6 ? ["strong", t("Strong match")] : rel >= 0.3 ? ["good", t("Good match")] : ["part", t("Partial match")];
  const saved = LIB.scholars[c.id];
  const picked = RV.selected.has(c.id);
  const lvl = why === "author" ? "info" : why === "excluded" ? "info" : c.coi.level;
  const badge = why === "author" ? t("One of the manuscript's authors")
    : why === "excluded" ? t("Excluded by you")
    : { ok:t("No conflict found"), warn:t("Check before inviting"), bad:t("Conflict of interest") }[c.coi.level];
  const ex = c.works.slice(0, 2);
  const inst = c.inst?.display_name || t("No affiliation recorded");
  return `<div class="rv-cand coi-${lvl} ${picked ? "picked" : ""}" data-id="${esc(c.id)}">
    ${rank ? `<label class="pick" title="${esc(t("Select"))}"><input type="checkbox" data-rpick="${esc(c.id)}" ${picked ? "checked" : ""}></label>` : `<span></span>`}
    <div class="rv-main">
      <div class="rv-top">${rank ? `<span class="rv-rank">${rank}</span>` : ""}
        <button class="pname" data-open="${esc(c.id)}">${esc(c.name)}</button>
        ${c.orcid ? `<span class="b oa" title="ORCID ${esc(c.orcid)}">ORCID</span>` : ""}
        ${saved ? `<span class="b manual">★ ${esc(t("saved"))}</span>` : ""}
        ${c.sameCountry ? `<span class="b idx" title="${esc(t("Same country as the authors"))}">${esc(c.country)}</span>` : ""}
      </div>
      <div class="psub">${esc(inst)}${c.country ? " · " + esc(countryName(c.country)) : ""}
        · h ${c.h ?? "—"} · ${esc(tn(c.worksCount, "work"))}${c.span[1] ? " · " + esc(t("active {from}–{to}", { from:c.span[0], to:c.span[1] })) : ""}</div>
      <div class="rv-why"><b>${esc(t("{n} matching {works}", { n:c.works.length, works:tw(c.works.length, "work") }))}</b>${c.from ? `, ${c.from === c.to ? c.from : c.from + "–" + c.to}` : ""}:
        ${ex.map(w => `<i>${esc(w.title)}</i> (${w.year || esc(t("n.d."))}${w.venue ? ", " + esc(w.venue) : ""})`).join("; ")}
        ${c.works.length > 2 ? `<button type="button" class="linkish" data-more="${esc(c.id)}">+${c.works.length - 2}</button>` : ""}</div>
      <ul class="dd-list rv-morelist" data-morelist="${esc(c.id)}" hidden>${c.works.slice(2, 12).map(w => `<li><span class="yr">${w.year || esc(t("n.d."))}</span>${w.doi
        ? `<a href="https://doi.org/${esc(w.doi)}" target="_blank" rel="noopener">${esc(w.title)}</a>` : esc(w.title)}${w.venue ? ` <span class="muted">· ${esc(w.venue)}</span>` : ""}</li>`).join("")}</ul>
      ${c.themes.length ? `<div class="rv-themes">${c.themes.map(id => `<span class="theme-tag ${RV.themes.includes(id) ? "hit" : ""}">${esc(themeName(id))}</span>`).join("")}</div>` : ""}
      ${why ? "" : `<div class="rv-contact" data-contact="${esc(c.id)}">${contactLine(c)}</div>`}
    </div>
    <div class="rv-side">
      <div class="fit fit-${strength[0]}"><span class="bar"><i style="width:${Math.max(6, Math.round(rel * 100))}%"></i></span><span>${esc(strength[1])}</span></div>
      <div class="coi-badge ${lvl}">${esc(badge)}</div>
      ${c.coi.reasons.length ? `<ul class="coi-list">${c.coi.reasons.map(r => `<li class="${r.level}">${esc(reasonText(r))}</li>`).join("")}</ul>` : ""}
      <div class="rv-acts">
        <button class="icon-btn" data-rsave="${esc(c.id)}">${saved ? "★ " + esc(t("Saved")) : "☆ " + esc(t("Save"))}</button>
        ${why === "excluded" ? `<button class="icon-btn" data-restore="${esc(c.id)}">${esc(t("Restore"))}</button>`
          : why ? "" : `<button class="icon-btn" data-exclude="${esc(c.id)}">${esc(t("Exclude"))}</button>`}
      </div>
    </div>
  </div>`;
}

function contactLine(c){
  if (!c.orcid) return `<span class="muted">${esc(t("No ORCID — the dossier lists other ways to reach them."))}</span>`;
  const e = RV.enrich.get(c.orcid);
  if (!e || e === "loading") return `<span class="muted">${esc(t("checking ORCID…"))}</span>`;
  const bits = [];
  if (e.emails.length) bits.push(`✉ ${e.emails.slice(0, 2).map(m => `<a href="mailto:${esc(m)}">${esc(m)}</a>`).join(", ")} <span class="muted">${esc(t("on ORCID"))}</span>`);
  else bits.push(`<span class="muted">${esc(t("No public email on ORCID — the dossier lists other routes."))}</span>`);
  if (e.venues) bits.push(esc(t("has reviewed for {venues}", { venues:tn(e.venues, "journal") })));
  return bits.join(" · ");
}

/** Public email and review record from ORCID, for the candidates on screen. */
function rvEnrichVisible(){
  const { main } = rvSplit();
  main.slice(0, RV.shown).filter(c => c.orcid && !RV.enrich.has(c.orcid)).forEach(async c => {
    RV.enrich.set(c.orcid, "loading");
    const [p, r] = await Promise.all([
      getJSON(CFG.orcid + "/" + c.orcid + "/person", { optional:true }),
      getJSON(CFG.orcid + "/" + c.orcid + "/peer-reviews", { optional:true }),
    ]);
    RV.enrich.set(c.orcid, { emails:(p?.emails?.email || []).map(x => x.email).filter(Boolean), venues:(r?.group || []).length });
    const el = $(`#view-reviewers [data-contact="${CSS.escape(c.id)}"]`);
    if (el) el.innerHTML = contactLine(c);
  });
}

function wireReviewers(){
  const V = "#view-reviewers";
  const bind = (id, key, ev = "input", prop = "value") => {
    const el = $("#" + id);
    el.addEventListener(ev, () => { RV.f[key] = el[prop]; });
  };
  bind("rvTitle", "title"); bind("rvAbstract", "abstract"); bind("rvKeywords", "keywords"); bind("rvAuthors", "authors");
  const reapply = () => { if (RV.status === "done"){ applyCoi(); renderReviewers(); } };
  $("#rvYears").onchange = e => { RV.f.years = e.target.value; if (RV.status === "done") runReviewers(); };
  $("#rvCoi").onchange   = e => { RV.f.coi = e.target.value; reapply(); };
  $("#rvOther").onchange = e => { RV.f.otherCountries = e.target.checked; reapply(); };
  $("#rvThin").onchange  = e => { RV.f.hideThin = e.target.checked; reapply(); };
  $("#rvForm").onsubmit = e => { e.preventDefault(); runReviewers(); };
  $("#rvReset").onclick = async () => {
    if ((RV.f.title || RV.f.abstract) && !await ask({ title:t("Clear the manuscript?"), text:t("The title, abstract, authors and results go."), ok:t("Clear") })) return;
    RV.runId++;
    Object.assign(RV, { terms:[], termsFor:"", themes:[], people:[], peopleFor:"", cands:[], status:"idle", error:"", showAside:false });
    RV.f = { ...RV.f, title:"", abstract:"", keywords:"", authors:"" };
    RV.excluded.clear(); RV.selected.clear();
    renderReviewers();
  };

  $$(`${V} [data-term]`).forEach(b => b.onclick = () => {
    const x = RV.terms[+b.dataset.term];
    x.on = !x.on;
    b.classList.toggle("on", x.on); b.setAttribute("aria-pressed", String(x.on));
    if (RV.terms.some(y => y.on)) rvRerun();
  });
  const add = $("#rvAddTerm");
  if (add) add.onsubmit = e => {
    e.preventDefault();
    const v = $("#rvNewTerm").value.trim();
    if (v.length < 2) return;
    RV.terms.push({ text:v, forms:[v.toLowerCase()], src:"user", on:true });
    runReviewers();
  };
  $$(`${V} [data-person]`).forEach(b => b.onclick = () => rvChangePerson(+b.dataset.person));

  $$(`${V} [data-open]`).forEach(b => b.onclick = () => openScholar(b.dataset.open));
  $$(`${V} [data-more]`).forEach(b => b.onclick = () => {
    const ul = $(`${V} [data-morelist="${CSS.escape(b.dataset.more)}"]`);
    if (ul){ ul.hidden = !ul.hidden; b.textContent = ul.hidden ? "+" + (ul.children.length) : "−"; }
  });
  $$(`${V} [data-rpick]`).forEach(cb => cb.onchange = () => {
    cb.checked ? RV.selected.add(cb.dataset.rpick) : RV.selected.delete(cb.dataset.rpick);
    cb.closest(".rv-cand").classList.toggle("picked", cb.checked);
    rvBar();
  });
  $$(`${V} [data-exclude]`).forEach(b => b.onclick = () => { RV.excluded.add(b.dataset.exclude); RV.selected.delete(b.dataset.exclude); renderReviewers(); });
  $$(`${V} [data-restore]`).forEach(b => b.onclick = () => { RV.excluded.delete(b.dataset.restore); renderReviewers(); });
  $$(`${V} [data-rsave]`).forEach(b => b.onclick = async () => {
    const c = RV.cands.find(x => x.id === b.dataset.rsave);
    if (!c) return;
    const fid = await pickFolder({ title:t("Save {name}", { name:c.name }), suggest:rvFolderName() });
    if (fid === null) return;
    await libSaveAuthors([c.a], fid);
    toast(t("Saved to your library."));
    renderReviewers();
  });
  const mo = $("#rvMore"); if (mo) mo.onclick = () => { RV.shown += 25; renderReviewers(); };
  const at = $("#rvAsideT"); if (at) at.onclick = () => { RV.showAside = !RV.showAside; renderReviewers(); };
  rvBar();
}

const rvFolderName = () => t("Reviewers — {title}", { title:(RV.f.title.trim() || t("manuscript")).slice(0, 48) });

async function rvChangePerson(i){
  const p = RV.people[i];
  const k = await choose({ title:t("Who is “{name}”?", { name:p.line }),
    text:t("The conflict check runs against the profile you choose."),
    choices:[
      ...p.alts.slice(0, 8).map((a, j) => ({ value:String(j), label:a.display_name,
        sub:[currentInstOf(a)?.display_name, tn(a.works_count || 0, "work"),
             fieldTopicCount(a) ? t("{n} in Romani studies", { n:fieldTopicCount(a) }) : "",
             a.orcid ? "ORCID " + orcidOf(a.orcid) : ""].filter(Boolean).join(" · ") })),
      { value:"skip", label:t("None of these"), sub:t("leave this author out of the conflict check") },
    ] });
  if (k === null) return;
  if (k === "skip"){ p.a = null; p.how = "skipped"; p.ids = []; p.profiles = []; p.co = null; p.insts = null; }
  else {
    await setPerson(p, p.alts[+k], "picked");
    await loadPersonCoi(p);
  }
  applyCoi();
  renderReviewers();
}

function rvBar(){
  const bar = $("#rvBar");
  if (!bar) return;
  const n = RV.selected.size;
  const authors = RV.people.filter(p => p.a);
  bar.innerHTML = `
    <span>${n ? esc(t("{n} selected", { n })) : esc(t("Tick candidates to shortlist them"))}</span>
    <span class="ctl-sp"></span>
    ${n ? `<button class="icon-btn" id="rvClearSel">${esc(t("Clear"))}</button>
           <button class="icon-btn" id="rvSaveSel">${esc(t("Save shortlist to folder…"))}</button>` : ""}
    <button class="icon-btn" id="rvCsv">${esc(t("Export CSV"))}</button>
    <button class="btn small" id="rvMap" ${n + authors.length < 2 || !n ? "disabled" : ""}>${esc(authors.length ? t("Map with the authors") : t("Map relations"))}</button>`;
  bar.classList.toggle("active", n > 0);
  const sel = () => RV.cands.filter(c => RV.selected.has(c.id));
  const cl = $("#rvClearSel"); if (cl) cl.onclick = () => { RV.selected.clear(); renderReviewers(); };
  const sv = $("#rvSaveSel"); if (sv) sv.onclick = async () => {
    const fid = await pickFolder({ title:t("Save {n} to the library", { n:tn(n, "scholar") }), suggest:rvFolderName() });
    if (fid === null) return;
    const added = await libSaveAuthors(sel().map(c => c.a), fid);
    toast(t("Saved: {n} new in the library.", { n:added }));
    renderReviewers();
  };
  $("#rvCsv").onclick = () => exportReviewersCSV(n ? sel() : rvSplit().main);
  $("#rvMap").onclick = () => {
    const ids = [...new Set([...authors.map(p => shortId(p.a.id)), ...sel().map(c => c.id)])];
    if (ids.length > CMP_MAX) return toast(t("Up to {n} at a time — beyond that the map stops being readable.", { n:CMP_MAX }), { bad:true });
    const names = Object.fromEntries([...authors.map(p => [shortId(p.a.id), p.a.display_name]), ...sel().map(c => [c.id, c.name])]);
    renderCompare(ids, { host:"reviewers", names });
  };
}

function exportReviewersCSV(list){
  const head = ["rank","name","openalex","orcid","institution","country","matching_works","first_match","last_match",
                "h_index","works","citations","conflict","conflict_detail","same_country_as_authors","public_email","reviewed_for_journals"];
  const rows = list.map((c, i) => {
    const e = c.orcid ? RV.enrich.get(c.orcid) : null;
    return [i + 1, c.name, "https://openalex.org/" + c.id, c.orcid || "", c.inst?.display_name || "", c.country || "",
      c.works.length, c.from ?? "", c.to ?? "", c.h ?? "", c.worksCount, c.cites,
      c.coi.level === "ok" ? "none found" : c.coi.level === "warn" ? "check" : "conflict",
      c.coi.reasons.map(reasonText).join("; "), c.sameCountry ? "yes" : "",
      e && e !== "loading" ? e.emails.join("; ") : "", e && e !== "loading" ? e.venues : ""].map(csvCell).join(",");
  });
  download(`srom-reviewers-${stamp()}.csv`, "﻿" + head.join(",") + "\n" + rows.join("\n"), "text/csv;charset=utf-8");
}

VIEW_ENTER.reviewers = () => {
  if (CMP.active && CMP.host === "reviewers") return drawGraph();
  if (!$("#rvForm")) renderReviewers();
};
