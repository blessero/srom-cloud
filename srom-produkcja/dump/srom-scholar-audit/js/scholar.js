"use strict";

/* =====================================================================
   One scholar's record: from a name, ORCID or OpenAlex ID to a scored,
   characterised publication record. No rendering here — dossier.js draws
   it, library.js compares records, reviewers.js reuses the scoring.
   ===================================================================== */

/* ---------- 4. Resolution: query -> author --------------------------- */

async function resolveQuery(q){
  q = q.trim();
  if (!q) return { kind:"empty" };

  const mo = q.match(RX_ORCID);
  if (mo){
    // Not /authors/orcid:… — when several profiles share an ORCID, that
    // endpoint can return the smallest (for one scholar, a one-work fragment
    // instead of the 105-work record). loadAuthor gathers all of them.
    const list = await orcidProfiles(mo[1]);
    if (list.length) return { kind:"author", author:list[0] };
    // ORCID exists but OpenAlex has no matching author record.
    return { kind:"orcid-only", orcid: mo[1] };
  }

  const mx = q.match(RX_OPENALEX);
  if (mx) return { kind:"author", author: await getJSON(oa("/authors/" + mx[1])) };

  const d = await getJSON(oa("/authors", { search:q, per_page:25 }));
  const list = d.results || [];
  if (!list.length) return { kind:"none" };
  if (list.length === 1) return { kind:"author", author:list[0] };
  return { kind:"candidates", list };
}

/** Every OpenAlex profile that carries this ORCID, largest first. OpenAlex
    splits one person across several profiles often enough to matter; a
    shared ORCID is the scholar's own assertion that they are one person,
    so those profiles are safe to merge. */
async function orcidProfiles(orcid){
  if (!orcid) return [];
  const d = await getJSON(oa("/authors", { filter:"orcid:" + orcid, per_page:25 }), { optional:true });
  return (d?.results || []).sort((a, b) => (b.works_count || 0) - (a.works_count || 0));
}

/** How many of a candidate's works sit in the field? Cheap: one count query. */
async function fieldCountFor(authorId){
  const d = await getJSON(oa("/works", {
    filter: `author.id:${shortId(authorId)},topics.id:${FIELD.topicIds.join("|")}`,
    per_page: 1,
  }), { optional:true });
  return d?.meta?.count ?? 0;
}

/* ---------- 5. Enrichment: author -> full dossier -------------------- */

async function buildDossier(author, onStep, siblings = []){
  S.author  = author;
  S.storedAt = null;
  S.siblings = siblings;
  S.works   = [];
  S.sources = new Map();
  S.orcid   = null;
  S.wikidata = null;
  S.s2 = null;
  S.inst = null;
  S.orcidInferred = false;
  S.reviews = [];

  const aid = [author.id, ...siblings.map(x => x.id)].map(shortId).join("|");

  onStep(t("Retrieving publication record from OpenAlex…"));
  S.works = await fetchAllWorks(aid, onStep);

  onStep(t("Resolving venues and indexing status…"));
  await fetchSources();

  onStep(t("Resolving books and chapters via Crossref…"));
  await enrichFromCrossref(onStep);

  const orcidId = orcidOf(author.orcid);
  if (orcidId){
    onStep(t("Cross-checking ORCID record…"));
    S.orcid = await getJSON(CFG.orcid + "/" + orcidId + "/record", { optional:true });
    if (S.orcid){
      onStep(t("Resolving peer-review activity…"));
      S.reviews = await resolveReviews(S.orcid);
    }
  }

  onStep(t("Checking DOAJ registration for journals…"));
  await checkDoaj();

  onStep(t("Resolving scholarly profiles…"));
  let orcidId2 = orcidOf(author.orcid);
  if (!orcidId2){
    orcidId2 = await orcidByName(author.display_name);
    if (orcidId2){
      S.orcidInferred = true;
      S.orcid = await getJSON(CFG.orcid + "/" + orcidId2 + "/record", { optional:true });
    }
  }
  S.wikidata = await resolveWikidata(orcidId2, author.display_name);
  S.s2 = await resolveSemanticScholar(author.display_name, S.works);
  S.inst = await currentInstitution(author);

  onStep(t("Scoring venues and field relevance…"));
  S.works.forEach(scoreWork);
}

/* ---------- 5b. Identifier resolution ------------------------------- */

function wd(params){
  const u = new URL(CFG.wikidata);
  for (const [k, v] of Object.entries({ format:"json", origin:"*", ...params }))
    u.searchParams.set(k, v);
  return u.toString();
}

/** OpenAlex carries only its own id and ORCID. When it has no ORCID, ORCID's
    own name index often does — and an ORCID is the key that unlocks Wikidata. */
async function orcidByName(name){
  const parts = String(name).trim().split(/\s+/);
  if (parts.length < 2) return null;
  const family = parts[parts.length - 1];
  const given  = parts.slice(0, -1).join(" ");
  const q = `given-names:${given} AND family-name:${family}`;
  const d = await getJSON(
    CFG.orcid + "/expanded-search/?q=" + encodeURIComponent(q) + "&rows=5",
    { optional:true });
  const hits = d?.["expanded-result"] || [];
  // Only accept an unambiguous single match; guessing an identity is worse
  // than leaving it blank.
  return hits.length === 1 ? hits[0]["orcid-id"] : null;
}

/** Wikidata by ORCID is exact. By name it is a guess, so it is accepted only
    when the item is a human whose label matches and which carries at least
    one scholarly identifier. */
async function resolveWikidata(orcid, name){
  let qid = null, how = null;

  if (orcid){
    const d = await getJSON(wd({
      action:"query", list:"search",
      srsearch:"haswbstatement:P496=" + orcid, srlimit:1,
    }), { optional:true });
    qid = d?.query?.search?.[0]?.title || null;
    if (qid) how = "ORCID";
  }

  if (!qid && name){
    const d = await getJSON(wd({
      action:"wbsearchentities", search:name, language:"en", type:"item", limit:5,
    }), { optional:true });
    const cand = (d?.search || []).find(r =>
      String(r.label || "").toLowerCase() === String(name).toLowerCase());
    qid = cand?.id || null;
    if (qid) how = "name";
  }
  if (!qid) return null;

  const e = await getJSON(wd({
    action:"wbgetentities", ids:qid,
    props:"claims|labels|descriptions", languages:"en",
  }), { optional:true });
  const ent = e?.entities?.[qid];
  if (!ent) return null;

  const claims = ent.claims || {};
  if (!claims.P31?.some(c => c.mainsnak?.datavalue?.value?.id === "Q5")) return null;

  const ids = {};
  for (const [pid, def] of Object.entries(WD_PROPS)){
    const v = claims[pid]?.[0]?.mainsnak?.datavalue?.value;
    if (typeof v === "string" && v) ids[def.key] = v;
  }
  // Matched on name alone with nothing scholarly attached — too weak to trust.
  if (!orcid && !Object.keys(ids).length) return null;

  return {
    id: qid,
    label: ent.labels?.en?.value || name,
    description: ent.descriptions?.en?.value || "",
    ids,
    matchedBy: how,
  };
}

/** Semantic Scholar's author search is unreliable — for one scholar it
    returned four fragmentary profiles. Going in through a known DOI lands on
    the real one, so resolve by publication rather than by name. */
async function resolveSemanticScholar(name, works){
  const surname = String(name).trim().split(/\s+/).pop().toLowerCase();
  const dois = works.filter(w => w.doi && w.cites > 0)
                    .sort((a,b) => b.cites - a.cites).slice(0, 3)
                    .map(w => w.doi);
  if (!dois.length) return null;

  for (const doi of dois){
    const d = await getJSON(
      CFG.s2 + "/paper/DOI:" + encodeURI(doi) +
      "?fields=authors.name,authors.authorId,authors.paperCount,authors.hIndex",
      { optional:true });
    const hit = (d?.authors || []).find(a =>
      String(a.name || "").toLowerCase().split(/\s+/).pop() === surname);
    if (hit?.authorId){
      return { authorId:hit.authorId, name:hit.name,
               paperCount:hit.paperCount, hIndex:hit.hIndex, viaDoi:doi };
    }
  }
  return null;
}

/** The most recent affiliation, with its website — the usual route to a
    staff directory and a contact address. */
async function currentInstitution(author){
  const aff = (author.affiliations || []).slice()
    .sort((a, b) => Math.max(0, ...(b.years || [])) - Math.max(0, ...(a.years || [])))[0];
  const inst = aff?.institution;
  if (!inst?.id) return null;
  const d = await getJSON(oa("/institutions/" + shortId(inst.id)), { optional:true });
  return { name: inst.display_name, country: inst.country_code, ror: inst.ror || d?.ror || null,
           homepage: d?.homepage_url || null, year: Math.max(0, ...(aff.years || [])) || null };
}

/** Cursor-paged so prolific scholars come back complete, not truncated. */
const WORK_SELECT = [
  "id","doi","title","display_name","publication_year","publication_date","type",
  "cited_by_count","language","is_retracted","is_paratext","open_access",
  "primary_location","locations_count","authorships","biblio","topics",
  "indexed_in","fwci","citation_normalized_percentile","abstract_inverted_index","keywords",
  "referenced_works",
];

async function fetchAllWorks(aid, onStep, extra = []){
  const out = [];
  let cursor = "*";
  const SELECT = [...new Set(WORK_SELECT.concat(extra))].join(",");

  for (let page = 0; page < 25 && cursor; page++){
    const d = await getJSON(oa("/works", {
      filter: "author.id:" + aid,
      per_page: 200,
      cursor,
      select: SELECT,
      sort: "publication_date:desc",
    }));
    (d.results || []).forEach(w => out.push(normaliseWork(w, aid)));
    cursor = d.meta?.next_cursor || null;
    if (d.meta?.count > 200) onStep(t("Retrieved {n} of {total} works…", { n:num(out.length), total:num(d.meta.count) }));
    if (!cursor || out.length >= (d.meta?.count ?? 0)) break;
  }
  return out;
}

/* Publishers deposit a book's front and back matter as "chapters" with their
   own DOIs — "Illustrations", "Index", "Contents". Counted as works, they
   inflate a scholar's record. Exact titles only: an authored Introduction or
   Conclusion is real work and stays. */
const FRONT_MATTER = /^(illustrations?|list of (illustrations|figures|tables|maps|abbreviations|contributors)|index(es)?|(name|subject|general) index|contents|table of contents|bibliography|references|front ?matter|back ?matter|prelim(inary pages|s)?|title pages?|copyright( page)?|acknowledge?ments|abbreviations|notes on (the )?contributors|contributors|about the (authors?|editors?|contributors)|frontmatter|backmatter|imprint|dedication|plates|maps|figures|errata|erratum)$/i;
const isFrontMatter = t => FRONT_MATTER.test(String(t || "").trim().replace(/[.:;]+$/, ""));

function normaliseWork(w, aid){
  const loc  = w.primary_location || {};
  const src  = loc.source || null;
  const mine = new Set(String(aid).split("|"));
  const me   = (w.authorships || []).find(a => mine.has(shortId(a.author?.id)));
  const abs  = deInvert(w.abstract_inverted_index);

  return {
    id:        shortId(w.id),
    doi:       doiOf(w.doi),
    title:     w.title || w.display_name || "[untitled]",
    year:      w.publication_year || null,
    date:      w.publication_date || null,
    type:      w.type || "other",
    cites:     w.cited_by_count || 0,
    fwci:      w.fwci ?? null,
    pctile:    w.citation_normalized_percentile?.value ?? null,
    lang:      w.language || null,
    retracted: !!w.is_retracted,
    paratext:  !!w.is_paratext || w.type === "paratext" || isFrontMatter(w.title || w.display_name),
    oa:        w.open_access?.is_oa || false,
    oaStatus:  w.open_access?.oa_status || "closed",
    indexedIn: w.indexed_in || [],
    pages:     w.biblio?.first_page && w.biblio?.last_page
                 ? w.biblio.first_page + "–" + w.biblio.last_page : "",
    volume:    w.biblio?.volume || "",
    issue:     w.biblio?.issue || "",
    landing:   loc.landing_page_url || (w.doi || ""),
    pdf:       loc.pdf_url || "",
    license:   loc.license || "",
    version:   loc.version || "",
    sourceId:  src ? shortId(src.id) : null,
    venue:     tidyVenue(src?.display_name) || NO_VENUE,
    venueFrom: src ? "openalex" : null,
    isbn:      [],
    container: null,
    venueType: src?.type || null,
    issn:      src?.issn_l || (src?.issn || [])[0] || null,
    issnAll:   src?.issn || [],
    publisher: src?.host_organization_name || null,
    authorPos: me?.author_position || null,
    nAuthors:  (w.authorships || []).length,
    authors:   (w.authorships || []).map(a => a.author?.display_name || a.raw_author_name).filter(Boolean),
    coauthors: (w.authorships || [])
                 .filter(a => !mine.has(shortId(a.author?.id)))
                 .map(a => a.author?.display_name)
                 .filter(Boolean),
    myAffil:   (me?.institutions || []).map(i => i.display_name),
    topics:    (w.topics || []).map(t => ({ id: shortId(t.id), name: t.display_name, score: t.score })),
    keywords:  (w.keywords || []).map(k => k.display_name).filter(Boolean),
    abstract:  abs,
    refs:      (w.referenced_works || []).map(shortId),
    // filled by scoreWork()
    tier: "E", tierWhy: [], relevant: false, relevanceWhy: "",
  };
}

/** Batch-fetch every distinct source in one or two calls, not one per work. */
async function fetchSources(){
  const ids = [...new Set(S.works.map(w => w.sourceId).filter(Boolean))];
  for (let i = 0; i < ids.length; i += 50){
    const batch = ids.slice(i, i + 50);
    const d = await getJSON(oa("/sources", {
      filter: "ids.openalex:" + batch.join("|"),
      per_page: 50,
    }), { optional:true });
    (d?.results || []).forEach(s => S.sources.set(shortId(s.id), s));
  }
}

/** OpenAlex frequently has no `source` for book chapters and monographs — it
    knows the chapter but not the book it sits in. Crossref does. Resolving
    these matters for evaluation: without it, forty chapters of one monograph
    read as forty separate publications. */
async function enrichFromCrossref(onStep){
  const targets = S.works.filter(w => w.doi && !w.sourceId && !w.paratext);
  if (!targets.length) return;

  // One cheap call per DOI prefix gives the publisher for everything under
  // it — a floor of evidence that survives any per-work lookup failing.
  const prefixes = [...new Set(targets.map(w => w.doi.split("/")[0]))];
  const pubByPrefix = new Map();
  await Promise.all(prefixes.map(async pre => {
    const d = await getJSON(CFG.crossref + "/prefixes/" + pre, { optional:true });
    if (d?.message?.name) pubByPrefix.set(pre, d.message.name);
  }));

  // Then per-work detail, in small waves so Crossref does not throttle us.
  let done = 0;
  const list = targets.slice(0, 150);
  for (let i = 0; i < list.length; i += 6){
    await Promise.all(list.slice(i, i + 6).map(async w => {
      const d = await getJSON(CFG.crossref + "/works/" + encodeURI(w.doi), { optional:true });
      done++;
      const m = d?.message;
      if (m){
        const container = (m["container-title"] || []).filter(Boolean)[0] || null;
        if (container){ w.container = container; w.venue = container; w.venueFrom = "crossref"; }
        if (m.publisher) w.publisher = m.publisher;
        if (m.ISBN?.length) w.isbn = m.ISBN;
        if (!w.pages && m.page) w.pages = m.page;
        // A monograph has no container of its own. Naming its title as the
        // venue printed the title twice; name the publisher instead.
        if (!container && /book|monograph/i.test(m.type || "")){
          w.container = w.title; w.venueFrom = "crossref";
          w.venue = m.publisher ? `Monograph · ${m.publisher}` : "Monograph";
        }
      }
      if (!w.publisher){
        const pub = pubByPrefix.get(w.doi.split("/")[0]);
        if (pub){ w.publisher = pub; w.venueFrom = w.venueFrom || "crossref-prefix"; }
      }
    }));
    onStep(t("Resolving books and chapters… {n}/{total}", { n:Math.min(done, list.length), total:list.length }));
    if (i + 6 < list.length) await sleep(120);
  }
}

/** ORCID records peer reviews grouped by the reviewed journal's ISSN.
    Resolve those ISSNs to journal names — that is the useful part. */
async function resolveReviews(rec){
  const groups = rec["activities-summary"]?.["peer-reviews"]?.group || [];
  const out = [];
  for (const g of groups){
    const ext  = (g["external-ids"]?.["external-id"] || [])[0];
    const raw  = ext?.["external-id-value"] || "";
    const issn = raw.startsWith("issn:") ? raw.slice(5) : null;
    const items = g["peer-review-group"] || [];
    let name = issn ? "ISSN " + issn : "Undisclosed venue";
    let sid = null;
    if (issn){
      const d = await getJSON(oa("/sources/issn:" + issn), { optional:true });
      if (d?.display_name){ name = d.display_name; sid = shortId(d.id); S.sources.set(sid, d); }
    }
    const years = items
      .map(it => it["peer-review-summary"]?.["completion-date"]?.year?.value)
      .filter(Boolean).map(Number);
    out.push({ issn, name, sourceId:sid, count:items.length, years });
  }
  return out.sort((a, b) => b.count - a.count);
}

/** DOAJ is authoritative for its own listing; OpenAlex's flag can lag. */
async function checkDoaj(){
  const issns = [...new Set(
    [...S.sources.values()]
      .filter(s => s.type === "journal")
      .flatMap(s => s.issn || [])
      .filter(Boolean)
  )];
  await Promise.all(issns.slice(0, 40).map(async issn => {
    const d = await getJSON(
      CFG.doaj + "/search/journals/issn%3A" + encodeURIComponent(issn),
      { optional:true }
    );
    const hit = d?.results?.[0];
    if (hit) S.doaj.set(issn, { seal: !!hit.seal, title: hit.bibjson?.title || "" });
  }));
}

/* ---------- 6. Scoring ---------------------------------------------- */
/* Two independent judgements per work:
     tier      — how well-indexed the venue is (the "priority of indexing")
     relevant  — whether the work is in Romani studies
   Both record *why*, so the screen can always show its own reasoning. The
   reasons are written in the interface language; a language switch
   re-scores. */

/** Never let a render crash on an unscored work. */
const tierOf  = w => TIERS[w?.tier] ? w.tier : "E";
const tierRank = w => TIERS[tierOf(w)].rank;

const TIERS = {
  A: { label:"A", name:"Core indexed",      rank:5 },
  B: { label:"B", name:"Indexed journal",   rank:4 },
  C: { label:"C", name:"Journal, limited",  rank:3 },
  D: { label:"D", name:"Book / chapter",    rank:2 },
  E: { label:"E", name:"Repository / other",rank:1 },
};
const tierName = k => t(TIERS[k]?.name || "");

/** DOAJ's own answer for a venue, by any of its ISSNs. */
function doajFor(w){
  for (const issn of (w.issnAll?.length ? w.issnAll : [w.issn])) if (issn && S.doaj.has(issn)) return S.doaj.get(issn);
  return null;
}

/** User assertions for a venue, looked up by any of its ISSNs. */
function registryFor(work){
  for (const issn of (work.issnAll?.length ? work.issnAll : [work.issn]))
    if (issn && S.registry[issn]) return { issn, rec: S.registry[issn] };
  return { issn: work.issn, rec: null };
}

function scoreWork(w){
  const src = w.sourceId ? S.sources.get(w.sourceId) : null;
  const { rec } = registryFor(w);
  const why = [];
  let tier;

  // --- Hand-verified assertions outrank every machine signal. -----------
  const manual = [];
  if (rec?.scopus) manual.push("Scopus");
  if (rec?.wos)    manual.push("Web of Science");
  if (rec?.erih)   manual.push("ERIH PLUS");
  if (rec?.mein && rec.mein !== "—" && rec.mein !== "0") manual.push(t("MEiN {n} pts", { n:rec.mein }));

  const isJournal = (src?.type === "journal") || (w.venueType === "journal");
  const isRepo    = src?.is_preprint_repository || src?.type === "repository";
  const isBook    = /book|chapter|monograph|dissertation/i.test(w.type);
  const srcH      = src?.summary_stats?.h_index ?? 0;
  const dj        = doajFor(w);
  const inDoaj    = !!dj || src?.is_in_doaj;
  const isCore    = src?.is_core;

  if (manual.length && isJournal){
    tier = "A";
    why.push(t("Listed in {list}", { list:manual.join(", ") }) + " " +
             (rec?.seeded ? t("(SROM seed list — confirm it in Venues)") : t("(your verdict)")));
  } else if (isJournal && inDoaj && isCore){
    tier = "A";
    why.push(dj ? t("DOAJ-listed (confirmed via DOAJ)") : t("DOAJ-listed (OpenAlex)"));
    why.push(t("OpenAlex core collection"));
  } else if (isJournal && (inDoaj || isCore || srcH >= 20)){
    tier = "B";
    if (inDoaj) why.push(dj ? t("DOAJ-listed (confirmed)") : t("DOAJ-listed (OpenAlex)"));
    if (isCore) why.push(t("OpenAlex core collection"));
    if (srcH >= 20) why.push(t("Venue h-index {h}", { h:srcH }));
  } else if (isJournal && (w.issn || w.publisher)){
    tier = "C";
    why.push(w.issn ? t("Journal with registered ISSN") : t("Journal with named publisher"));
    if (srcH) why.push(t("Venue h-index {h}", { h:srcH }));
    if (src?.is_ojs) why.push(t("Runs on OJS"));
  } else if ((isBook || w.publisher) && w.publisher && !isRepo){
    tier = "D";
    why.push(t("Published by {p}", { p:w.publisher }));
    if (w.container && w.container !== w.title) why.push(t("Chapter in “{title}”", { title:w.container }));
    if (w.isbn?.length) why.push("ISBN " + w.isbn[0]);
  } else if (isBook){
    tier = "E";
    why.push(t("Book-form publication, but no publisher could be verified"));
  } else {
    tier = "E";
    why.push(isRepo ? t("Repository or preprint deposit") : t("No indexed venue identified"));
  }

  // Provenance markers that travel with the work itself.
  if (w.indexedIn.includes("crossref")) why.push(t("DOI registered with Crossref"));
  if (w.indexedIn.includes("pubmed"))   why.push(t("Indexed in PubMed"));
  if (w.indexedIn.includes("doaj"))     why.push(t("Article indexed in DOAJ"));
  if (!w.doi) why.push(t("No DOI — citation cannot be resolved"));

  w.tier = tier;
  w.tierWhy = why;
  w.manualBadges = manual;
  w.manualSeed = !!rec?.seeded;
  w.doajSeal = !!dj?.seal;

  relevanceOf(w);
}

/** Is this work in Romani studies, and on what evidence? Shared by the
    dossier and the comparison so both apply the identical test. */
function relevanceOf(w){
  const topicHit = w.topics.some(t => FIELD.topicIds.includes(t.id));
  const lexHit   = inLexicon(w.title) || inLexicon(w.abstract);
  const venueHit = inLexicon(w.venue);
  w.relevant = topicHit || lexHit || venueHit;
  w.relevanceWhy =
      topicHit ? t("OpenAlex topic: Romani and Gypsy Studies")
    : venueHit ? t("Published in a Romani-studies venue")
    : lexHit   ? t("Field terminology in title or abstract")
    : "";
}

/* ---------- 6b. Expertise profile ------------------------------------ */
/* What, inside Romani studies, is this person actually an expert in?
   Themes are ranked by share of their in-field output and split into tiers,
   so "core" means sustained work rather than a single paper. Recency is
   carried through because a theme last touched in 1998 is not current
   expertise. */

/** The strongest two themes a text touches — shared by the expertise
    profile and the reviewer finder, so both read a text the same way. */
function themeHits(hay, max = 2){
  const h = String(hay || "").toLowerCase();
  return THEMES
    .map(th => ({ th, n: th.cues.reduce((a, c) => a + (h.includes(c) ? 1 : 0), 0) }))
    .filter(x => x.n > 0)
    .sort((a, b) => b.n - a.n)
    .slice(0, max);
}

function computeExpertise(works = S.works){
  const inField = works.filter(w => !w.paratext && w.relevant);
  const thisYear = new Date().getFullYear();

  const rows = THEMES.map(th => ({
    id:th.id, label:th.label, works:[], cites:0, last:null, first:null, recent:0,
  }));
  const byId = new Map(rows.map(r => [r.id, r]));

  for (const w of inField){
    const hay = [w.title, w.abstract, w.venue, (w.keywords || []).join(" "),
                 w.topics.map(tp => tp.name).join(" ")].join(" ");

    // Score every theme, then keep only the strongest two. A single article
    // touches half a dozen themes in passing; counting all of them makes
    // everything look like core expertise and the profile says nothing.
    for (const h of themeHits(hay)){
      const r = byId.get(h.th.id);
      r.works.push(w);
      r.cites += w.cites;
      if (w.year){
        r.last  = Math.max(r.last  ?? w.year, w.year);
        r.first = Math.min(r.first ?? w.year, w.year);
        if (w.year >= thisYear - 8) r.recent++;
      }
    }
  }

  const total = inField.length;
  const scored = rows
    .filter(r => r.works.length)
    .map(r => ({ ...r, n:r.works.length, share: total ? r.works.length / total : 0 }))
    .sort((a,b) => b.n - a.n || b.cites - a.cites);

  // Tiering: sustained presence, not a single paper — and capped, because a
  // list of twelve "core" specialisms characterises nobody.
  const thin = total < 5;
  scored.forEach((r, i) => {
    if (thin){ r.tier = "peripheral"; return; }
    r.tier = (i < 3 && r.n >= 3 && r.share >= 0.20) ? "core"
           : (i < 7 && r.n >= 2 && r.share >= 0.10) ? "secondary"
           : "peripheral";
  });

  // Machine-assigned topics as an independent cross-check on the term matching.
  const topicCount = new Map();
  for (const w of inField)
    for (const tp of w.topics){
      if (FIELD.topicIds.includes(tp.id)) continue;
      topicCount.set(tp.name, (topicCount.get(tp.name) || 0) + 1);
    }
  const topics = [...topicCount.entries()]
    .sort((a,b) => b[1] - a[1]).slice(0, 6)
    .map(([name, n]) => ({ name, n }));

  return {
    total, thin, all: scored,
    core:       scored.filter(r => r.tier === "core"),
    secondary:  scored.filter(r => r.tier === "secondary"),
    peripheral: scored.filter(r => r.tier === "peripheral").slice(0, 8),
    topics,
  };
}

/** "a", "a and b", "a, b and c" — in the interface language. */
function joinList(names){
  const and = I18N.lang === "pl" ? " i " : " and ";
  if (names.length <= 1) return names[0] || "";
  if (names.length === 2) return names.some(n => n.includes(and)) ? names.join(", ") : names.join(and);
  return names.slice(0, -1).join(", ") + (I18N.lang === "pl" ? " i " : ", and ") + names[names.length - 1];
}

/** One-line characterisation for the top of the dossier. Phrased without
    a noun for the person, so it reads right in Polish whoever it describes. */
function expertiseHeadline(x, sm){
  if (!x.total) return t("No indexed work in Romani studies.");
  const depth = sm.relevantPct >= 60 ? t("Field specialist")
              : sm.relevantPct >= 20 ? t("Substantially engaged with the field")
              : t("Occasional contributor to the field");
  if (x.thin) return t("headline.thin", { depth, n:x.total, works:tn(x.total, "in-field work") });
  const names = x.core.slice(0, 3).map(r => themeShort(r.id));
  if (!names.length) return t("headline.even", { depth });
  return t("headline.main", { depth, list:joinList(names) });
}

/** The headline for a saved record, in the current language — rebuilt from
    what the record holds rather than the sentence stored with it. */
function recordHeadline(r){
  if (r.light || r.relevantPct == null) return "";
  const ids = r.coreIds || (r.core || []).map(l => themeByLabel(l)?.id).filter(Boolean);
  const total = r.inField ?? 0;
  return expertiseHeadline({ total, thin: total < 5, core: ids.map(id => ({ id })) }, { relevantPct:r.relevantPct });
}

/* ---------- 7. Aggregate metrics ------------------------------------- */

/** h-index from a work list — needed when the record merges several profiles. */
function hIndexOf(works){
  const c = works.map(w => w.cites).sort((a, b) => b - a);
  let h = 0; while (h < c.length && c[h] >= h + 1) h++;
  return h;
}

function computeSummary(){
  const w  = S.works.filter(x => !x.paratext);
  const rel = w.filter(x => x.relevant);
  const yrs = w.map(x => x.year).filter(Boolean).sort((a,b)=>a-b);
  const byTier = {};
  for (const k of Object.keys(TIERS)) byTier[k] = w.filter(x => x.tier === k).length;

  const fw = w.map(x => x.fwci).filter(v => typeof v === "number");
  const meanFwci = fw.length ? fw.reduce((a,b)=>a+b,0) / fw.length : null;

  // Recent = last 5 complete years; a proxy for whether they are still active.
  const thisYear = new Date().getFullYear();
  const recent = w.filter(x => x.year && x.year >= thisYear - 5);

  return {
    total: w.length,
    relevant: rel.length,
    relevantPct: pct(rel.length, w.length),
    relCited: rel.reduce((a,b)=>a+b.cites,0),
    cites: w.reduce((a,b)=>a+b.cites,0),
    hIndex: S.siblings?.length ? hIndexOf(w) : (S.author?.summary_stats?.h_index ?? null),
    i10: S.siblings?.length ? w.filter(x => x.cites >= 10).length : (S.author?.summary_stats?.i10_index ?? null),
    firstYear: yrs[0] ?? null,
    lastYear: yrs[yrs.length-1] ?? null,
    span: yrs.length ? yrs[yrs.length-1] - yrs[0] + 1 : 0,
    byTier,
    topTierPct: pct(byTier.A + byTier.B, w.length),
    oa: w.filter(x=>x.oa).length,
    oaPct: pct(w.filter(x=>x.oa).length, w.length),
    doiPct: pct(w.filter(x=>x.doi).length, w.length),
    solo: w.filter(x=>x.nAuthors === 1).length,
    firstAuthor: w.filter(x=>x.authorPos === "first").length,
    venues: new Set(w.map(x=>x.venue).filter(v=>v!==NO_VENUE)).size,
    meanFwci,
    recent: recent.length,
    recentRelevant: recent.filter(x=>x.relevant).length,
    retracted: w.filter(x=>x.retracted).length,
    langs: [...new Set(w.map(x=>x.lang).filter(Boolean))],
  };
}

/** Per-year publication counts, for the sparkline. */
function yearHistogram(){
  const m = new Map();
  S.works.filter(w=>w.year && !w.paratext).forEach(w => m.set(w.year, (m.get(w.year)||0)+1));
  const yrs = [...m.keys()].sort((a,b)=>a-b);
  if (!yrs.length) return [];
  const out = [];
  for (let y = yrs[0]; y <= yrs[yrs.length-1]; y++) out.push({ year:y, n:m.get(y)||0 });
  return out;
}

/* ---------- 8. Editorial flags --------------------------------------- */
/* Things an editor should look at before deciding. Deliberately phrased
   as observations, never as verdicts. */

function computeFlags(sm){
  const f = [];
  const A = S.author;
  const add = (sev, ic, key, vars) => f.push({ sev, ic, t:t(key + ".t", vars), d:t(key + ".d", vars) });

  if (sm.retracted) add("high", "⛔", "flag.retracted", { n:sm.retracted, works:tw(sm.retracted, "work") });

  if (!A?.orcid && S.orcidInferred) add("med", "≈", "flag.orcidInferred");
  else if (!A?.orcid)                add("med", "◯", "flag.noOrcid");
  else                               add("ok",  "✓", "flag.orcidOk");

  if (S.orcid){
    const orcidWorks = orcidWorkCount();
    const delta = orcidWorks - sm.total;
    if (Math.abs(delta) > Math.max(15, sm.total * 0.35))
      add("med", "≠", "flag.sizeDiff", { orcid:num(orcidWorks), oa:num(sm.total) });
  }

  if (sm.total && sm.topTierPct < 20 && sm.total >= 10) add("med", "△", "flag.lowTier", { pct:sm.topTierPct });
  if (sm.doiPct < 50 && sm.total >= 10)                  add("med", "⚯", "flag.noDoi", { pct:100 - sm.doiPct });

  if (sm.relevantPct >= 60)      add("ok",  "◆", "flag.specialist", { pct:sm.relevantPct });
  else if (sm.relevantPct >= 20) add("ok",  "◇", "flag.adjacent",   { pct:sm.relevantPct });
  else if (sm.total >= 5)        add("med", "○", "flag.limited",    { pct:sm.relevantPct });

  const thisYear = new Date().getFullYear();
  if (sm.lastYear && thisYear - sm.lastYear >= 6) add("med", "⏳", "flag.inactive", { year:sm.lastYear });

  if (S.siblings?.length){
    const extra = S.siblings.reduce((a, x) => a + (x.works_count || 0), 0);
    add("ok", "⊕", "flag.merged", { n:S.siblings.length + 1, works:tn(extra, "work") });
  }

  if (S.wikidata && S.wikidata.matchedBy === "name") add("med", "⑂", "flag.wdName", { id:S.wikidata.id });

  if (S.reviews.length) add("ok", "✎", "flag.reviews", { venues:tn(S.reviews.length, "venue") });

  const chapters = S.works.filter(w => !w.paratext && /chapter/i.test(w.type) && w.container);
  if (chapters.length >= 5){
    const books = new Set(chapters.map(w => w.container));
    if (chapters.length >= books.size * 3){
      const top = [...books].slice(0, 3).join("”, “");
      add("med", "❏", "flag.chapters", { chapters:tn(chapters.length, "chapter"), books:tn(books.size, "book"), nc:chapters.length, nb:books.size,
                                         top, monographs:tn(books.size, "monograph") });
    }
  }

  const unverified = S.works.filter(w => !w.paratext && !w.sourceId && !w.publisher).length;
  if (unverified >= Math.max(5, S.works.length * 0.15)) add("med", "?", "flag.unverified", { works:tn(unverified, "work") });

  const nameCount = S.candidateCount || 0;
  if (nameCount > 3) add("med", "⑂", "flag.nameCount", { n:nameCount });

  return f;
}

/* ---------- 9. Scholarly profile links ------------------------------- */
/* Three classes, always visually distinct:
     resolved — an identifier that points at this exact person, from ORCID,
                Wikidata or a DOI lookup
     pinned   — you recorded it by hand, because no open source carries it
     search   — a pre-built query, shown only where the destination can
                actually hold something about a person

   Nothing appears here that cannot show anything. ERIH PLUS indexes
   journals, not people, so it belongs on the Venues tab and nowhere else. */

function profileLinks(){
  const A = S.author;
  const name = A.display_name || "";
  const q = encodeURIComponent(name);
  const pins = myPins();
  const out = [];
  const seen = new Set();

  const add = (kind, label, sub, url) => {
    if (!url) return;
    const k = label.toLowerCase();
    if (seen.has(k)) return;
    seen.add(k);
    out.push({ kind, label, sub, url });
  };

  add("resolved", "OpenAlex", shortId(A.id), A.id);

  const orcid = orcidOf(A.orcid) || (S.orcidInferred && S.orcid
    ? S.orcid["orcid-identifier"]?.path : null);
  if (orcid)
    add(S.orcidInferred ? "inferred" : "resolved", "ORCID",
        S.orcidInferred ? orcid + " · " + t("matched by name — verify") : orcid,
        "https://orcid.org/" + orcid);

  // --- Identifiers the scholar attached to their own ORCID record ---------
  const ext = S.orcid?.person?.["external-identifiers"]?.["external-identifier"] || [];
  for (const e of ext){
    const type = e["external-id-type"] || "";
    const val  = e["external-id-value"] || "";
    if (!val) continue;
    if (/scopus/i.test(type))
      add("resolved", "Scopus", t("Author ID {id}", { id:val }),
          "https://www.scopus.com/authid/detail.uri?authorId=" + encodeURIComponent(val));
    else if (/researcher\s*id/i.test(type))
      add("resolved", "Web of Science", "ResearcherID " + val,
          "https://www.webofscience.com/wos/author/record/" + encodeURIComponent(val));
    else if (e["external-id-url"]?.value)
      add("resolved", type, val, e["external-id-url"].value);
  }

  // --- Wikidata: the one open hub that federates profile identifiers ------
  if (S.wikidata){
    const wdKind = S.wikidata.matchedBy === "ORCID" ? "resolved" : "inferred";
    const wdSub  = S.wikidata.matchedBy === "ORCID" ? t("via Wikidata") : t("via Wikidata — name match, verify");
    add(wdKind, "Wikidata",
        S.wikidata.id + (S.wikidata.description ? " · " + S.wikidata.description : "")
          + (wdKind === "inferred" ? " · " + t("name match") : ""),
        "https://www.wikidata.org/wiki/" + S.wikidata.id);
    for (const def of Object.values(WD_PROPS)){
      const v = S.wikidata.ids[def.key];
      if (v && def.key !== "orcid") add(wdKind, t(def.label), wdSub, def.url(v));
    }
  }

  // --- Semantic Scholar, resolved through a DOI rather than by name ------
  if (S.s2)
    add("resolved", "Semantic Scholar",
        t("{n} papers · matched via DOI", { n:S.s2.paperCount ?? "?" }),
        "https://www.semanticscholar.org/author/" + S.s2.authorId);

  // --- Pages the scholar published on their own ORCID record -------------
  for (const u of (S.orcid?.person?.["researcher-urls"]?.["researcher-url"] || []).slice(0, 6)){
    const href = u.url?.value;
    if (!href) continue;
    let host = href;
    try { host = new URL(href).hostname.replace(/^www\./, ""); } catch (e) {}
    add("resolved", u["url-name"]?.value || host, t("from ORCID"), href);
  }

  // --- Anything you pinned by hand ---------------------------------------
  for (const def of PINNABLE){
    const v = pins[def.key];
    if (v) add("pinned", t(def.label), t("pinned by you"), def.url(v));
  }

  // --- Searches, only where the destination holds scholar-level records ---
  const hasBooks  = S.works.some(w => /book|monograph|chapter/i.test(w.type));
  const isPolish  = (A.affiliations || []).some(a => a.institution?.country_code === "PL")
                 || S.works.some(w => w.lang === "pl");

  // Academia.edu and ResearchGate wall their own search behind a login;
  // a site-scoped web search reaches the public profile instead.
  if (!pins.academia && !S.wikidata?.ids?.academia)
    add("search", "Academia.edu", t("site search — no API exists"),
        "https://duckduckgo.com/?q=" + encodeURIComponent(`site:academia.edu "${name}"`));
  if (!pins.rg && !S.wikidata?.ids?.rg)
    add("search", "ResearchGate", t("site search — no API exists"),
        "https://duckduckgo.com/?q=" + encodeURIComponent(`site:researchgate.net "${name}"`));
  if (!pins.gscholar && !S.wikidata?.ids?.gscholar)
    add("search", "Google Scholar", t("profile search — no API exists"),
        "https://scholar.google.com/citations?hl=" + I18N.lang + "&view_op=search_authors&mauthors=" + q);
  // LinkedIn serves HTTP 999 to any automated request and its API is
  // partner-gated with no people search, so the profile itself is
  // unreachable. Wikidata carries the profile URL for a sizeable minority
  // of scholars; otherwise this is a search, or you pin it.
  if (!pins.linkedin && !S.wikidata?.ids?.linkedin)
    add("search", "LinkedIn", t("site search — profile data is not retrievable"),
        "https://duckduckgo.com/?q=" + encodeURIComponent(`site:linkedin.com/in "${name}"`));

  if (!pins.scopus && !S.wikidata?.ids?.scopus)
    add("search", "Scopus", t("needs a subscription to view"),
        "https://www.scopus.com/results/authorNamesList.uri?st1=" +
        encodeURIComponent(name.split(/\s+/).pop()) + "&st2=" + q);

  add("search", "Crossref", t("works filed under this name"),
      "https://search.crossref.org/search/works?q=" + q + "&from_ui=yes");

  // Library authority files only hold catalogued monograph authors.
  if (hasBooks){
    if (!S.wikidata?.ids?.viaf)
      add("search", "VIAF", t("name authority — monograph authors only"),
          "https://viaf.org/viaf/search?query=local.personalNames+all+%22" + q + "%22");
    add("search", "WorldCat", t("monographs and editions"),
        "https://search.worldcat.org/search?q=au%3A" + q);
  }

  // Polish national registries, only for scholars with a Polish footprint.
  if (isPolish){
    add("search", "PBN", t("Polish Science Base"),
        "https://pbn.nauka.gov.pl/core/#/search/scientists?searchText=" + q);
    add("search", "Nauka Polska", t("Polish researcher registry"),
        "https://nauka-polska.pl/#/profile/search?_k=lookup&query=" + q);
  }

  return out;
}
