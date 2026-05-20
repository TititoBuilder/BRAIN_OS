# Check apply-status of each patch against its target file

$results = @()

function Check-Patch {
    param($patchName, $targetPath, $oldStr, $newStr, $note="")
    $repo = if ($targetPath -like "*soccer-content-generator*") { "soccer-content-generator" }
            elseif ($targetPath -like "*resolve-mcp-server*") { "resolve-mcp-server" }
            else { "other" }

    if (-not (Test-Path $targetPath)) {
        return [PSCustomObject]@{ Patch=$patchName; Status="TARGET_MISSING"; Repo=$repo; Target=$targetPath; Note=$note }
    }
    $text = Get-Content $targetPath -Raw
    if ($oldStr -and $text.Contains($oldStr)) {
        return [PSCustomObject]@{ Patch=$patchName; Status="NOT_APPLIED"; Repo=$repo; Target=$targetPath; Note=$note }
    }
    if ($newStr -and $text.Contains($newStr)) {
        return [PSCustomObject]@{ Patch=$patchName; Status="APPLIED"; Repo=$repo; Target=$targetPath; Note=$note }
    }
    return [PSCustomObject]@{ Patch=$patchName; Status="UNKNOWN"; Repo=$repo; Target=$targetPath; Note="old not found, new not found -- version mismatch?" }
}

# patch_bridge_render.py
$results += Check-Patch "patch_bridge_render.py" `
    "C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py" `
    "                while project.IsRenderingInProgress():" `
    "while bool(project.IsRenderingInProgress()):"

# patch_parser.py
$results += Check-Patch "patch_parser.py" `
    "C:\Dev\Projects\soccer-content-generator\src\agent\clip_name_parser.py" `
    '"raw_clip_name": raw_clip_name,' `
    '"confidence":    1.0 if subject else 0.5,'

# patch_delete_job.py
$results += Check-Patch "patch_delete_job.py" `
    "C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py" `
    "project.DeleteRenderJobByUUID(job_id)" `
    "pass  # Resolve 20 Free -- method may be None"

# patch_ingest.py
$results += Check-Patch "patch_ingest.py" `
    "C:\Dev\Projects\soccer-content-generator\mcp_ingest.py" `
    "" `
    "from src.agent.clip_name_parser import parse_clip_name" `
    "checks if import replaced inline def"

# patch_ingest_subject.py
$results += Check-Patch "patch_ingest_subject.py" `
    "C:\Dev\Projects\soccer-content-generator\mcp_ingest.py" `
    "" `
    "# Log entry subject (set explicitly in cleanup) wins over parser"

# patch_cleanup_subject.py
$results += Check-Patch "patch_cleanup_subject.py" `
    "C:\Users\titit\Projects\resolve-mcp-server\server_api.py" `
    'competition = arguments.get("competition", "").strip()  # explicit override wins all tiers' `
    'subject     = arguments.get("subject", "").strip()'

# patch_format_b.py
$results += Check-Patch "patch_format_b.py" `
    "C:\Dev\Projects\soccer-content-generator\mcp_ingest.py" `
    "                    full_path = lib_dir / fname" `
    "# Prefer staging path if file is still there"

# patch_enricher.py -- target 1: knowledge_enricher.py
$results += Check-Patch "patch_enricher.py [enricher]" `
    "C:\Dev\Projects\soccer-content-generator\src\agent\knowledge_enricher.py" `
    "def enrich(subject: str, content_type: str, description: str) -> str:" `
    'competition: str = ""'

# patch_enricher.py -- target 2: mcp_ingest.py
$results += Check-Patch "patch_enricher.py [mcp_ingest]" `
    "C:\Dev\Projects\soccer-content-generator\mcp_ingest.py" `
    'parsed["subject"], parsed["content_type"], parsed["description"]' `
    'competition=entry.get("competition", ""),'

# patch_server_api.py
$results += Check-Patch "patch_server_api.py" `
    "C:\Users\titit\Projects\resolve-mcp-server\server_api.py" `
    "        except Exception:" `
    "[competition] tier-2 failed:"

# Output
$results | ForEach-Object {
    $tag = switch ($_.Status) {
        "APPLIED"        { "[APPLIED        ]" }
        "NOT_APPLIED"    { "[NOT_APPLIED    ]" }
        "TARGET_MISSING" { "[TARGET_MISSING ]" }
        default          { "[UNKNOWN        ]" }
    }
    Write-Output "$tag  $($_.Patch)"
    Write-Output "   Repo   : $($_.Repo)"
    Write-Output "   Target : $($_.Target)"
    if ($_.Note) { Write-Output "   Note   : $($_.Note)" }
    Write-Output ""
}
