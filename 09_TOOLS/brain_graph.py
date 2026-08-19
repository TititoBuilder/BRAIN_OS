"""
category: Graph & Code Analysis
brain_graph.py - unified BRAIN_OS code graph.
Captures BOTH edge types:
  - subprocess: "X launches Y.py" at runtime (direct + variable-tracked)
  - import:     "X imports Y" within the project
Also extracts each file's one-line description (module docstring / line-2 comment).
Read-only on sources; writes one JSON.
"""
import re, json, ast
from pathlib import Path

ROOT = Path(r"C:\BRAIN_OS")
SKIP = ("\\venv\\", "\\.git\\", "site-packages", "__pycache__")
files = [p for p in ROOT.rglob("*.py") if not any(s in str(p) for s in SKIP)]
SELF = "brain_graph.py"
files = [p for p in files if p.name != SELF]                 # exclude self
by_name = {p.name: str(p.relative_to(ROOT)).replace("\\","/") for p in files}
by_stem = {p.stem: str(p.relative_to(ROOT)).replace("\\","/") for p in files}  # for imports

PY_REF  = re.compile(r'[\\/"\']([\w\-]+\.py)\b')
SUBPROC = re.compile(r'subprocess\.(run|Popen|call|check_output|check_call)')
ASSIGN  = re.compile(r'^\s*([A-Za-z_]\w*)\s*=.*?[\\/"\']([\w\-]+\.py)\b')

def describe(text):
    """First meaningful line of purpose: module docstring, or a 'name — desc' header comment."""
    # try module docstring via AST
    try:
        doc = ast.get_docstring(ast.parse(text))
        if doc:
            first = doc.strip().splitlines()[0].strip()
            # strip leading 'filename.py - ' if present
            return re.sub(r'^[\w\.\-]+\.py\s*[-—:]\s*', '', first).strip()[:120]
    except Exception:
        pass
    # fallback: line 2 comment like "# name.py — desc"
    for ln in text.splitlines()[:6]:
        if ln.strip().startswith("#") and ("—" in ln or "-" in ln):
            return re.sub(r'^#\s*[\w\.\-]+\.py\s*[-—:]\s*', '', ln.strip("# ").strip())[:120]
    return ""

nodes, edges = {}, []
def add_edge(src, tname, line, kind):
    tgt = by_name.get(tname)
    if tgt is None:
        tgt = "EXTERNAL/" + tname
        nodes.setdefault(tgt, {"label": tname, "folder":"(external)", "kb":0, "external":True, "desc":"external / other project"})
    if tgt != src:
        edges.append({"source": src, "target": tgt, "line": line, "kind": kind})

for p in files:
    rid = str(p.relative_to(ROOT)).replace("\\","/")
    text = p.read_text(encoding="utf-8", errors="replace")
    nodes[rid] = {"label": p.name, "folder": p.parent.name,
                  "kb": round(p.stat().st_size/1024,1), "external": False, "desc": describe(text)}
    lines = text.splitlines()

    # subprocess edges (with variable tracking)
    var2py = {}
    for ln in lines:
        m = ASSIGN.search(ln)
        if m: var2py[m.group(1)] = m.group(2)
    for i, line in enumerate(lines):
        if not SUBPROC.search(line): continue
        win = " ".join(lines[i:i+6])
        for m in PY_REF.finditer(win): add_edge(rid, m.group(1), i+1, "subprocess")
        for v, pyn in var2py.items():
            if re.search(r'\b'+re.escape(v)+r'\b', win): add_edge(rid, pyn, i+1, "subprocess")

    # import edges (internal only) via AST
    try:
        tree = ast.parse(text)
        for n in ast.walk(tree):
            mods = []
            if isinstance(n, ast.Import): mods = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom) and n.module: mods = [n.module]
            for mod in mods:
                stem = mod.split(".")[0]
                if stem in by_stem and by_stem[stem] != rid:
                    edges.append({"source": rid, "target": by_stem[stem], "line": getattr(n,"lineno",0), "kind":"import"})
    except Exception:
        pass

# dedupe on (source,target,kind)
seen, uniq = set(), []
for e in edges:
    k=(e["source"],e["target"],e["kind"])
    if k not in seen: seen.add(k); uniq.append(e)

out = {"node_count":len(nodes), "edge_count":len(uniq), "nodes":nodes, "edges":uniq}
dest = ROOT/"02_PROJECTS"/"graphs"/"brain_os_full.json"
dest.write_text(json.dumps(out,indent=2), encoding="utf-8", newline="\n")

sp=[e for e in uniq if e["kind"]=="subprocess"]; im=[e for e in uniq if e["kind"]=="import"]
print(f"Scanned {len(files)} files.  Nodes:{len(nodes)}  subprocess-edges:{len(sp)}  import-edges:{len(im)}\n")
print("=== SUBPROCESS (X launches Y) ===")
for e in sorted(sp,key=lambda x:x['source']): print(f"  {nodes[e['source']]['label']:24} -> {nodes[e['target']]['label']:24} (L{e['line']})")
print("\n=== IMPORT (X imports Y) ===")
for e in sorted(im,key=lambda x:x['source']): print(f"  {nodes[e['source']]['label']:24} -> {nodes[e['target']]['label']:24} (L{e['line']})")
print(f"\nWrote {dest}")