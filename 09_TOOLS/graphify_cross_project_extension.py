# =============================================================================
# CROSS-PROJECT SYSTEM MAP
# Paste these three helpers + builder above def main(), and the dispatch block
# inside main() right after `args = parser.parse_args()`.
# =============================================================================

def _scan_editable(venv: Path, packages: list[str]) -> list[str]:
    """Return which shared packages are editable-installed in this venv.

    The reliable editable-install marker is __editable__.<pkg>-*.pth in
    site-packages (a plain .dist-info alone means a regular install).
    """
    site = venv / "Lib" / "site-packages"
    if not site.is_dir():
        return []
    found: list[str] = []
    for pkg in packages:
        if list(site.glob(f"__editable__.{pkg}-*.pth")):
            found.append(pkg)
    return found


def _scan_deploys(root: Path, detect: dict) -> list[str]:
    """Return deploy targets whose marker files exist at the project root."""
    targets: list[str] = []
    for target in ("railway", "vercel"):
        for marker in detect.get(target, []):
            if (root / marker).exists():
                targets.append(target)
                break
    return targets


def _scan_drive(root: Path, detect: dict) -> bool:
    """True if any Drive marker file exists anywhere in the project tree."""
    markers = detect.get("drive", [])
    for marker in markers:
        if (root / marker).exists():
            return True
        if next(root.rglob(marker), None) is not None:
            return True
    return False


def build_cross_project_graph(manifest: dict) -> dict:
    """Build the cross-project system map.

    Mirrors build_graph's five-key envelope so downstream consumers read it
    without special-casing. Nodes are whole projects; edges (venv, shared
    packages, deploys, drive) are derived live from each project's filesystem.
    """
    shared: list[str] = manifest.get("shared_packages", [])
    detect: dict = manifest.get("detect", {})
    nodes: dict = {}

    for proj in manifest["projects"]:
        root = Path(proj["root"])
        venv = Path(proj["venv"]) if proj.get("venv") else None
        nodes[proj["name"]] = {
            "root": proj["root"],
            "exists": root.is_dir(),
            "venv": proj.get("venv"),
            "shared_packages": _scan_editable(venv, shared) if venv else [],
            "deploys": _scan_deploys(root, detect) if root.is_dir() else [],
            "uses_drive": _scan_drive(root, detect) if root.is_dir() else False,
        }

    return {
        "project": manifest["project"],
        "root": "(cross-project)",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "node_count": len(nodes),
        "nodes": nodes,
    }


def write_cross_project_context_md(graph: dict, out_path: Path) -> None:
    """Render the derived human-readable system map (single source = graph)."""
    lines: list[str] = []
    lines.append(f"# System Map — {graph['project']}")
    lines.append("")
    lines.append(f"Generated: {graph['updated_at']}")
    lines.append(f"Projects: {graph['node_count']}")
    lines.append("")
    lines.append("| Project | Exists | Venv | Shared pkgs | Deploys | Drive |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for name, n in graph["nodes"].items():
        venv = n["venv"] or "—"
        pkgs = ", ".join(n["shared_packages"]) or "—"
        deploys = ", ".join(n["deploys"]) or "—"
        drive = "yes" if n["uses_drive"] else "—"
        exists = "yes" if n["exists"] else "MISSING"
        lines.append(f"| {name} | {exists} | {venv} | {pkgs} | {deploys} | {drive} |")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


# ---- dispatch block: paste inside main() right after args = parser.parse_args() ----
#
#     if args.cross_project:
#         manifest_path = Path(
#             r"C:\BRAIN_OS\02_PROJECTS\graphs\projects.manifest.json"
#         )
#         if not manifest_path.exists():
#             sys.exit(f"[graph] Manifest not found: {manifest_path}")
#         manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
#         graph = build_cross_project_graph(manifest)
#         out = Path(manifest["output"])
#         out.parent.mkdir(parents=True, exist_ok=True)
#         out.write_text(json.dumps(graph, indent=2), encoding="utf-8", newline="\n")
#         context_path = out.parent / (out.stem + ".context.md")
#         write_cross_project_context_md(graph, context_path)
#         print(f"[graph] cross-project map: {graph['node_count']} projects -> {out}")
#         print(f"[graph] context: {context_path}")
#         return
#
# ---- and add this argument next to the existing parser.add_argument calls ----
#
#     parser.add_argument(
#         "--cross-project",
#         action="store_true",
#         help="Build cross-project system map from projects.manifest.json",
#     )
