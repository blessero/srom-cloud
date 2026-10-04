"use strict";

/* =====================================================================
   SROM Scholar Audit — shared core
   A toolkit for editors and researchers in Romani studies: check a
   scholar's standing, find reviewers without conflicts of interest, see
   who works on what, and keep a library of the people you work with.

   Design principle: every claim on screen carries its provenance.
   Machine-derived signals and hand-verified assertions are never
   allowed to look alike.

   Files, loaded in this order:
     i18n.js       interface language — t(), plurals, the Polish text
     core.js       configuration, utilities, dialogs, network, storage,
                   library, backup, stored dossiers, views
     scholar.js    one scholar's record: resolution, enrichment, scoring,
                   expertise, editorial notes, profile links
     dossier.js    the Check a scholar tool
     library.js    the Library and the relations map
     directory.js  the Field directory
     reviewers.js  the Reviewer finder
     app.js        masthead, navigation, settings, start-up
   ===================================================================== */

/* ---------- 0. Configuration ---------------------------------------- */

const CFG = {
  // OpenAlex "polite pool" — set your own email for higher rate limits.
  // Left blank by default so nothing is transmitted you didn't choose.
  mailto: "",
  openalex: "https://api.openalex.org",
  orcid:    "https://pub.orcid.org/v3.0",
  crossref: "https://api.crossref.org",
  doaj:     "https://doaj.org/api/v4",
  wikidata: "https://www.wikidata.org/w/api.php",
  s2:       "https://api.semanticscholar.org/graph/v1",
};

/* Wikidata is the only open, CORS-accessible hub that federates scholarly
   profile identifiers. Where a scholar has an item, these resolve to real
   profile pages — including Academia.edu, which publishes no API of its own.
   Where they don't, nothing here invents a link. */
const WD_PROPS = {
  P496:  { key:"orcid",     label:"ORCID",            url:v=>"https://orcid.org/"+v },
  P1153: { key:"scopus",    label:"Scopus",           url:v=>"https://www.scopus.com/authid/detail.uri?authorId="+v },
  P1053: { key:"wos",       label:"Web of Science",   url:v=>"https://www.webofscience.com/wos/author/record/"+v },
  P4012: { key:"s2",        label:"Semantic Scholar", url:v=>"https://www.semanticscholar.org/author/"+v },
  P2038: { key:"rg",        label:"ResearchGate",     url:v=>"https://www.researchgate.net/profile/"+v },
  P5715: { key:"academia",  label:"Academia.edu",     url:v=>/^https?:/.test(v)?v:"https://independent.academia.edu/"+v },
  P1960: { key:"gscholar",  label:"Google Scholar",   url:v=>"https://scholar.google.com/citations?user="+v },
  P214:  { key:"viaf",      label:"VIAF",             url:v=>"https://viaf.org/viaf/"+v },
  P213:  { key:"isni",      label:"ISNI",             url:v=>"https://isni.org/isni/"+String(v).replace(/\s/g,"") },
  P227:  { key:"gnd",       label:"GND (DNB)",        url:v=>"https://d-nb.info/gnd/"+v },
  P244:  { key:"loc",       label:"Library of Congress", url:v=>"https://id.loc.gov/authorities/names/"+v },
  P269:  { key:"idref",     label:"IdRef (Sudoc)",    url:v=>"https://www.idref.fr/"+v },
  P6634: { key:"linkedin",  label:"LinkedIn",         url:v=>/^https?:/.test(v)?v:"https://www.linkedin.com/in/"+v },
  P856:  { key:"website",   label:"Official website", url:v=>v },
};

/* Identifiers you can pin by hand when no open source carries them.
   Scopus and Academia.edu are the common cases: Elsevier serves no CORS
   headers at all, and Academia.edu has no API and forbids scraping. */
const PINNABLE = [
  { key:"email",    label:"Email",            ph:"only if you already know it",
    url:v=>"mailto:" + v.replace(/^mailto:/i, "") },
  { key:"scopus",   label:"Scopus Author ID", ph:"56111168700",
    url:v=>/^https?:/.test(v)?v:"https://www.scopus.com/authid/detail.uri?authorId="+v },
  { key:"academia", label:"Academia.edu",     ph:"gonzaga.academia.edu/Aostendorf",
    url:v=>/^https?:/.test(v)?v:"https://"+v.replace(/^\/+/,"") },
  { key:"gscholar", label:"Google Scholar ID",ph:"user id from the profile URL",
    url:v=>/^https?:/.test(v)?v:"https://scholar.google.com/citations?user="+v },
  { key:"rg",       label:"ResearchGate",     ph:"profile/Jane-Doe",
    url:v=>/^https?:/.test(v)?v:"https://www.researchgate.net/"+v.replace(/^\/+/,"") },
  { key:"wos",      label:"WoS ResearcherID", ph:"AAR-2927-2020",
    url:v=>/^https?:/.test(v)?v:"https://www.webofscience.com/wos/author/record/"+v },
  { key:"linkedin", label:"LinkedIn",         ph:"linkedin.com/in/jane-doe",
    url:v=>/^https?:/.test(v)?v:"https://www.linkedin.com/in/"+v.replace(/^.*linkedin\.com\/in\//,"").replace(/^\/+/,"") },
];

/* The field of record. OpenAlex topic T12595 is "Romani and Gypsy
   Studies"; the lexicon catches works that predate or sit outside that
   classification (older ethnography, Polish/German/French-language
   scholarship, etc.) where topic assignment is unreliable. */
const FIELD = {
  topicIds: ["T12595"],
  topicNames: ["Romani and Gypsy Studies"],
  lexicon: [
    "roma","romani","romany","romanies","rroma","gypsy","gypsies","sinti","kale",
    "kalderash","lovari","lovara","bergitka","polska roma","manouche","travellers",
    "romolog","romologia","romologic","cygan","cyganie","cygansk","zigeuner",
    "tsigane","tzigane","gitano","gitanos","ciganos","cigány","romské","romsk",
    "antigypsyism","antiziganism","antitsiganism","porajmos","romanes",
    "romani studies","gypsy studies","romani language","romani people"
  ],
};

/* Thematic map of Romani studies. Cues are deliberately multilingual —
   the field's literature is written in Polish, German, French, Bulgarian,
   Czech, Hungarian and Spanish as much as in English, and an English-only
   term list would systematically under-read Central and Eastern European
   scholars. Matching is substring-based over title, abstract, keywords and
   venue, so cues are chosen to be long enough not to collide.

   `short` completes "working mainly on …"; `grid` is the one-line label of
   the side-by-side grid; `pl…` are the Polish forms; `q` is what the Field
   directory sends to OpenAlex — whole words, since its search is not
   substring-based. */
const THEMES = [
  { id:"history", label:"History & archives", short:"history", grid:"History & archives",
    pl:"Historia i archiwa", plShort:"historia", plGrid:"Historia", cues:[
    "history","historical","historiograph","archive","archival","eighteenth","nineteenth",
    "seventeenth","medieval","early modern","century","geschichte","historia","histoire",
    "dzieje","istoriya","chronicle","manuscript","histor","archiw"],
    q:["history","historical","historiography","archive","archival","historia","geschichte","histoire","dzieje"] },
  { id:"holocaust", label:"Holocaust & genocide (Porajmos)", short:"the Holocaust", grid:"Holocaust (Porajmos)",
    pl:"Zagłada i ludobójstwo (Porajmos)", plShort:"Zagłada", plGrid:"Zagłada (Porajmos)", cues:[
    "holocaust","porajmos","samudaripen","genocide","nazi","auschwitz","concentration camp",
    "extermination","deportation","internment","zagłada","zaglada","völkermord","voelkermord",
    "shoah","wartime persecution","third reich","zagład","ludobój","obóz koncentr"],
    q:["holocaust","porajmos","samudaripen","genocide","auschwitz","nazi","\"concentration camp\"","zagłada","ludobójstwo","völkermord","shoah"] },
  { id:"slavery", label:"Slavery, serfdom & bondage", short:"slavery", grid:"Slavery & serfdom",
    pl:"Niewolnictwo, poddaństwo i zależność", plShort:"niewolnictwo", plGrid:"Niewolnictwo", cues:[
    "slavery","slaves","enslave","serfdom","bondage","robie","emancipation of the","abolition",
    "niewol","pańszczyź"],
    q:["slavery","slaves","enslavement","serfdom","bondage","abolition","robie","niewolnictwo"] },
  { id:"language", label:"Language & linguistics", short:"Romani linguistics", grid:"Language",
    pl:"Język i językoznawstwo", plShort:"językoznawstwo romskie", plGrid:"Język", cues:[
    "linguistic","language contact","dialect","grammar","lexicon","lexical","morpholog",
    "syntax","phonolog","bilingual","multilingual","sociolinguistic","romani language",
    "romanes","język","jezyk","sprache","corpus","języko","dialekt","gramaty","słownic",
    "dwujęzycz","wielojęzycz","leksyk"],
    q:["linguistic","linguistics","dialect","dialects","grammar","\"language contact\"","sociolinguistic","morphology","phonology","bilingual","romanes","język","sprache"] },
  { id:"literature", label:"Literature & writing", short:"literature", grid:"Literature",
    pl:"Literatura i piśmiennictwo", plShort:"literatura", plGrid:"Literatura", cues:[
    "literature","literary","poetry","poems","novel","fiction","autobiograph","memoir",
    "life writing","narrative voice","writers","authorship","literatura","literac","poezj",
    "powieś","wiersz"],
    q:["literature","literary","poetry","poems","novel","fiction","autobiography","memoir","literatura","poezja"] },
  { id:"arts", label:"Music, arts & performance", short:"music and the arts", grid:"Music & arts",
    pl:"Muzyka, sztuka i performans", plShort:"muzyka i sztuka", plGrid:"Muzyka i sztuka", cues:[
    "music","musical","song","dance","performance","theatre","theater","film","cinema",
    "visual art","photograph","festival","flamenco","instrument","folklore","muzy","taniec",
    "tańc","teatr","piosen","pieśn","sztuk","fotograf"],
    q:["music","musical","songs","dance","theatre","film","cinema","art","photography","flamenco","folklore","muzyka","teatr"] },
  { id:"education", label:"Education & schooling", short:"education", grid:"Education",
    pl:"Edukacja i szkolnictwo", plShort:"edukacja", plGrid:"Edukacja", cues:[
    "education","school","pupil","student","teacher","teaching","curriculum","classroom",
    "literacy","desegregation of school","enrolment","enrollment","edukacja","szkoł","bildung",
    "edukac","szkol","uczni","uczeń","nauczyc","oświat"],
    q:["education","school","schools","schooling","pupils","teachers","curriculum","literacy","edukacja","szkoła","bildung"] },
  { id:"health", label:"Health & public health", short:"health", grid:"Health",
    pl:"Zdrowie i zdrowie publiczne", plShort:"zdrowie", plGrid:"Zdrowie", cues:[
    "health","medical","medicine","disease","epidemiolog","vaccin","mortality","morbidity",
    "genetic","hereditary","nutrition","mental health","healthcare","clinical","patient",
    "zdrow","chorob","medycz","szczepi","umieralno"],
    q:["health","medical","disease","epidemiology","vaccination","mortality","genetic","healthcare","zdrowie"] },
  { id:"migration", label:"Migration & mobility", short:"migration", grid:"Migration & mobility",
    pl:"Migracje i mobilność", plShort:"migracje", plGrid:"Migracje", cues:[
    "migration","migrant","mobility","nomad","itinerant","diaspora","asylum","refugee",
    "travelling","traveling","sedentar","settlement policy","emigration","immigration","border",
    "migrac","migran","emigrac","imigrac","uchodźc","koczown"],
    q:["migration","migrants","mobility","nomadism","diaspora","asylum","refugees","emigration","immigration","migracja","migracje"] },
  { id:"antigypsyism", label:"Antigypsyism & racism", short:"antigypsyism", grid:"Antigypsyism & racism",
    pl:"Antycyganizm i rasizm", plShort:"antycyganizm", plGrid:"Antycyganizm", cues:[
    "antigypsyism","anti-gypsyism","antiziganism","antitsiganism","racism","racial","racializ",
    "racialis","prejudice","stereotype","discriminat","stigma","hate speech","othering",
    "exclusion","xenophob","rasism","antycygan","dyskrymin","rasizm","rasist","uprzedze",
    "wyklucz","mowa nienawiści"],
    q:["antigypsyism","antiziganism","racism","discrimination","prejudice","stereotypes","stigma","\"hate speech\"","antycyganizm","dyskryminacja","rasizm"] },
  { id:"policy", label:"Policy, inclusion & development", short:"policy and inclusion work", grid:"Policy & inclusion",
    pl:"Polityka, inkluzja i rozwój", plShort:"polityka publiczna i inkluzja", plGrid:"Polityka i inkluzja", cues:[
    "policy","policies","inclusion","integration","strateg","framework","european union",
    "programme","development project","intervention","governance","municipal","reform",
    "polityk","integrac","inkluzj","program"],
    q:["policy","policies","inclusion","integration","strategy","\"European Union\"","governance","programme","polityka","integracja"] },
  { id:"law", label:"Law, citizenship & rights", short:"law and citizenship", grid:"Law & citizenship",
    pl:"Prawo, obywatelstwo i prawa człowieka", plShort:"prawo i obywatelstwo", plGrid:"Prawo", cues:[
    "legal","law","legislation","statute","citizenship","stateless","court","judicial",
    "litigation","human rights","constitutional","tribunal","jurisprudence","decree","regulation",
    "prawn","ustaw","obywatel","sądow","praw człowieka","praw mniejszo"],
    q:["law","legal","legislation","citizenship","statelessness","court","\"human rights\"","rights","prawo","obywatelstwo"] },
  { id:"identity", label:"Identity, ethnography & community", short:"ethnography", grid:"Identity & ethnography",
    pl:"Tożsamość, etnografia i społeczność", plShort:"etnografia", plGrid:"Tożsamość i etnografia", cues:[
    "identity","ethnograph","fieldwork","anthropolog","community","kinship","family",
    "belonging","ethnicity","group boundar","self-identification","tradition","custom",
    "tożsamoś","etnograf","społecznoś","pokrewieńs","rodzin","tradycj","zwyczaj"],
    q:["identity","ethnography","fieldwork","anthropology","community","kinship","ethnicity","tożsamość","etnografia"] },
  { id:"media", label:"Media & representation", short:"media representation", grid:"Media",
    pl:"Media i reprezentacje", plShort:"reprezentacje medialne", plGrid:"Media", cues:[
    "media","representation","press","newspaper","journalis","discourse","portrayal",
    "image of","public opinion","television","broadcast","prasa","prasow","dyskurs","wizerun",
    "telewiz","medialn"],
    q:["media","representation","press","newspapers","journalism","discourse","television","prasa","dyskurs"] },
  { id:"gender", label:"Gender & women", short:"gender", grid:"Gender",
    pl:"Gender i kobiety", plShort:"gender", plGrid:"Gender", cues:[
    "gender","women","woman","feminis","marriage","bride","girl","masculin","patriarch",
    "kobiet","płeć","płci","małżeńs","męskoś","feminiz"],
    q:["gender","women","feminism","marriage","masculinity","kobiety","płeć"] },
  { id:"religion", label:"Religion & belief", short:"religion", grid:"Religion",
    pl:"Religia i wierzenia", plShort:"religia", plGrid:"Religia", cues:[
    "religio","church","pentecostal","evangelic","islam","muslim","christian","pilgrimage",
    "faith","conversion","ritual","sacred","religi","kości","zielonoświątk","wiara","wiary",
    "pielgrzym","obrzęd","rytuał"],
    q:["religion","religious","church","pentecostal","evangelical","islam","muslim","pilgrimage","religia","kościół"] },
  { id:"housing", label:"Housing, settlement & segregation", short:"housing", grid:"Housing & segregation",
    pl:"Mieszkalnictwo, osadnictwo i segregacja", plShort:"mieszkalnictwo", plGrid:"Mieszkalnictwo", cues:[
    "housing","settlement","slum","ghetto","segregat","neighbourhood","neighborhood",
    "eviction","mahala","encampment","spatial","urban","dwelling","mieszkaniow","osiedl",
    "getto","segregac","eksmis"],
    q:["housing","settlement","settlements","slum","ghetto","segregation","neighbourhood","eviction","mahala","osiedle","segregacja"] },
  { id:"labour", label:"Labour, economy & poverty", short:"labour", grid:"Labour & poverty",
    pl:"Praca, gospodarka i ubóstwo", plShort:"praca i gospodarka", plGrid:"Praca i ubóstwo", cues:[
    "labour","labor","employment","unemploy","occupation","craft","trade","economic",
    "economy","poverty","welfare","income","livelihood","begging","zatrudni","bezroboc",
    "ubóstw","bieda","gospodar","rzemiosł"],
    q:["labour","labor","employment","unemployment","economy","poverty","welfare","income","livelihood","ubóstwo","bezrobocie"] },
  { id:"demography", label:"Demography & census", short:"demography", grid:"Demography",
    pl:"Demografia i spisy", plShort:"demografia", plGrid:"Demografia", cues:[
    "census","demograph","population","statistic","enumerat","fertility","household survey",
    "spis ludno","spis powsz","demograf","ludnoś","dzietnoś"],
    q:["census","demography","demographic","population","statistics","fertility","demografia","spis"] },
  { id:"activism", label:"Activism, politics & representation", short:"activism", grid:"Activism & politics",
    pl:"Aktywizm, polityka i reprezentacja", plShort:"aktywizm", plGrid:"Aktywizm", cues:[
    "activism","activist","movement","civil society","ngo","political participation",
    "mobilisation","mobilization","emancipat","self-organis","self-organiz","leadership",
    "party politics","nationalism","aktywi","stowarzysz","mobilizac","przywódc","nacjonaliz",
    "partycypac"],
    q:["activism","activists","movement","\"civil society\"","ngo","mobilisation","mobilization","\"political participation\"","leadership","nationalism","aktywizm"] },
];
const themeById    = id => THEMES.find(t => t.id === id);
const themeByLabel = s  => THEMES.find(t => t.label === s || t.pl === s);
const themeName  = id => { const t = themeById(id); return !t ? id : I18N.lang === "pl" ? t.pl : t.label; };
const themeShort = id => { const t = themeById(id); return !t ? id : I18N.lang === "pl" ? t.plShort : t.short; };
const themeGridLabel = id => { const t = themeById(id); return !t ? id : I18N.lang === "pl" ? t.plGrid : t.grid; };

/* Venues whose ISSN we can recognise without a lookup — the field's core
   journals. Used only to seed the registry with sensible starting values;
   everything here remains user-editable and is labelled as a seed. */
// Only claims checked against a published source; everything else is left for
// you to record. Romani Studies: Scopus and WoS (AHCI, SSCI) per its listing.
// Critical Romani Studies: DOAJ only, which the tool detects by itself.
// Studia Romologica: 0 MEiN points since July 2023.
const SEED_VENUES = {
  "1528-0748": { name:"Romani Studies",          erih:false, scopus:true,  wos:true  },
  "1757-2274": { name:"Romani Studies",          erih:false, scopus:true,  wos:true  },
  "1689-4758": { name:"Studia Romologica",       erih:false, scopus:false, wos:false, mein:"0" },
};

/* ---------- 1. Small utilities -------------------------------------- */

const $  = (s, r=document) => r.querySelector(s);
const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));

function esc(s){
  return String(s ?? "").replace(/[&<>"']/g, c =>
    ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c]));
}
const shortId  = u => String(u ?? "").split("/").pop();
/** OpenAlex repeats many repository names as "Name (Name)". */
const tidyVenue = n => {
  const s = String(n ?? "").trim();
  const m = s.match(/^(.+?)\s*\((.+)\)$/);
  return (m && m[1].trim() === m[2].trim()) ? m[1].trim() : s;
};
const orcidOf  = u => String(u ?? "").replace(/^https?:\/\/orcid\.org\//, "");
const doiOf    = u => String(u ?? "").replace(/^https?:\/\/(dx\.)?doi\.org\//, "");
const num      = n => (n ?? 0).toLocaleString(LOCALE());
const pct      = (a, b) => (!b ? 0 : Math.round((a / b) * 100));
const THIS_YEAR = new Date().getFullYear();

/* Venue names are data, and two of them are sentinels the code tests for;
   they are translated only where they are shown. */
const NO_VENUE = "No identified venue";
function venueLabel(v){
  if (v === NO_VENUE) return t(NO_VENUE);
  if (/^Monograph( · |$)/.test(v)) return t("Monograph") + v.slice(9);
  return v;
}

/** A country code as a name in the interface language. */
function countryName(code){
  if (!code) return "";
  try { return new Intl.DisplayNames([LOCALE()], { type:"region" }).of(String(code).toUpperCase()) || code; }
  catch (e) { return code; }
}

/** Does this text look like it belongs to the field? */
function inLexicon(text){
  const s = " " + String(text ?? "").toLowerCase().replace(/[^\p{L}\s]/gu, " ") + " ";
  return FIELD.lexicon.some(k => s.includes(" " + k) || s.includes(k + " "));
}

/** OpenAlex stores abstracts as an inverted index; rebuild the text. */
function deInvert(idx){
  if (!idx) return "";
  const out = [];
  for (const [word, positions] of Object.entries(idx))
    for (const p of positions) out[p] = word;
  return out.join(" ");
}

/* ---------- 1b. Dialogs and notices -------------------------------- */
/* Native prompt/alert/confirm are unstyled, block the page, and some
   browsers suppress them outright in installed apps — unacceptable on a
   public tool. One <dialog>, three shapes. */

function openDialog(inner){
  const d = $("#dlg");
  d.innerHTML = `<form method="dialog">${inner}</form>`;
  d.returnValue = "";
  d.showModal();
  return d;
}
/* The answer comes from the form's submit event, which fires synchronously on
   the click. The dialog's own "close" event is delivered later as a task, and
   browsers defer it while a page is hidden — a tap followed by an app switch
   would leave the answer pending. "cancel" (Esc) and "close" remain fallbacks. */
const closed = d => new Promise(res => {
  let done = false;
  const finish = v => { if (!done){ done = true; res(v); } };
  d.querySelector("form").addEventListener("submit", e => finish(e.submitter?.value ?? ""), { once:true });
  d.addEventListener("cancel", () => finish(""), { once:true });
  d.addEventListener("close", () => finish(d.returnValue), { once:true });
});

/** Confirm, or ask for a value when `input` is given. Resolves true/false,
    or the entered string / null. The primary button comes first in the DOM
    so Enter submits it; the row is reversed visually. */
async function ask({ title, text = "", ok = t("OK"), cancel = t("Cancel"), danger = false, input = null }){
  const field = input ? (input.multiline
    ? `<textarea name="v" placeholder="${esc(input.placeholder || "")}">${esc(input.value || "")}</textarea>`
    : `<input type="text" name="v" value="${esc(input.value || "")}" placeholder="${esc(input.placeholder || "")}" autocomplete="off">`) : "";
  const d = openDialog(`<h2>${esc(title)}</h2>${text ? `<p>${esc(text)}</p>` : ""}${field}
    <div class="acts" style="flex-direction:row-reverse;justify-content:flex-start">
      <button class="btn small ${danger ? "danger" : ""}" value="ok">${esc(ok)}</button>
      ${cancel ? `<button class="btn ghost small" value="cancel">${esc(cancel)}</button>` : ""}
    </div>`);
  const f = d.querySelector("[name=v]");
  if (f){ f.focus(); if (!input.multiline) f.select(); } else d.querySelector('[value="ok"]').focus();
  const rv = await closed(d);
  return input ? (rv === "ok" ? f.value.trim() : null) : rv === "ok";
}

/** Pick one of several actions. Resolves the chosen value, or null. */
async function choose({ title, text = "", choices, cancel = t("Cancel") }){
  const d = openDialog(`<h2>${esc(title)}</h2>${text ? `<p>${esc(text)}</p>` : ""}
    <div class="choices">${choices.map(c => `<button class="choice" value="c:${esc(c.value)}" ${c.disabled ? "disabled" : ""}>
      <b>${esc(c.label)}</b>${c.sub ? `<small>${esc(c.sub)}</small>` : ""}</button>`).join("")}</div>
    <div class="acts"><button class="btn ghost small" value="cancel">${esc(cancel)}</button></div>`);
  d.querySelector(".choice:not([disabled])")?.focus();
  const rv = await closed(d);
  return rv.startsWith("c:") ? rv.slice(2) : null;
}

function toast(msg, { bad = false, ms = 4800 } = {}){
  const el = document.createElement("div");
  el.className = "toast" + (bad ? " bad" : "");
  el.setAttribute("role", bad ? "alert" : "status");
  el.textContent = msg;
  $("#toasts").appendChild(el);
  setTimeout(() => el.remove(), ms);
}

async function shareLink(title){
  const url = location.href;
  if (navigator.share && matchMedia("(pointer:coarse)").matches){
    try { await navigator.share({ title, url }); return; } catch (e) { if (e.name === "AbortError") return; }
  }
  try { await navigator.clipboard.writeText(url); toast(t("Link copied — anyone with it sees the same live view.")); }
  catch (e){ await ask({ title:t("Link to this view"), input:{ value:url }, ok:t("Done"), cancel:"" }); }
}

/** File picker as a promise — resolves the parsed JSON, or null. */
function pickJSON(){
  return new Promise(resolve => {
    const inp = document.createElement("input");
    inp.type = "file"; inp.accept = "application/json,.json";
    inp.onchange = async () => {
      const file = inp.files?.[0];
      if (!file) return resolve(null);
      try { resolve(JSON.parse(await file.text())); }
      catch (e){ toast(t("That file is not valid JSON: {msg}", { msg:e.message }), { bad:true }); resolve(null); }
    };
    inp.click();
  });
}

function download(name, text, mime){
  const url = URL.createObjectURL(new Blob([text], { type:mime }));
  const a = document.createElement("a");
  a.href = url; a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1500);
}

const csvCell = v => { const s = v == null ? "" : String(v); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };

/* ---------- 1c. Views ------------------------------------------------ */
/* Four tools and a settings page, each in its own section of the page. A
   tool keeps its state while you are elsewhere — shortlist reviewers, check
   one of them, come back, and the shortlist is where you left it.

   Every view has an address, so it can be bookmarked, reloaded, or sent to
   a colleague. The address of the view on screen is the page's address. */

const VIEWS = ["check", "reviewers", "directory", "library", "settings"];
const UI = { view:"check", prev:"check", addr:{}, scroll:{} };
const VIEW_ENTER = {};   // view → function run each time it is shown (filled in by each tool)

function writeAddress(){
  const v = UI.view === "settings" ? UI.prev : UI.view;
  const p = { ...(v !== "check" ? { tool:v } : {}), ...(UI.addr[v] || {}) };
  const u = new URL(location.href);
  u.search = "";
  for (const [k, val] of Object.entries(p)) if (val !== undefined && val !== null && val !== "") u.searchParams.set(k, val);
  history.replaceState(null, "", u.pathname + u.search);
}
/** Record a view's address; it becomes the page's address while that view is on screen. */
function setAddress(params, view = UI.view){
  UI.addr[view] = params || {};
  if (view === UI.view || (UI.view === "settings" && view === UI.prev)) writeAddress();
}

function showView(v){
  if (!VIEWS.includes(v)) v = "check";
  if (UI.view !== v){
    UI.scroll[UI.view] = scrollY;
    if (v === "settings") UI.prev = UI.view;
    UI.view = v;
  }
  for (const id of VIEWS){ const el = $("#view-" + id); if (el) el.hidden = id !== v; }
  $$("#toolNav [data-view]").forEach(a => {
    const on = a.dataset.view === v;
    a.classList.toggle("on", on);
    if (on) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
  });
  writeAddress();
  VIEW_ENTER[v]?.();
  const y = UI.scroll[v] || 0;
  requestAnimationFrame(() => scrollTo(0, y));
}
function setView(v, html){ $("#view-" + v).innerHTML = html; }

/* ---------- 2. Network layer ---------------------------------------- */
/* One cache, one queue. OpenAlex asks for courtesy, not keys — we honour
   that with a modest concurrency cap rather than hammering it. */

const cache = new Map();
let inflight = 0;
const queue = [];

function pump(){
  while (inflight < 4 && queue.length){
    const job = queue.shift();
    inflight++;
    job().finally(() => { inflight--; pump(); });
  }
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

/* Crossref throttles bursts and answers 429 without a body. A failed
   lookup silently degrades the evidence for a work, so retry rather than
   accept the null. */
async function attempt(url, tries){
  let lastErr;
  for (let i = 0; i < tries; i++){
    try {
      const r = await fetch(url, { headers: { Accept: "application/json" } });
      if (r.status === 429 || r.status >= 500) throw new Error("HTTP " + r.status);
      if (!r.ok) throw new Error("HTTP " + r.status + " — " + url);
      return await r.json();
    } catch (e){
      lastErr = e;
      if (i < tries - 1) await sleep(400 * Math.pow(2, i) + Math.random() * 250);
    }
  }
  throw lastErr;
}

/* Bounded: a relations map alone pulls megabytes of reference lists, and a
   public tool can stay open all day. Oldest entries go first (a Map keeps
   insertion order); re-reading an entry moves it to the back. */
const CACHE_MAX = 600;
function remember(url, value){
  cache.delete(url);
  cache.set(url, value);
  if (cache.size > CACHE_MAX) for (const k of [...cache.keys()].slice(0, cache.size - CACHE_MAX)) cache.delete(k);
}

function getJSON(url, { optional = false, tries = 3 } = {}){
  if (cache.has(url)){ const v = cache.get(url); remember(url, v); return Promise.resolve(v); }
  return new Promise((resolve, reject) => {
    queue.push(() =>
      attempt(url, tries)
        .then(j => { remember(url, j); resolve(j); })
        .catch(e => {
          if (optional){ remember(url, null); resolve(null); }
          else reject(e);
        })
    );
    pump();
  });
}

function oa(path, params = {}){
  const u = new URL(CFG.openalex + path);
  for (const [k, v] of Object.entries(params))
    if (v !== undefined && v !== null && v !== "") u.searchParams.set(k, v);
  if (CFG.mailto) u.searchParams.set("mailto", CFG.mailto);
  return u.toString();
}

/* Author records in bulk — what the directory and the reviewer finder show
   for each person. Fifty per request, the most OpenAlex returns. */
const AUTHOR_SELECT = "id,display_name,orcid,works_count,cited_by_count,summary_stats,last_known_institutions,affiliations,counts_by_year,topics";
async function fetchAuthors(ids){
  const out = new Map();
  const list = [...new Set(ids.map(shortId))];
  await Promise.all(Array.from({ length:Math.ceil(list.length / 50) }, (_, i) => list.slice(i * 50, i * 50 + 50))
    .map(async batch => {
      const d = await getJSON(oa("/authors", { filter:"openalex:" + batch.join("|"), per_page:50, select:AUTHOR_SELECT }), { optional:true });
      (d?.results || []).forEach(a => out.set(shortId(a.id), a));
    }));
  return out;
}

/** Where a person is now: OpenAlex's last known institution, else the
    affiliation with the latest year on record. */
function currentInstOf(a){
  const lk = (a?.last_known_institutions || [])[0];
  if (lk) return lk;
  const aff = (a?.affiliations || []).slice()
    .sort((x, y) => Math.max(0, ...(y.years || [])) - Math.max(0, ...(x.years || [])))[0];
  return aff?.institution || null;
}
/** First and last year with indexed output. */
function activeSpan(a){
  const ys = (a?.counts_by_year || []).filter(c => c.works_count > 0).map(c => c.year);
  return ys.length ? [Math.min(...ys), Math.max(...ys)] : [null, null];
}
/** Works OpenAlex files under the field's topic — among the person's top five topics only. */
const fieldTopicCount = a => (a?.topics || []).find(tp => FIELD.topicIds.includes(shortId(tp.id)))?.count || 0;

/* ---------- 2b. Persistent store ------------------------------------ */
/* IndexedDB rather than localStorage: the saved library is meant to grow,
   localStorage caps at about 5 MB, and browsers evict it far more readily —
   particularly for pages opened from a file:// or content:// URL, which is
   how this runs before it is hosted. localStorage stays as a fallback for
   contexts where IndexedDB is blocked (private windows, some webviews). */

const DB = (() => {
  const NAME = "srom-audit", STORE = "kv";
  let dbp = null;

  function open(){
    if (dbp) return dbp;
    dbp = new Promise((resolve, reject) => {
      if (!self.indexedDB) return reject(new Error("no indexedDB"));
      const rq = indexedDB.open(NAME, 1);
      rq.onupgradeneeded = () => {
        if (!rq.result.objectStoreNames.contains(STORE)) rq.result.createObjectStore(STORE);
      };
      rq.onsuccess = () => resolve(rq.result);
      rq.onerror   = () => reject(rq.error);
    }).catch(e => { dbp = null; throw e; });
    return dbp;
  }

  function tx(mode, fn){
    return open().then(db => new Promise((resolve, reject) => {
      const t = db.transaction(STORE, mode);
      const rq = fn(t.objectStore(STORE));
      rq.onsuccess = () => resolve(rq.result);
      rq.onerror   = () => reject(rq.error);
    }));
  }

  const lsGet = k => { try { const v = localStorage.getItem("srom.kv." + k);
                             return v ? JSON.parse(v) : undefined; } catch (e) { return undefined; } };
  const lsSet = (k, v) => { try { localStorage.setItem("srom.kv." + k, JSON.stringify(v)); } catch (e) {} };

  return {
    async get(key, fallback){
      try { const v = await tx("readonly", st => st.get(key)); if (v !== undefined) return v; }
      catch (e) { const v = lsGet(key); if (v !== undefined) return v; }
      return fallback;
    },
    async set(key, value, { mirror = true } = {}){
      if (mirror) lsSet(key, value);           // mirror, so a blocked IDB still persists
      try { await tx("readwrite", st => st.put(value, key)); return true; } catch (e) { return mirror; }
    },
    async del(key){
      try { localStorage.removeItem("srom.kv." + key); } catch (e) {}
      try { await tx("readwrite", st => st.delete(key)); } catch (e) {}
    },
  };
})();

/* ---------- 2c. The saved library ----------------------------------- */
/* Folders are a many-to-many tagging of saved scholars: one person can
   legitimately sit under both "Holocaust" and "Poland", and forcing a single
   folder would make you choose arbitrarily. */

const LIB = { folders: [], scholars: {}, loaded: false };

const uid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 7);

async function libLoad(){
  const d = await DB.get("library", null);
  if (d){ LIB.folders = d.folders || []; LIB.scholars = d.scholars || {}; }
  else {
    // First run: seed with the categories an editorial process actually uses.
    LIB.folders = [
      { id:uid(), name:t("Reviewer pool") },
      { id:uid(), name:t("Editorial board candidates") },
      { id:uid(), name:t("Authors") },
    ];
  }
  LIB.loaded = true;
  libCount();
}
async function libSave(){
  await DB.set("library", { folders:LIB.folders, scholars:LIB.scholars, v:1 });
  libCount();
  scheduleBackup();
}

/* ---------- 2d. Automatic backup to disk ----------------------------- */
/* IndexedDB is wiped by "clear browsing data", so the library is written
   out to a real file as well.

   Chrome and Edge on the desktop can write into a folder you choose, and
   keep writing to it silently — one file, overwritten, plus a dated copy
   per day. Safari, Firefox and Chrome on Android offer no folder access to
   web pages at all, so there the backup is a download into Downloads.

   A folder permission is a browser grant, and browsers ask for it again
   in a new session unless "allow on every visit" was chosen. When that
   happens the backup does not fail silently: a banner asks for one click. */

const BK = {
  canFolder: typeof window.showDirectoryPicker === "function",
  settings: { dest:"download", when:"change" },   // dest: folder | download ; when: change | 5 | 15 | manual
  dir: null,                                      // FileSystemDirectoryHandle
  perm: "none",                                   // granted | prompt | none
  lastAt: null, lastWhere: null, lastError: null,
  dirty: false, timer: null, ticker: null,
};

function libraryPayload(){
  return { app:"SROM Scholar Audit", v:1, exported:new Date().toISOString(),
           folders:LIB.folders, scholars:LIB.scholars,
           venueRegistry:S.registry, pins:S.pins };
}

async function bkLoad(){
  BK.settings = { ...BK.settings, ...(await DB.get("backupSettings", {})) };
  const st = await DB.get("backupStatus", {});
  BK.lastAt = st.lastAt || null; BK.lastWhere = st.lastWhere || null;
  if (BK.canFolder){
    BK.dir = await DB.get("backupDir", null);
    if (BK.dir && typeof BK.dir.queryPermission === "function"){
      try { BK.perm = await BK.dir.queryPermission({ mode:"readwrite" }); }
      catch (e) { BK.perm = "none"; BK.dir = null; }
    } else BK.dir = null;
  }
  if (!BK.canFolder && BK.settings.dest === "folder") BK.settings.dest = "download";
  bkArmTicker();
  bkBanner();
}
async function bkSaveSettings(){ await DB.set("backupSettings", BK.settings); bkArmTicker(); bkBanner(); }

/** Called after every change. The debounce is short for silent folder
    writes and long for downloads, so a burst of edits — save a scholar, tag
    two folders, type a note — becomes one file rather than five. */
function scheduleBackup(){
  BK.dirty = true;
  if (BK.settings.when !== "change") return;
  clearTimeout(BK.timer);
  const wait = BK.settings.dest === "folder" ? 1500 : 30000;
  BK.timer = setTimeout(() => runBackup({ manual:false }), wait);
}

function bkArmTicker(){
  clearInterval(BK.ticker);
  const mins = { "5":5, "15":15 }[BK.settings.when];
  if (mins) BK.ticker = setInterval(() => { if (BK.dirty) runBackup({ manual:false }); }, mins * 60000);
}

const stamp = (d = new Date()) => d.toISOString().slice(0,16).replace("T","-").replace(":","");

/** Where the last backup went, in the interface language. Older versions
    stored an English phrase; it is shown as it was. */
function whereText(w){
  if (!w) return "";
  if (typeof w === "string") return w;
  return w.kind === "folder" ? t("folder “{name}”", { name:w.name }) : t("Downloads");
}

async function runBackup({ manual }){
  if (!LIB.loaded) return;
  const text = JSON.stringify(libraryPayload(), null, 2);
  BK.lastError = null;
  try {
    if (BK.settings.dest === "folder" && BK.dir){
      if (BK.perm !== "granted"){
        // Re-granting needs a user gesture; a manual press is one.
        if (manual) BK.perm = await BK.dir.requestPermission({ mode:"readwrite" });
        if (BK.perm !== "granted"){ bkBanner(); return; }
      }
      await writeFile(BK.dir, "srom-library.json", text);
      // One dated copy per day, so a bad edit can be walked back.
      const hist = await BK.dir.getDirectoryHandle("history", { create:true });
      await writeFile(hist, `srom-library-${new Date().toISOString().slice(0,10)}.json`, text);
      await pruneHistory(hist, 30);
      BK.lastWhere = { kind:"folder", name:BK.dir.name };
    } else if (BK.settings.dest === "download" || manual){
      download(`srom-library-${stamp()}.json`, text, "application/json");
      BK.lastWhere = { kind:"download" };
    } else return;
    BK.lastAt = new Date().toISOString();
    BK.dirty = false;
    await DB.set("backupStatus", { lastAt:BK.lastAt, lastWhere:BK.lastWhere });
  } catch (e){
    BK.lastError = e.message || String(e);
  }
  bkBanner();
  if (UI.view === "settings") renderSettings();
}

async function writeFile(dir, name, text){
  const fh = await dir.getFileHandle(name, { create:true });
  const w = await fh.createWritable();
  await w.write(text);
  await w.close();
}

async function pruneHistory(dir, keep){
  const names = [];
  for await (const [name] of dir.entries()) if (/^srom-library-\d{4}-\d{2}-\d{2}\.json$/.test(name)) names.push(name);
  names.sort().slice(0, Math.max(0, names.length - keep))
       .forEach(n => dir.removeEntry(n).catch(() => {}));
}

async function bkChooseFolder(){
  try {
    const dir = await window.showDirectoryPicker({ id:"srom-backup", mode:"readwrite", startIn:"documents" });
    BK.dir = dir;
    BK.perm = await dir.queryPermission({ mode:"readwrite" });
    if (BK.perm !== "granted") BK.perm = await dir.requestPermission({ mode:"readwrite" });
    await DB.set("backupDir", dir, { mirror:false });
    BK.settings.dest = "folder";
    await bkSaveSettings();

    // A folder that already holds a backup is the recovery path after the
    // browser's data was cleared: offer it before overwriting anything.
    const existing = await readFolderBackup();
    const localN = Object.keys(LIB.scholars).length;
    if (existing && Object.keys(existing.scholars || {}).length){
      const n = Object.keys(existing.scholars).length;
      if (await ask({ title:t("This folder already holds a backup"),
            text: t("{scholars}, saved {when}.", { scholars:tn(n, "scholar"), when:fmtWhen(existing.exported) }) + " " +
                  (localN ? t("Merge it into the {n} you have here? Nothing already here is lost.", { n:localN }) : t("Restore it now?")),
            ok: localN ? t("Merge") : t("Restore"), cancel:t("Not now") })){
        const r = await mergeLibrary(existing);
        toast(t("Restored {added}; {merged} merged.", { added:tn(r.added, "scholar"), merged:r.merged }));
      }
    }
    await runBackup({ manual:true });
  } catch (e){
    if (e.name !== "AbortError") toast(t("Could not use that folder: {msg}", { msg:e.message }), { bad:true });
  }
  if (UI.view === "settings") renderSettings();
}

async function readFolderBackup(){
  if (!BK.dir) return null;
  try {
    if (BK.perm !== "granted") BK.perm = await BK.dir.requestPermission({ mode:"readwrite" });
    if (BK.perm !== "granted") return null;
    const fh = await BK.dir.getFileHandle("srom-library.json");
    return JSON.parse(await (await fh.getFile()).text());
  } catch (e){ return null; }
}

const fmtWhen = iso => iso ? new Date(iso).toLocaleString(LOCALE(),
  { day:"numeric", month:"short", year:"numeric", hour:"2-digit", minute:"2-digit" }) : t("never");

/** A lapsed folder permission must be visible, or backups stop without anyone noticing. */
function bkBanner(){
  let b = $("#bkBanner");
  const needs = BK.settings.dest === "folder" && BK.dir && BK.perm !== "granted";
  const lost  = BK.settings.dest === "folder" && !BK.dir && BK.canFolder;
  if (!needs && !lost && !BK.lastError){ if (b) b.remove(); return; }
  if (!b){
    b = document.createElement("div");
    b.id = "bkBanner"; b.className = "bk-banner";
    document.querySelector(".wrap").prepend(b);
  }
  b.innerHTML = BK.lastError
    ? `${esc(t("Backup failed: {msg}", { msg:BK.lastError }))} <button class="icon-btn" id="bkFix">${esc(t("Settings"))}</button>`
    : needs
      ? `${esc(t("Automatic backup is paused — the browser needs permission to write to “{name}” again.", { name:BK.dir.name }))}
         <button class="icon-btn" id="bkFix">${esc(t("Allow"))}</button>`
      : `${esc(t("No backup folder is connected."))} <button class="icon-btn" id="bkFix">${esc(t("Choose folder"))}</button>`;
  $("#bkFix").onclick = async () => {
    if (needs){
      BK.perm = await BK.dir.requestPermission({ mode:"readwrite" });
      if (BK.perm === "granted" && BK.dirty) await runBackup({ manual:true });
      bkBanner();
    } else if (lost) bkChooseFolder();
    else showView("settings");
  };
}
function libCount(){
  const n = Object.keys(LIB.scholars).length;
  const el = $("#libCount");
  if (el) el.textContent = n ? String(n) : "";
}

/** A compact, self-sufficient record: enough to browse and compare the
    library without refetching every scholar from the APIs. */
function scholarSnapshot(){
  const sm = computeSummary();
  const x  = computeExpertise();
  const A  = S.author;
  return {
    id: shortId(A.id),
    name: A.display_name,
    orcid: orcidOf(A.orcid) || (S.orcidInferred && S.orcid ? S.orcid["orcid-identifier"]?.path : null) || null,
    orcidInferred: !!S.orcidInferred,
    affiliation: (A.affiliations || [])[0]?.institution?.display_name || null,
    country: (A.affiliations || [])[0]?.institution?.country_code || null,
    works: sm.total, cites: sm.cites, hIndex: sm.hIndex,
    firstYear: sm.firstYear, lastYear: sm.lastYear,
    relevantPct: sm.relevantPct, inField: sm.relevant,
    topTierPct: sm.topTierPct, tiers: sm.byTier,
    headline: expertiseHeadline(x, sm),
    core: x.core.map(r => r.label),
    secondary: x.secondary.map(r => r.label),
    coreIds: x.core.map(r => r.id),
    secondaryIds: x.secondary.map(r => r.id),
    reviewVenues: S.reviews.map(r => r.name),
    wikidata: S.wikidata?.id || null,
    siblings: (S.siblings || []).map(x => shortId(x.id)),
    pins: myPins(),
    savedAt: new Date().toISOString(),
  };
}

/** A library record from an OpenAlex author alone — what the directory and
    the reviewer finder know before a dossier is built. Marked `light`; the
    first time the dossier is opened it fills in. */
function lightRecord(a){
  const inst = currentInstOf(a);
  const [first, last] = activeSpan(a);
  return {
    id: shortId(a.id), name: a.display_name,
    orcid: orcidOf(a.orcid) || null, orcidInferred: false,
    affiliation: inst?.display_name || null, country: inst?.country_code || null,
    works: a.works_count ?? null, cites: a.cited_by_count ?? null, hIndex: a.summary_stats?.h_index ?? null,
    firstYear: first, lastYear: last,
    light: true, pins: {}, savedAt: new Date().toISOString(),
  };
}

async function libToggleSave(){
  if (!S.author) return;
  const id = shortId(S.author.id);
  if (LIB.scholars[id]) delete LIB.scholars[id];
  else LIB.scholars[id] = { ...scholarSnapshot(), folders: [], note: "" };
  await libSave();
  if (LIB.scholars[id] && !dcEntry(id)) await dcPut();   // saved ⇒ kept
  renderShell();
}

/** A saved scholar's record follows the dossier: a light record fills in, and
    a stale count is corrected — but only when something changed, so opening a
    dossier does not trigger a backup by itself. */
async function libRefreshFromDossier(){
  const id = shortId(S.author?.id);
  const rec = id && LIB.scholars[id];
  if (!rec) return;
  const snap = scholarSnapshot();
  const keys = ["works","cites","hIndex","lastYear","relevantPct","inField","affiliation"];
  if (!rec.light && rec.coreIds && keys.every(k => rec[k] === snap[k])) return;
  Object.assign(rec, snap, { folders:rec.folders || [], note:rec.note || "", savedAt:rec.savedAt || snap.savedAt,
                             pins:{ ...(rec.pins || {}), ...snap.pins } });
  delete rec.light;
  await libSave();
}

async function libSetFolder(scholarId, folderId, on){
  const rec = LIB.scholars[scholarId];
  if (!rec) return;
  const set = new Set(rec.folders || []);
  on ? set.add(folderId) : set.delete(folderId);
  rec.folders = [...set];
  await libSave();
}

async function newFolder(value = ""){
  const name = await ask({ title:t("New folder"), text:t("Name it after a niche, a speciality or a purpose."),
    input:{ value, placeholder:t("e.g. Porajmos · Romani linguistics · Reviewers 2027") }, ok:t("Create") });
  if (!name) return null;
  const f = { id:uid(), name };
  LIB.folders.push(f);
  return f;
}

/** Choose a folder to save into. Resolves a folder id, "" for no folder, or
    null when cancelled. */
async function pickFolder({ title, text = "", suggest = "" }){
  const k = await choose({ title, text, choices:[
    ...LIB.folders.map(f => ({ value:f.id, label:f.name,
      sub:tn(Object.values(LIB.scholars).filter(r => (r.folders || []).includes(f.id)).length, "scholar") })),
    { value:"__new",  label:t("New folder…") },
    { value:"__none", label:t("Library only, no folder") },
  ] });
  if (k === null) return null;
  if (k === "__none") return "";
  if (k === "__new"){ const f = await newFolder(suggest); return f ? f.id : null; }
  return k;
}

/** Save OpenAlex authors to the library, into a folder. Records already
    there keep what they have and gain the folder. */
async function libSaveAuthors(authors, folderId){
  let added = 0;
  for (const a of authors){
    const id = shortId(a.id);
    const rec = LIB.scholars[id] || (added++, LIB.scholars[id] = { ...lightRecord(a), folders:[], note:"" });
    if (folderId && !(rec.folders || []).includes(folderId)) rec.folders = [...(rec.folders || []), folderId];
  }
  await libSave();
  return added;
}

/* ---------- 2e. Stored dossiers ------------------------------------- */
/* A dossier costs about a hundred API calls. Keep the result: opening a
   saved scholar becomes instant, and a relations map of stored scholars
   needs no second download. Saved scholars are kept while they are saved;
   the last KEEP_OTHERS other dossiers you opened are kept too, oldest
   dropped first. Stored copies are left out of the library backup — they
   rebuild from the APIs, and would make every backup many megabytes. */

const DC = {
  index: [],           // [{ id, orcid, name, at, siblings }], newest first
  mode: "cached",      // cached: open the stored copy, offer an update · ask · fresh
  KEEP_OTHERS: 25,
  STALE_DAYS: 30,
};

async function dcLoad(){
  DC.index = await DB.get("dossierIndex", []);
  DC.mode  = await DB.get("dossierMode", "cached");
}
const dcSaveIndex = () => DB.set("dossierIndex", DC.index, { mirror:false });
const dcGet = id => DB.get("dossier:" + id, null);

/** A stored dossier by ORCID or OpenAlex id — including a merged sibling profile. */
function dcEntry(key){
  const k = String(key || "").trim();
  const mo = k.match(RX_ORCID), mx = k.match(RX_OPENALEX);
  if (mo) return DC.index.find(e => e.orcid === mo[1]) || null;
  if (mx){ const id = mx[1].toUpperCase(); return DC.index.find(e => e.id === id || (e.siblings || []).includes(id)) || null; }
  return null;
}

const SOURCE_KEYS = ["id","display_name","type","is_in_doaj","is_core","is_ojs","is_preprint_repository",
                     "summary_stats","homepage_url","host_organization_name","issn","issn_l"];
function trimSource(src){ const o = {}; for (const k of SOURCE_KEYS) if (k in src) o[k] = src[k]; return o; }

/** An ORCID record carries every claimed work in full; the dossier needs the
    person, employment, education — and only a count of works. */
function orcidWorkCount(o = S.orcid){
  const act = o?.["activities-summary"];
  return act?.worksCount ?? act?.works?.group?.length ?? 0;
}
function trimOrcid(o){
  if (!o) return null;
  const act = o["activities-summary"] || {};
  return { "orcid-identifier": o["orcid-identifier"], person: o.person,
           "activities-summary": { employments: act.employments, educations: act.educations, worksCount: orcidWorkCount(o) } };
}

async function dcPut(){
  if (!S.author) return;
  const id = shortId(S.author.id);
  const at = new Date().toISOString();
  const ok = await DB.set("dossier:" + id, {
    v: 1, at, hasRefs: true,
    author: S.author, siblings: S.siblings || [], works: S.works,
    sources: [...S.sources.entries()].map(([k, v]) => [k, trimSource(v)]),
    orcid: trimOrcid(S.orcid), orcidInferred: !!S.orcidInferred,
    reviews: S.reviews, wikidata: S.wikidata, s2: S.s2, inst: S.inst,
    doaj: [...S.doaj.entries()], candidateCount: S.candidateCount || 1,
  }, { mirror:false });
  if (!ok) return;                      // storage blocked: the dossier still works, it just is not kept
  DC.index = DC.index.filter(e => e.id !== id);
  DC.index.unshift({ id, name: S.author.display_name, at,
    orcid: S.orcidInferred ? null : (orcidOf(S.author.orcid) || null),
    siblings: (S.siblings || []).map(x => shortId(x.id)) });
  await dcPrune();
}

async function dcPrune(){
  let others = 0;
  const keep = [];
  for (const e of DC.index){
    if (LIB.scholars[e.id] || ++others <= DC.KEEP_OTHERS) keep.push(e);
    else await DB.del("dossier:" + e.id);
  }
  DC.index = keep;
  await dcSaveIndex();
}

async function dcClear(){
  for (const e of DC.index) await DB.del("dossier:" + e.id);
  DC.index = [];
  await dcSaveIndex();
}

function dcRestore(snap){
  S.author = snap.author; S.siblings = snap.siblings || []; S.works = snap.works;
  S.sources = new Map(snap.sources || []); S.orcid = snap.orcid; S.orcidInferred = !!snap.orcidInferred;
  S.reviews = snap.reviews || []; S.wikidata = snap.wikidata; S.s2 = snap.s2; S.inst = snap.inst;
  for (const [k, v] of snap.doaj || []) S.doaj.set(k, v);
  S.candidateCount = snap.candidateCount || 1;
  S.storedAt = snap.at;
  S.works.forEach(scoreWork);          // venue verdicts may have changed since it was stored
}

const daysSince = iso => Math.floor((Date.now() - new Date(iso)) / 86400000);
const ageText = iso => { const d = daysSince(iso);
  return d <= 0 ? t("today") : d === 1 ? t("yesterday")
       : d < 60 ? t("{n} ago", { n:tn(d, "day") }) : t("{n} ago", { n:tn(Math.round(d / 30), "month") }); };

/* ---------- 3. Application state ------------------------------------ */

const S = {
  author: null,      // OpenAlex author object
  works: [],         // normalised work records
  sources: new Map(),// OpenAlex source id -> source object
  orcid: null,       // ORCID record
  wikidata: null,    // { id, label, description, ids:{} }
  s2: null,          // resolved Semantic Scholar author
  pins: loadPins(),  // hand-pinned identifiers, keyed by OpenAlex author id
  reviews: [],       // resolved peer-review venues
  doaj: new Map(),   // ISSN → DOAJ's answer (session cache, never stored as a verdict)
  registry: loadRegistry(),
  view: "chrono",    // chrono | venue | tier
  tab: "record",
  filters: { text:"", from:null, to:null, type:"", tier:"", venue:"", oaOnly:false, fieldOnly:false },
};

function loadPins(){
  try { return JSON.parse(localStorage.getItem("srom.scholarPins") || "{}"); }
  catch (e) { return {}; }
}
function savePins(){
  try { localStorage.setItem("srom.scholarPins", JSON.stringify(S.pins)); } catch (e) {}
  scheduleBackup();
}
/** Pinned identifiers for the scholar currently on screen. */
function myPins(){
  const id = shortId(S.author?.id);
  return (id && S.pins[id]) || {};
}

const hasVerdict = v => !!(v && (v.erih || v.scopus || v.wos || (v.mein && v.mein !== "—")));

function loadRegistry(){
  try {
    const raw = localStorage.getItem("srom.venueRegistry");
    if (raw){
      // Earlier versions filed DOAJ lookups here as if they were verdicts.
      const reg = JSON.parse(raw);
      for (const [k, v] of Object.entries(reg)){
        delete v.doajConfirmed; delete v.doajSeal;
        if (!hasVerdict(v) && !v.seeded) delete reg[k];
        // Seed entries are ones you never edited (editing clears `seeded`),
        // so they follow the current seed list — a retracted claim goes.
        else if (v.seeded) SEED_VENUES[k] ? (reg[k] = { ...SEED_VENUES[k], seeded:true }) : delete reg[k];
      }
      for (const [k, v] of Object.entries(SEED_VENUES)) if (!reg[k]) reg[k] = { ...v, seeded:true };
      return reg;
    }
  } catch (e) { /* private mode, cleared storage — fall through to seed */ }
  const seed = {};
  for (const [issn, v] of Object.entries(SEED_VENUES))
    seed[issn] = { ...v, seeded:true };
  return seed;
}
function saveRegistry(){
  try { localStorage.setItem("srom.venueRegistry", JSON.stringify(S.registry)); }
  catch (e) { /* nothing persistable; the session still works */ }
  updateRegCount();
  if (typeof scheduleBackup === "function" && LIB.loaded) scheduleBackup();
}
/** Venues where you, not the seed list, recorded a verdict. */
function userVerdictCount(){
  return Object.values(S.registry).filter(v => !v.seeded && hasVerdict(v)).length;
}
function updateRegCount(){
  const n = userVerdictCount();
  const el = $("#regCount");
  if (el) el.textContent = n ? "(" + n + ")" : "";
}

const RX_ORCID    = /^(?:https?:\/\/orcid\.org\/)?(\d{4}-\d{4}-\d{4}-\d{3}[\dX])$/i;
const RX_OPENALEX = /^(?:https?:\/\/openalex\.org\/)?(A\d{5,})$/i;
