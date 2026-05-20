$dir = 'C:\Knowledge\MCP\MCP_Book\incoming\_review'

Get-ChildItem $dir -File | Sort-Object Name | ForEach-Object {
    $f     = $_
    $lines = Get-Content $f.FullName -TotalCount 3 -ErrorAction SilentlyContinue
    Write-Output ("=== " + $f.Name + " | " + $f.Length + " bytes")
    if ($lines) {
        $lines | ForEach-Object { Write-Output ("  " + $_) }
    } else {
        Write-Output "  [empty or unreadable]"
    }
    Write-Output ""
}

Write-Output ("--- MCP_Book folder created: " + (Get-Item 'C:\Knowledge\MCP\MCP_Book').CreationTime)
