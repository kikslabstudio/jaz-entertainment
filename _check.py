import re, json
h = open("movies.js", encoding="utf-8").read()
print("has </script>:", "</script" in h.lower())
print("has backtick:", "`" in h)
print("has dollar-brace:", "${" in h)
try:
    arr = json.loads(re.search(r"window.SCRAPER_MOVIES = (.*);", h, re.S).group(1))
    print("JSON parse OK, count:", len(arr))
    bad = [x.get("title","") for x in arr if ("`" in x.get("title","") or "${" in x.get("title","") or "</" in x.get("title",""))]
    print("bad titles:", bad[:5])
    # titles with single quote (break showToast)
    q = [x.get("title","") for x in arr if "'" in x.get("title","")]
    print("titles with single-quote:", q[:5], "count:", len(q))
except Exception as e:
    print("JSON PARSE FAIL:", repr(e))
