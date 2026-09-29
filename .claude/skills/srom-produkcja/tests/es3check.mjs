// ES3 syntax check (acorn ecmaVersion 3) + ES5-API denylist for ExtendScript.
import { createRequire } from "module";
import fs from "fs";
import os from "os";
const require = createRequire(import.meta.url);
let acorn = null;
for (const p of [process.env.ACORN || "", "/home/claude/es3/node_modules/acorn",
                 os.homedir() + "/.venvs/srom/node/node_modules/acorn", "acorn"]) {
  if (!p) continue;
  try { acorn = require(p); break; } catch (e) {}
}
let bad = 0;
for (const f of process.argv.slice(2)) {
  const src = fs.readFileSync(f, "utf8");
  if (acorn) {
    try { acorn.parse(src, { ecmaVersion: 3, allowReserved: true }); }
    catch (e) { console.log(`FAIL ${f}: ES3 syntax: ${e.message}`); bad++; continue; }
  } else {
    try { new Function(src); } catch (e) { console.log(`FAIL ${f}: ${e.message}`); bad++; continue; }
  }
  const deny = [/\.forEach\(/, /\.map\(/, /\.filter\(/, /\.trim\(/, /\bJSON\./, /Array\.isArray/, /Object\.keys/, /\.bind\(/, /\blet\s/, /\bconst\s/, /=>/, /`/];
  const code = src.replace(/\/\/.*$/gm, "");
  for (const rx of deny) if (rx.test(code)) { console.log(`FAIL ${f}: non-ES3 API ${rx}`); bad++; }
  if (!bad) console.log(`ok ${f}${acorn ? " (acorn es3)" : " (fallback parse)"}`);
}
console.log(bad ? `JSX FAIL ${bad}` : "JSX-DONE");
