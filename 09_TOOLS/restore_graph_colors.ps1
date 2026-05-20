# Restore Obsidian graph color groups
# Run with Obsidian CLOSED

$graphPath = "C:\BRAIN_OS\.obsidian\graph.json"
$graph = Get-Content $graphPath -Raw | ConvertFrom-Json

$graph.colorGroups = @(
    @{ query = "path:10_CHATS";     color = @{ a = 1; rgb = 4886754  } },
    @{ query = "path:02_PROJECTS";  color = @{ a = 1; rgb = 8311585  } },
    @{ query = "path:09_TOOLS";     color = @{ a = 1; rgb = 16098851 } },
    @{ query = "path:02_AGENTS";    color = @{ a = 1; rgb = 12390624 } },
    @{ query = "path:07_SYSTEM";    color = @{ a = 1; rgb = 5065804  } },
    @{ query = "path:08_SESSIONS";  color = @{ a = 1; rgb = 15241817 } },
    @{ query = "path:01_DOMAINS";   color = @{ a = 1; rgb = 14543876 } },
    @{ query = "path:03_APIS";      color = @{ a = 1; rgb = 270480   } },
    @{ query = "path:08_TRIGGERS";  color = @{ a = 1; rgb = 16711680 } }
)

$json = $graph | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($graphPath, $json)
Write-Host "Graph colors restored." -ForegroundColor Green