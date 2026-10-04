# build/orig/<skill> must equal today's source (junk excluded)
. tools/sources.sh
n=0
for s in $SKILLS; do
  d=$(diff -rq -x __pycache__ -x .DS_Store -x '*.pyc' "$(src_of $s)" "build/orig/$s" 2>&1)
  if [ -z "$d" ]; then n=$((n+1)); else echo "DIFF $s: $d" | head -5; fi
done
echo "ORIG IDENTICAL $n/6"
