--[[ srom_post.lua — runs AFTER --citeproc (see build.py).

Turns the SROM-MD AST into a DOCX-ready AST whose every paragraph and every
italic/small-caps run carries a NAMED style (config/styles.json), so InDesign
maps them by name on import and nothing arrives as a local override.

Messages on stderr:  SROM-WARN: …  (review)   SROM-ERROR: …  (build fails)
]]

local stringify = pandoc.utils.stringify
local cfg, P, C, R, KEEP_TITLE
local nerr = 0
local function warn(m) io.stderr:write("SROM-WARN: " .. m .. "\n") end
local function err(m) io.stderr:write("SROM-ERROR: " .. m .. "\n"); nerr = nerr + 1 end
-- cut on character boundaries: a byte cut can split a Polish letter, and invalid UTF-8 on stderr breaks build.py (E15)
local function head(s, n) local i = utf8.offset(s, n + 1); return i and s:sub(1, i - 1) or s end
local function tail(s, n) local i = utf8.offset(s, -n); return i and s:sub(i) or s end
local function short(inls) local s = stringify(inls); return (utf8.len(s) or #s) > 70 and (head(s, 70) .. "…") or s end

local function cstyle(name) return pandoc.Attr("", {}, {{"custom-style", name}}) end

-- non-author note (kanon § 7.1): its text ENDS with "– przyp. tłum." or "– przyp. red." (as check.py na_kind);
-- "[… – przyp. tłum.]" closing an author's note is an addition inside that note and does not count
local function is_nonauthor(blocks)
  local s = stringify(blocks):gsub("%s+$", "")
  for _, f in ipairs({"przyp%.%s*tłum%.$", "przyp%.%s*red%.$"}) do
    local i = s:find(f)
    if i then
      local before = s:sub(1, i - 1):gsub("%s+$", "")
      if before:sub(-3) == "–" or before:sub(-1) == "-" then return true end
    end
  end
  return false
end
local function styled_para(inls, style) return pandoc.Div({pandoc.Para(inls)}, cstyle(style)) end

---------------------------------------------------------------- pass A: config
local function load_cfg(meta)
  local path = meta["srom-config"] and stringify(meta["srom-config"]) or os.getenv("SROM_CONFIG")
  if not path then error("SROM: no srom-config metadata / SROM_CONFIG") end
  local fh = assert(io.open(path, "r"), "SROM: cannot open " .. path)
  cfg = pandoc.json.decode(fh:read("a"), false)
  fh:close()
  P, C, R = cfg.paragraph, cfg.character, cfg.roles
  KEEP_TITLE = meta["srom-keep-title"] and stringify(meta["srom-keep-title"]) == "true"   -- check.py --keyed
end

-- a title note with citations reaches citeproc as the first footnote (build.py title_note_as_footnote), its
-- content opening with an empty span of class srom-title; pass F takes it back out
local function is_title_note(n)
  local b = n.content[1]
  local f = b and (b.t == "Para" or b.t == "Plain") and b.content[1]
  return f and f.t == "Span" and f.classes:includes("srom-title")
end

---------------------------------------------------------------- pass B: in-note citations
-- pandoc wraps a citation that sits INSIDE a footnote in parentheses: "Zob. (Ficowski, …, s. 5)".
-- SROM wants it bare. Strip exactly one outer "(" … ")" pair; restore a period that ended the
-- user's suffix (e.g. "i n.") which citeproc drops; collapse a resulting double period.
local function edge_str(inls, from_end)
  -- returns the list and index of the outermost-first/last Str, descending into containers
  local i = from_end and #inls or 1
  while inls[i] and (inls[i].t == "Space" or inls[i].t == "SoftBreak") do
    i = from_end and i - 1 or i + 1
  end
  local el = inls[i]
  if not el then return nil end
  if el.t == "Str" then return inls, i end
  if el.content and el.t ~= "Note" and el.t ~= "Cite" then return edge_str(el.content, from_end) end
  return nil
end

local function trim_leading_space(inls)
  while #inls > 0 and (inls[1].t == "Space" or inls[1].t == "SoftBreak") do inls:remove(1) end
end

-- abbreviations that may legitimately end a rendered citation (their period is not the layout period)
local ABBR = {["w."]=1, ["r."]=1, ["n."]=1, ["s."]=1, ["t."]=1, ["nr."]=1, ["red."]=1, ["tłum."]=1, ["wyd."]=1,
              ["oprac."]=1, ["in."]=1, ["zob."]=1, ["por."]=1, ["k."]=1, ["l."]=1, ["ark."]=1, ["ok."]=1}

local function fix_note_cites(note)
  local function fix_inlines(inls)
    local out = pandoc.List()
    local own_dot = nil      -- a Cite whose final period is the author's own ("[@key]." merged): not a layout period
    for idx, el in ipairs(inls) do
      if el.t == "Cite" then
        local c = el.content
        trim_leading_space(c)
        local fl, fi = edge_str(c, false)
        local ll, li = edge_str(c, true)
        if fl and ll and fl[fi].text:sub(1, 1) == "(" and ll[li].text:sub(-1) == ")" then
          fl[fi].text = fl[fi].text:sub(2)
          ll, li = edge_str(c, true)
          ll[li].text = ll[li].text:sub(1, -2)
          -- restore a trailing abbreviation period from the user's suffix ("i n.") which citeproc drops
          local last = el.citations[#el.citations]
          local suf = stringify(last.suffix)
          ll, li = edge_str(c, true)
          if suf:match("%.$") and ll and not ll[li].text:match("%.$") then
            ll[li].text = ll[li].text .. "."
          end
        end
        el.content = c   -- write back: .content returns a copy
        out:insert(el)
      elseif el.t == "Str" and #out > 0 and out[#out].t == "Cite" then
        local cite = out[#out]
        local c = cite.content
        local ll, li = edge_str(c, true)
        local first = el.text:sub(1, 1)
        if first == "." and ll and ll[li].text:match("%.$") then
          -- "s. 15." + "." -> single period
          local rest = el.text:sub(2)
          if rest ~= "" then out:insert(pandoc.Str(rest)) else own_dot = cite end
        elseif (first == ";" or first == "," or first == ":") and ll and ll[li].text:match("%.$") then
          -- CSL layout period before the author's own ; , : -> drop it, unless it closes an abbreviation
          local suf = stringify(cite.citations[#cite.citations].suffix)
          local tok = ll[li].text:match("(%S+)$") or ""
          if not suf:match("%.$") and not ABBR[tok] then
            ll[li].text = ll[li].text:sub(1, -2)
            cite.content = c
          end
          out:insert(el)
        else
          out:insert(el)
        end
      elseif el.t == "Space" and #out > 0 and out[#out].t == "Cite" and out[#out] ~= own_dot and inls[idx + 1] and inls[idx + 1].t == "Str"
             and inls[idx + 1].text:sub(1, 1) == "(" then
        -- the author's remark after a citation, "s. 63 (my translation).": the CSL layout period does not go before
        -- the bracket ("s. 63. (my translation)." before), unless it closes an abbreviation, or the bracket holds a
        -- sentence of its own ("…, s. 90. (Zdanie.)": citeproc has taken the author's full stop into the citation)
        local inside = ""
        for j = idx + 1, math.min(#inls, idx + 60) do
          inside = inside .. stringify(inls[j])
          if inside:find(")", 1, true) then break end
        end
        local sentence = inside:match("[%.!?…]%)") ~= nil
        local cite = out[#out]
        local c = cite.content
        local ll, li = edge_str(c, true)
        local suf = stringify(cite.citations[#cite.citations].suffix)
        local tok = ll and (ll[li].text:match("(%S+)$") or "") or ""
        if ll and ll[li].text:match("%.$") and not suf:match("%.$") and not ABBR[tok] and not sentence then
          ll[li].text = ll[li].text:sub(1, -2)
          cite.content = c
        end
        out:insert(el)
      else
        out:insert(el)
      end
    end
    return out
  end
  local nb = pandoc.walk_block(pandoc.Div(note.content), {
    Para = function(p) p.content = fix_inlines(p.content); return p end,
    Plain = function(p) p.content = fix_inlines(p.content); return p end,
  })
  note.content = nb.content
  return note
end

---------------------------------------------------------------- pass B0: citations without a page
-- CSL prints "[BRAK STRONY]" for a citation without a locator. It is never printed and never blocks:
-- a page-less citation may legitimately refer to the whole work. Every one is reported on stderr as
--   SROM-NOPAGE: <note no> TAB <quote|work> TAB <keys> TAB <text before the marker>
-- "quote" = the first citation of a note attached to a quotation (marker right after ” or «, or a
-- note inside a block quote) that is not introduced by zob./por./np./też — ask the author for a page.
-- build.py turns these lines into the author query sheet (<article>_pytania.md/.csv).
local SEE = {["zob."]=1, ["por."]=1, ["np."]=1, ["też"]=1, ["też:"]=1}
local function is_see(text)
  local w = (text or ""):match("(%S+)%s*$")
  return w and SEE[pandoc.text.lower(w)] ~= nil
end

local function has_brak(inls)
  return stringify(inls):find("[BRAK STRONY]", 1, true) ~= nil
end

local function drop_brak_strony(inls)
  local out = pandoc.List()
  local i = 1
  while i <= #inls do
    local el = inls[i]
    if el.t == "Str" and el.text == "[BRAK" and inls[i + 1] and inls[i + 1].t == "Space"
       and inls[i + 2] and inls[i + 2].t == "Str" and inls[i + 2].text:match("^STRONY%]") then
      if #out > 0 and out[#out].t == "Space" then out:remove(#out) end
      if #out > 0 and out[#out].t == "Str" then out[#out].text = out[#out].text:gsub(",$", "") end
      local rest = inls[i + 2].text:gsub("^STRONY%]", "")
      if rest ~= "" then out:insert(pandoc.Str(rest)) end
      i = i + 3
    else
      out:insert(el)
      i = i + 1
    end
  end
  return out
end

-- citation modes that break SROM notes: "@key" (author in text) and "[-@key]" (author suppressed)
-- print a first citation without its author; pandoc gives no warning, so we stop here.
local function check_modes(inls)
  pandoc.walk_inline(pandoc.Span(inls), {Cite = function(c)
    for _, ci in ipairs(c.citations) do
      if ci.mode == "AuthorInText" then
        err("@" .. ci.id .. " written without brackets (author-in-text): write the name in prose and cite [@" .. ci.id .. ", s. …]")
      elseif ci.mode == "SuppressAuthor" then
        err("[-@" .. ci.id .. "] suppresses the author — SROM notes always give it; use [@" .. ci.id .. "]")
      end
    end
  end})
end

local note_no = 0
local function clean(s) return (s:gsub("[\t\n]", " ")) end

local function record(kind, keys, context, label)
  io.stderr:write("SROM-NOPAGE: " .. (label or note_no) .. "\t" .. kind .. "\t" .. table.concat(keys, " ") .. "\t" .. clean(context) .. "\n")
end

local function whole_work(blocks, quoted, context, outer)
  -- printed numbering counts the author's notes only; a non-author note is reported as "*"
  local label = nil
  if not outer and is_nonauthor(blocks) then label = "*" else note_no = note_no + 1 end
  if outer then
    -- a note that citeproc generated from a citation typed in the main text: the note holds the
    -- rendered citation itself, the Cite element (outer) sits around the Note
    local b = pandoc.Div(blocks)
    if has_brak(b.content) then
      local keys = {}
      for _, c in ipairs(outer.citations) do table.insert(keys, c.id) end
      local pre = pandoc.text.lower(stringify(outer.citations[1].prefix))
      local see = is_see(pre) or pre:match("^zob") or pre:match("^por") or pre:match("^np")
      record((quoted and not see) and "quote" or "work", keys, context)
      return pandoc.walk_block(b, {Inlines = drop_brak_strony}).content
    end
    return blocks
  end
  local k = 0
  local function fix(inls)
    local before = ""
    for _, el in ipairs(inls) do
      if el.t == "Cite" then
        check_modes({el})
        k = k + 1
        local see = is_see(before)
        local pre = pandoc.text.lower(stringify(el.citations[1].prefix))
        if is_see(pre) or pre:match("^zob") or pre:match("^por") or pre:match("^np") then see = true end
        if has_brak(el.content) then
          local keys = {}
          for _, c in ipairs(el.citations) do table.insert(keys, c.id) end
          record((quoted and k == 1 and not see) and "quote" or "work", keys, context, label)
          el.content = pandoc.walk_inline(pandoc.Span(el.content), {Inlines = drop_brak_strony}).content
        end
        before = before .. " " .. stringify(el.content)
      else
        before = before .. stringify(el)
      end
    end
    return inls
  end
  return pandoc.walk_block(pandoc.Div(blocks), {
    Para = function(p) p.content = fix(p.content); return p end,
    Plain = function(p) p.content = fix(p.content); return p end,
  }).content
end

local function quote_end(el)
  if not el then return false end
  if el.t == "Quoted" then return true end
  return el.t == "Str" and (el.text:match("”$") or el.text:match("«$")) ~= nil
end

local scan_blocks
local function scan_inlines(inls, in_quote)
  local seen = ""
  for i, el in ipairs(inls) do
    if el.t == "Note" then
      local ctx = tail(seen, 90)
      el.content = whole_work(el.content, in_quote or quote_end(inls[i - 1]), ctx)
    elseif el.t == "Cite" then
      check_modes({el})
      local q = in_quote or quote_end(inls[i - 1])
      local c = el.content
      for j, sub in ipairs(c) do
        if sub.t == "Note" then sub.content = whole_work(sub.content, q, tail(seen, 90), el) end
      end
      el.content = c
    elseif el.t ~= "Image" and el.t ~= "Str" and el.content and type(el.content) ~= "string" then
      el.content = scan_inlines(el.content, in_quote)
    end
    if el.t ~= "Note" then seen = seen .. stringify(el) end
  end
  return inls
end
scan_blocks = function(blocks, in_quote)
  for _, b in ipairs(blocks) do
    if b.t == "Para" or b.t == "Plain" or b.t == "Header" then b.content = scan_inlines(b.content, in_quote)
    elseif b.t == "LineBlock" then
      for j, line in ipairs(b.content) do b.content[j] = scan_inlines(line, true) end
    elseif b.t == "BlockQuote" then b.content = scan_blocks(b.content, true)
    elseif b.t == "Div" then b.content = scan_blocks(b.content, in_quote)
    elseif b.t == "BulletList" or b.t == "OrderedList" then
      local items = b.content
      for j, item in ipairs(items) do items[j] = scan_blocks(item, in_quote) end
      b.content = items
    elseif b.t == "Table" then
      local function rows(rs) for _, r in ipairs(rs) do for _, c in ipairs(r.cells) do c.contents = scan_blocks(c.contents, in_quote) end end end
      rows(b.head.rows)
      for _, body in ipairs(b.bodies) do rows(body.head); rows(body.body) end
      rows(b.foot.rows)
    end
  end
  return blocks
end

---------------------------------------------------------------- pass C: inline styling
local PARTICLES = {}
for _, p in ipairs({"de", "van", "von", "der", "den", "di", "da", "le", "la", "du", "del", "della", "ten", "ter", "van der", "van den", "von der", "de la", "d’", "d'", "y"}) do PARTICLES[p] = true end

local inline_pass = {
  Quoted = function(el)
    local o, c = "„", "”"
    if el.quotetype == "SingleQuote" then o, c = "»", "«" end
    local out = pandoc.List({pandoc.Str(o)})
    out:extend(el.content)
    out:insert(pandoc.Str(c))
    return out
  end,
  Emph = function(el)
    -- nested italics (title inside a title, Kanon § 3.4): the italic run is split and the inner title set as a
    -- roman run between its parts ("*A Note on _Les Fourberies_*" -> italic "A Note on " + roman "Les Fourberies")
    local out, cur = pandoc.List(), pandoc.List()
    local function flush()
      if #cur > 0 then out:insert(pandoc.Span(cur, cstyle(C.italic))); cur = pandoc.List() end
    end
    for _, x in ipairs(el.content) do
      if x.t == "Span" and x.attributes["custom-style"] == C.italic then
        warn("nested italics set roman, verify: " .. short(x.content))
        flush()
        out:extend(x.content)
      else
        -- deeper nesting (inside quotes, links): unwrap as before; rare
        cur:insert(pandoc.walk_inline(x, {Span = function(s)
          if s.attributes["custom-style"] == C.italic then
            warn("nested italics (deep) set roman, verify: " .. short(s.content)); return s.content
          end
        end}))
      end
    end
    flush()
    return out
  end,
  SmallCaps = function(el)
    -- kanon §9.3: particles stay lower case and outside small caps ("HEUSCH, Luc de"; placed per § 9.5)
    local t = stringify(el)
    if PARTICLES[t] then return el.content end
    return pandoc.Span(el.content, cstyle(C.smallcaps))
  end,
  Strong = function(el) warn("bold removed (kanon §3.4): " .. short(el.content)); return el.content end,
  Underline = function(el) warn("underline removed (kanon §3.4): " .. short(el.content)); return el.content end,
  Strikeout = function(el) warn("strikeout removed: " .. short(el.content)); return el.content end,
  Superscript = function(el) warn("superscript kept as local formatting, verify: " .. short(el.content)) end,
  Subscript = function(el) warn("subscript kept as local formatting, verify: " .. short(el.content)) end,
  Link = function(el) return el.content end,
  Image = function(el) err("image in text flow — place in InDesign, keep only caption: " .. el.src) ; return {} end,
  RawInline = function(el) err("raw " .. el.format .. " inline: " .. el.text) end,
  Math = function(el) err("math inline: " .. el.text) end,
}

-- forced line breaks survive only in verse (block quotes, line blocks); elsewhere -> space + warning
local function unbreak(inls)
  local n = 0
  local res = pandoc.walk_inline(pandoc.Span(inls), {LineBreak = function() n = n + 1; return pandoc.Space() end}).content
  if n > 0 then warn("forced line break converted to space (only verse quotations keep them): " .. short(inls)) end
  return res
end
local function has_break(inls)
  local found = false
  pandoc.walk_inline(pandoc.Span(inls), {LineBreak = function() found = true end})
  return found
end

---------------------------------------------------------------- pass D: footnote paragraphs
-- Paragraphs stay plain Para: pandoc gives them the Word style "Footnote Text", which build.py
-- renames to the configured footnote style. (Wrapping them in a custom-style Div would push
-- the footnote number into an empty paragraph of its own.)
local function style_note(note)
  local out = pandoc.List()
  for _, b in ipairs(note.content) do
    if b.t == "Para" or b.t == "Plain" then
      out:insert(pandoc.Para(unbreak(b.content)))
    elseif b.t == "BlockQuote" or b.t == "BulletList" or b.t == "OrderedList" or b.t == "Div" then
      warn("block (" .. b.t .. ") inside a footnote flattened to footnote paragraphs")
      pandoc.walk_block(b, {
        Para = function(p) out:insert(pandoc.Para(p.content)) end,
        Plain = function(p) out:insert(pandoc.Para(p.content)) end,
      })
    else
      err("unsupported block in footnote: " .. b.t)
    end
  end
  if #out > 1 and not is_title_note(note) then warn("multi-paragraph footnote (" .. #out .. " paragraphs): " .. short(out[1].content)) end
  note.content = out
  return note
end

---------------------------------------------------------------- pass E: block structure
local function strip_list_dash(inls)
  local f = inls[1]
  if f and f.t == "Str" and (f.text == "–" or f.text == "-" or f.text == "—" or f.text == "•") then
    inls:remove(1)
    trim_leading_space(inls)
  end
  return inls
end

local function has_class(b, name)
  for _, c in ipairs(b.classes or {}) do if c == name then return true end end
  return false
end

-- LineBlock lines -> one paragraph with forced line breaks
function verse(lines)
  local inls = pandoc.List()
  for j, line in ipairs(lines) do
    if j > 1 then inls:insert(pandoc.LineBreak()) end
    inls:extend(line)
  end
  return inls
end

-- kanon §5.3 interlinear example, typed in a fenced block inside ::: przyklad
--   (1)  Me         dikhav       e        čhave.
--        1SG.NOM    widzieć.1SG  DEF.OBL  chłopiec.OBL.PL
--        ‘Widzę chłopców.’
-- line 1 -> example_form, line 2 -> example_gloss, line 3 -> example_trans; runs of 2+ spaces -> tab
-- (tab stops, italic form line, small caps of gloss categories: in the template styles / GREP styles)
function example_lines(text)
  local out, n = pandoc.List(), 0
  for line in (text .. "\n"):gmatch("(.-)\n") do
    if line:match("^%s*$") then
      n = 0
    else
      n = n + 1
      local body = line:gsub("^%s+", ""):gsub("%s%s+", "\t")
      local style = (n == 1) and P.example_form or ((n == 2) and P.example_gloss or P.example_trans)
      if n > 3 then warn("example with more than 3 lines — extra lines set as translation: " .. body) end
      out:insert(styled_para({pandoc.Str(body)}, style))
    end
  end
  return out
end

-- dialogue turn: leading "Mr. Hise:" / "Przewodniczący Coe:" (capital letter, at most 6 words, ends with a
-- colon) -> character style speaker; a turn without such a label is a continuation and stays plain
function speaker_label(inls)
  local n, words = 0, 0
  for i, el in ipairs(inls) do
    if el.t == "Str" then
      words = words + 1
      if i == 1 and not el.text:match("^[%u\xC3\xC4\xC5]") then return inls end
      if el.text:match(":$") then n = i; break end
    elseif el.t ~= "Space" then return inls end
    if words > 6 then return inls end
  end
  if n == 0 then return inls end
  local label, rest = pandoc.List(), pandoc.List()
  for i, el in ipairs(inls) do if i <= n then label:insert(el) else rest:insert(el) end end
  local out = pandoc.List({pandoc.Span(label, cstyle(C.speaker))})
  out:extend(rest)
  return out
end

local process
process = function(blocks, ctx)
  local out = pandoc.List()
  local prev = nil
  for _, b in ipairs(blocks) do
    local t = b.t
    if t == "Header" then
      local style
      if ctx.mode == "bib" then
        style = (b.level == 1) and P.bib_title or P.bib_section
      elseif b.level == 1 then style = P.h1
      elseif b.level == 2 then style = P.h2
      else err("heading level " .. b.level .. " (kanon §2 allows two): " .. short(b.content)); style = P.h2 end
      out:insert(styled_para(b.content, style))
    elseif t == "Para" or t == "Plain" then
      local style
      if ctx.fixed then style = ctx.fixed
      elseif ctx.mode == "bib" then style = P.bib_entry
      elseif prev == nil or prev == "Header" then style = P.body_first
      else style = P.body end
      out:insert(styled_para(unbreak(b.content), style))
    elseif t == "LineBlock" then
      out:insert(styled_para(verse(b.content), P.quote_verse))
    elseif t == "BlockQuote" then
      for _, q in ipairs(b.content) do
        if q.t == "Para" or q.t == "Plain" then
          -- a quoted paragraph with forced line breaks is verse (kanon §4.1 block, lines kept)
          out:insert(styled_para(q.content, has_break(q.content) and P.quote_verse or P.quote))
        elseif q.t == "LineBlock" then
          out:insert(styled_para(verse(q.content), P.quote_verse))
        else err("unsupported block inside block quote: " .. q.t) end
      end
    elseif t == "BulletList" then
      for _, item in ipairs(b.content) do
        for _, ib in ipairs(item) do
          if ib.t == "Para" or ib.t == "Plain" then out:insert(styled_para(strip_list_dash(ib.content), P.list))
          else err("nested structure in list item (" .. ib.t .. ")") end
        end
      end
    elseif t == "OrderedList" then
      -- numbered list: each item a paragraph in list_numbered; the number is typed ("1." + tab), so the
      -- template style only sets indents/tab stop (no InDesign auto-numbering to restart per list)
      local n0 = b.start or 1
      for k, item in ipairs(b.content) do
        for j, ib in ipairs(item) do
          if ib.t == "Para" or ib.t == "Plain" then
            local inls = pandoc.List()
            if j == 1 then inls:insert(pandoc.Str(tostring(n0 + k - 1) .. ".\t")) end
            inls:extend(unbreak(ib.content))
            out:insert(styled_para(inls, P.list_numbered))
          else err("nested structure in numbered list item (" .. ib.t .. ")") end
        end
      end
    elseif t == "Div" then
      if b.identifier == "refs" then
        -- citeproc's own bibliography is suppressed; build.py inserts SROM sections
      elseif b.attributes["custom-style"] then
        out:insert(b)
      elseif has_class(b, "bibliografia") then
        out:extend(process(b.content, {mode = "bib"}))
      elseif has_class(b, "przyklad") then
        out:extend(process(b.content, {example = true, mode = ctx.mode}))
      elseif has_class(b, "motto") then
        -- opening quotation, set in italics by its style: titles inside it turn roman
        for _, x in ipairs(b.content) do
          if x.t == "Para" or x.t == "Plain" then
            local inls = pandoc.walk_inline(pandoc.Span(x.content), {Span = function(sp)
              if sp.attributes["custom-style"] == C.italic then sp.attributes["custom-style"] = C.roman end
              return sp end}).content
            out:insert(styled_para(unbreak(inls), P.motto))
          else err("unsupported block in ::: motto: " .. x.t) end
        end
      elseif has_class(b, "dialog") then
        -- one turn per paragraph; a leading "Name:" becomes the speaker label (character style)
        for _, x in ipairs(b.content) do
          if x.t == "Para" or x.t == "Plain" then out:insert(styled_para(speaker_label(unbreak(x.content)), P.dialog))
          else err("unsupported block in ::: dialog: " .. x.t) end
        end
      elseif has_class(b, "mowca") then
        -- transcript: speaker on a line of its own; a second line = affiliation
        for k, x in ipairs(b.content) do
          if x.t == "Para" or x.t == "Plain" then
            local lines, cur = {}, pandoc.List()
            for _, el in ipairs(x.content) do
              if el.t == "SoftBreak" or el.t == "LineBreak" then table.insert(lines, cur); cur = pandoc.List()
              else cur:insert(el) end
            end
            table.insert(lines, cur)
            for li, line in ipairs(lines) do
              if #line > 0 then out:insert(styled_para(line, (k == 1 and li == 1) and P.speaker or P.speaker_affiliation)) end
            end
          end
        end
      else
        local fixed
        for _, c in ipairs(b.classes) do if R[c] then fixed = P[R[c]] end end
        if not fixed then warn("unknown div class {" .. table.concat(b.classes, " ") .. "} — contents styled as body") end
        out:extend(process(b.content, {fixed = fixed, mode = ctx.mode}))
      end
    elseif t == "Table" then
      -- kanon §10: title above (from the caption or a ::: tabela-tytul div), cells in the table-cell style;
      -- table formatting (rules, widths) is done with the template's table style in InDesign
      local cap = pandoc.utils.blocks_to_inlines(b.caption.long or {})
      if #cap > 0 then
        out:insert(styled_para(cap, P.table_title))
        b.caption.long = pandoc.Blocks({})
      end
      local function cells(rows)
        for _, r in ipairs(rows) do
          for _, c in ipairs(r.cells) do
            local nb = pandoc.List()
            for _, cb in ipairs(c.contents) do
              if cb.t == "Para" or cb.t == "Plain" then nb:insert(styled_para(unbreak(cb.content), P.table_cell))
              else err("unsupported block in a table cell: " .. cb.t) end
            end
            c.contents = nb
          end
        end
      end
      cells(b.head.rows)
      for _, body in ipairs(b.bodies) do cells(body.head); cells(body.body) end
      cells(b.foot.rows)
      warn("table: text styled; apply the template table style in InDesign")
      out:insert(b)
    elseif t == "CodeBlock" then
      if ctx.example then
        out:extend(example_lines(b.text))
      else
        err("code block — interlinear examples go in a ::: przyklad div as a fenced block (kanon §5.3)")
      end
    elseif t == "HorizontalRule" then
      warn("horizontal rule dropped")
    elseif t == "Figure" then
      err("figure — place images in InDesign; keep caption as ::: podpis div")
    else
      err("unsupported block: " .. t)
    end
    -- the paragraph after a heading, a motto or a speaker's line starts without indent (like an opening);
    -- after a block quote or a dialogue it is indented (kanon §2)
    prev = (t == "Header" or (t == "Div" and (has_class(b, "motto") or has_class(b, "mowca")))) and "Header" or t
  end
  return out
end

---------------------------------------------------------------- pass F: the asterisk series (kanon § 7.1)
-- Non-author notes (translator's, editorial) and the title note (::: przypis-tytulowy) are one series *, **, …
-- restarting on every page, set ABOVE the numbered notes. An InDesign story has a single footnote sequence, so
-- they cannot be Word footnotes: in the text a placeholder "*" in the character style asterisk_ref; the notes
-- themselves as paragraphs in asterisk_note at the end of the document, the title note first, each opening
-- with "* ". The typesetter moves them into place and sets the asterisks per page (_gwiazdki.jsx lists them).
local function asterisk_series(doc)
  local title, notes, body = pandoc.List(), pandoc.List(), pandoc.List()
  for _, b in ipairs(doc.blocks) do
    if b.t == "Div" and has_class(b, "przypis-tytulowy") then title:insert(b.content) else body:insert(b) end
  end
  local moved = false
  body = pandoc.Blocks(body):walk({
    Note = function(n)
      if is_title_note(n) and not KEEP_TITLE then
        n.content[1].content:remove(1)          -- the srom-title marker span
        title:insert(n.content)
        moved = true
        return {}
      end
      if is_nonauthor(n.content) then
        notes:insert(n.content)
        return pandoc.Span({pandoc.Str("*")}, cstyle(C.asterisk_ref))
      end
    end,
  })
  local function paras(blocks)
    local out = pandoc.List()
    for _, b in ipairs(blocks) do
      if b.t == "Para" or b.t == "Plain" then
        local inls = pandoc.List()
        if #out == 0 then inls:extend({pandoc.Str("*"), pandoc.Space()}) end
        inls:extend(unbreak(b.content))
        out:insert(styled_para(inls, P.asterisk_note))
      else
        err("unsupported block in a non-author note: " .. b.t)
      end
    end
    return out
  end
  if moved then     -- the paragraph that only carried the title note's marker
    body = body:filter(function(b) return not ((b.t == "Para" or b.t == "Plain") and #b.content == 0) end)
  end
  for _, t in ipairs(title) do body:extend(paras(t)) end
  for _, n in ipairs(notes) do body:extend(paras(n)) end
  doc.blocks = body
  return doc
end

return {
  { Meta = load_cfg },
  { Pandoc = function(doc) doc.blocks = scan_blocks(doc.blocks, false); return doc end },
  { Note = fix_note_cites },
  inline_pass,
  { Note = style_note },
  { Pandoc = asterisk_series },
  { Pandoc = function(doc)
      doc.blocks = process(doc.blocks, {mode = "body"})
      if nerr > 0 then error("SROM: " .. nerr .. " error(s) — see SROM-ERROR lines") end
      return doc
    end },
}
