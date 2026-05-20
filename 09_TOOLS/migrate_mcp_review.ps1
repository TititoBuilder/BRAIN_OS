$src  = 'C:\Knowledge\MCP\MCP_Book\incoming\_review'
$dest = 'C:\Knowledge\BDF\BDF_Book\incoming'

$files = @(
    'UNKNOWN_TAG_ch17_clip_name_parser_session_compile_2026_04_26.txt',
    'UNKNOWN_TAG_ch18_competition_detection_session_compile_2026_04_26.txt',
    'UNKNOWN_TAG_ch19_export_pipeline_session_compile_2026_04_26.txt',
    'UNKNOWN_TAG_ch20_format_b_path_resolution_session_compile_2026_04_26.txt'
)

foreach ($fname in $files) {
    $srcPath  = Join-Path $src $fname
    $newName  = $fname -replace '^UNKNOWN_TAG_', '' -replace '\.txt$', '.md'
    $destPath = Join-Path $dest $newName

    $content  = [System.IO.File]::ReadAllText($srcPath, [System.Text.Encoding]::UTF8)
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($destPath, $content, $utf8NoBom)

    Remove-Item $srcPath
    Write-Output "MOVED  $fname"
    Write-Output "    -> $newName"
    Write-Output ""
}

$mcpRoot    = 'C:\Knowledge\MCP\MCP_Book'
$remaining  = Get-ChildItem $mcpRoot -Recurse -File -ErrorAction SilentlyContinue

if ($remaining.Count -eq 0) {
    Write-Output "MCP_Book has no files remaining. Deleting folder..."
    Remove-Item $mcpRoot -Recurse -Force
    if (-not (Test-Path $mcpRoot)) {
        Write-Output "DELETED  C:\Knowledge\MCP\MCP_Book\"
    }
} else {
    $n = $remaining.Count
    Write-Output "MCP_Book still has $n file(s) - NOT deleted."
    $remaining | Select-Object -ExpandProperty FullName | Write-Output
}
