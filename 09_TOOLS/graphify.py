"""
graphify.py — BDF project graph builder.

Usage:
  python graphify.py [--config PATH] [--force] [--header]

Flags:
  --config  Path to .graphify.json config (default: soccer-content-generator.graphify.json)
  --force   Reprocess every node regardless of hash
  --header  Print existing .context.md and exit
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Stdlib module set (Python 3.10+). Fallback to empty set on older builds.
# ---------------------------------------------------------------------------
_STDLIB: frozenset[str] = (
    frozenset(sys.stdlib_module_names)
    if hasattr(sys, "stdlib_module_names")
    else frozenset()
)
_BUILTINS: frozenset[str] = frozenset(sys.builtin_module_names)


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def _md5(path: Path, length: int = 12) -> str:
    h = hashlib.md5(path.read_bytes(), usedforsecurity=False)
    return h.hexdigest()[:length]


def _should_skip(path: Path, patterns: list[str]) -> bool:
    s = str(path)
    return any(p in s for p in patterns)


def _parse_top_level_imports(path: Path) -> list[str]:
    """Return module names referenced by top-level import / from-import statements."""
    try:
        tree = ast.parse(path.read_bytes())
    except SyntaxError:
        return []
    names: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.append(node.module)
    return names


def _format_args(args_node: ast.arguments) -> str:
    parts: list[str] = []
    for arg in args_node.args:
        parts.append(arg.arg)
    if args_node.vararg:
        parts.append(f"*{args_node.vararg.arg}")
    for arg in args_node.kwonlyargs:
        parts.append(arg.arg)
    if args_node.kwarg:
        parts.append(f"**{args_node.kwarg.arg}")
    return ", ".join(parts)


def _parse_signatures(path: Path) -> list[str]:
    """Extract top-level function/class signatures (names + params, no bodies)."""
    try:
        tree = ast.parse(path.read_bytes())
    except SyntaxError:
        return []
    sigs: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
            sigs.append(f"{prefix} {node.name}({_format_args(node.args)})")
        elif isinstance(node, ast.ClassDef):
            bases = [ast.unparse(b) for b in node.bases] if node.bases else []
            base_str = f"({', '.join(bases)})" if bases else ""
            sigs.append(f"class {node.name}{base_str}")
            for item in ast.iter_child_nodes(node):
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    prefix = "async def" if isinstance(item, ast.AsyncFunctionDef) else "def"
                    sigs.append(f"  {prefix} {item.name}({_format_args(item.args)})")
    return sigs


def _classify(
    names: list[str],
    internal: frozenset[str],
    ext_packages: frozenset[str],
) -> dict[str, list[str]]:
    stdlib_out, internal_out, external_out = [], [], []
    for name in names:
        root = name.split(".")[0]
        if root in internal or name in internal:
            internal_out.append(name)
        elif root in ext_packages:
            external_out.append(name)
        elif root in _STDLIB or root in _BUILTINS:
            stdlib_out.append(name)
        else:
            external_out.append(name)  # unknown third-party
    return {
        "stdlib": sorted(set(stdlib_out)),
        "internal": sorted(set(internal_out)),
        "external": sorted(set(external_out)),
    }


# ---------------------------------------------------------------------------
# Layer assignment
# ---------------------------------------------------------------------------

def _assign_layer(rel: str, layers: dict[str, list[str]]) -> str:
    norm = rel.replace("\\", "/")
    for layer_name, patterns in layers.items():
        for pattern in patterns:
            if pattern.endswith("/"):
                if norm.startswith(pattern):
                    return layer_name
            else:
                if norm == pattern:
                    return layer_name
    return "uncategorized"


# ---------------------------------------------------------------------------
# Core graph builder
# ---------------------------------------------------------------------------

def build_graph(
    config: dict,
    existing_graph: dict | None,
    *,
    force: bool,
) -> dict:
    root = Path(config["root"])
    threshold_kb: float = config.get("header_only_threshold_kb", 50)
    skip_patterns: list[str] = config.get("skip_patterns", [])
    ext_packages: frozenset[str] = frozenset(config.get("external_packages", []))
    layers: dict[str, list[str]] = config.get("layers", {})

    # Collect all live .py files
    live_files: dict[str, Path] = {}
    for f in root.rglob("*.py"):
        if not _should_skip(f, skip_patterns):
            rel = str(f.relative_to(root)).replace("\\", "/")
            live_files[rel] = f

    # Build internal module name set from all live file paths
    internal_names: set[str] = set()
    for rel in live_files:
        without_ext = rel.removesuffix(".py")
        module_dotted = without_ext.replace("/", ".")
        parts = module_dotted.split(".")
        for i in range(len(parts)):
            internal_names.add(".".join(parts[i:]))
    internal_frozen = frozenset(internal_names)

    existing_nodes: dict = existing_graph.get("nodes", {}) if existing_graph else {}
    new_nodes: dict = {}

    for rel, f in sorted(live_files.items()):
        file_hash = _md5(f)

        # Carry forward unchanged nodes
        if (
            not force
            and rel in existing_nodes
            and existing_nodes[rel].get("hash") == file_hash
        ):
            new_nodes[rel] = existing_nodes[rel]
            continue

        size_kb = round(f.stat().st_size / 1024, 1)
        layer = _assign_layer(rel, layers)

        if size_kb >= threshold_kb:
            node = {
                "hash": file_hash,
                "layer": layer,
                "size_kb": size_kb,
                "mode": "header_only",
                "signatures": _parse_signatures(f),
            }
        else:
            raw_imports = _parse_top_level_imports(f)
            node = {
                "hash": file_hash,
                "layer": layer,
                "size_kb": size_kb,
                "mode": "full",
                "imports": _classify(raw_imports, internal_frozen, ext_packages),
            }

        new_nodes[rel] = node

    return {
        "project": config["project"],
        "root": config["root"],
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "node_count": len(new_nodes),
        "nodes": new_nodes,
    }


# ---------------------------------------------------------------------------
# context.md writer
# ---------------------------------------------------------------------------

def write_context_md(graph: dict, config: dict, out_path: Path) -> None:
    ext_packages: frozenset[str] = frozenset(config.get("external_packages", []))

    # Group nodes by layer
    by_layer: dict[str, list[tuple[str, dict]]] = {}
    for rel, node in graph["nodes"].items():
        by_layer.setdefault(node["layer"], []).append((rel, node))

    # Check if brain_audio appears anywhere
    brain_audio_users = [
        rel for rel, node in graph["nodes"].items()
        if "brain_audio" in node.get("imports", {}).get("external", [])
    ]

    lines: list[str] = [
        f"# {graph['project']} — dependency context",
        f"_updated: {graph['updated_at']}_",
        f"_nodes: {graph['node_count']}_",
        "",
    ]
    if brain_audio_users:
        lines.append("> **[shared-core]** `brain_audio` detected in: " + ", ".join(f"`{r}`" for r in brain_audio_users))
        lines.append("")

    for layer_name in sorted(by_layer.keys()):
        lines.append(f"## {layer_name}")
        for rel, node in sorted(by_layer[layer_name]):
            size = node["size_kb"]
            if node["mode"] == "header_only":
                lines.append(f"- **{rel}** ({size} KB) `[HEADER ONLY - read on demand]`")
                for sig in node.get("signatures", []):
                    lines.append(f"  - `{sig}`")
            else:
                imp = node.get("imports", {})
                internal = imp.get("internal", [])
                external = imp.get("external", [])
                parts: list[str] = []
                if internal:
                    parts.append("internal: " + ", ".join(f"`{m}`" for m in internal))
                if external:
                    flagged = [
                        f"`{m}` [shared-core]" if m.split(".")[0] == "brain_audio" else f"`{m}`"
                        for m in external
                    ]
                    parts.append("external: " + ", ".join(flagged))
                dep_str = " — " + "; ".join(parts) if parts else ""
                lines.append(f"- **{rel}** ({size} KB){dep_str}")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Cross-project system map
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    default_config = str(
        Path(r"C:\BRAIN_OS\02_PROJECTS\graphs\soccer-content-generator.graphify.json")
    )
    parser = argparse.ArgumentParser(description="BDF graph builder")
    parser.add_argument("--config", default=default_config, help="Path to .graphify.json")
    parser.add_argument("--force", action="store_true", help="Reprocess all nodes")
    parser.add_argument("--header", action="store_true", help="Print existing .context.md and exit")
    parser.add_argument("--cross-project", action="store_true", help="Build cross-project system map from projects.manifest.json")
    args = parser.parse_args()

    if args.cross_project:
        manifest_path = Path(
            r"C:\BRAIN_OS\02_PROJECTS\graphs\projects.manifest.json"
        )
        if not manifest_path.exists():
            sys.exit(f"[graph] Manifest not found: {manifest_path}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        graph = build_cross_project_graph(manifest)
        out = Path(manifest["output"])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(graph, indent=2), encoding="utf-8", newline="\n")
        context_path = out.parent / (out.stem + ".context.md")
        write_cross_project_context_md(graph, context_path)
        print(f"[graph] cross-project map: {graph['node_count']} projects -> {out}")
        print(f"[graph] context: {context_path}")
        return

    config_path = Path(args.config)
    if not config_path.exists():
        sys.exit(f"[graph] Config not found: {config_path}")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    graph_output = Path(config["graph_output"])
    context_path = graph_output.parent / (graph_output.stem + ".context.md")

    if args.header:
        if context_path.exists():
            print(context_path.read_text(encoding="utf-8"))
        else:
            print(f"[graph] No context file found: {context_path}")
        return

    existing_graph: dict | None = None
    if graph_output.exists():
        existing_graph = json.loads(graph_output.read_text(encoding="utf-8"))

    graph = build_graph(config, existing_graph, force=args.force)

    graph_output.parent.mkdir(parents=True, exist_ok=True)
    graph_output.write_text(json.dumps(graph, indent=2), encoding="utf-8")
    write_context_md(graph, config, context_path)

    header_only = sum(1 for n in graph["nodes"].values() if n["mode"] == "header_only")
    print(f"[graph] {graph['node_count']} nodes written -> {graph_output}")
    print(f"[graph] header_only: {header_only}  full: {graph['node_count'] - header_only}")
    print(f"[graph] context: {context_path}")


if __name__ == "__main__":
    main()
