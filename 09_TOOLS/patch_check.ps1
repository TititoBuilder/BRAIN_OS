$dl = 'C:\Knowledge\BDF\BDF_Book\incoming\Downloads'
$repo = 'C:\Dev\Projects\soccer-content-generator'

$patches = @(
    'patch_bridge_render.py',
    'patch_parser.py',
    'patch_delete_job.py',
    'patch_ingest.py',
    'patch_ingest_subject.py',
    'patch_cleanup_subject.py',
    'patch_format_b.py',
    'patch_enricher.py',
    'patch_server_api.py'
)

# Build index of all non-venv .py files in repo
$repoFiles = Get-ChildItem $repo -Recurse -Filter '*.py' -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\(venv|node_modules|__pycache__)\\' }

foreach ($patch in $patches) {
    $patchPath = Join-Path $dl $patch
    $patchContent = Get-Content $patchPath -Raw

    # Extract def/class names as fingerprint
    $defs = [regex]::Matches($patchContent, '(?m)^(?:def|class)\s+(\w+)') |
        ForEach-Object { $_.Groups[1].Value }

    # 1. Check exact filename match
    $nameMatch = $repoFiles | Where-Object { $_.Name -eq $patch }
    if ($nameMatch) {
        $repoContent = Get-Content $nameMatch.FullName -Raw
        if ($repoContent -eq $patchContent) {
            Write-Output "FOUND_IN_REPO (identical)  $patch -> $($nameMatch.FullName)"
        } else {
            Write-Output "FOUND_IN_REPO (similar)    $patch -> $($nameMatch.FullName)"
        }
        continue
    }

    # 2. Check if any def/class names exist in repo files
    $similarFound = $false
    if ($defs.Count -gt 0) {
        foreach ($def in $defs) {
            $pattern = "(?m)^(?:def|class)\s+$def\b"
            $hit = $repoFiles | Where-Object {
                try { (Get-Content $_.FullName -Raw) -match $pattern } catch { $false }
            } | Select-Object -First 1
            if ($hit) {
                Write-Output "FOUND_IN_REPO (similar)    $patch  [fn:$def] -> $($hit.FullName)"
                $similarFound = $true
                break
            }
        }
    }

    if (-not $similarFound) {
        Write-Output "NOT_IN_REPO                $patch  [defs: $($defs -join ', ')]"
    }
}
