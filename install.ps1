<#
.SYNOPSIS
  Install dev-pack into a target project.
.EXAMPLE
  ./install.ps1 -ProjectPath "C:\Users\me\my-app"
#>
param(
  [Parameter(Mandatory = $true)]
  [string]$ProjectPath
)

$ErrorActionPreference = "Stop"
$src = $PSScriptRoot

if (-not (Test-Path $ProjectPath)) {
  throw "Project path not found: $ProjectPath"
}

Write-Host "Installing dev-pack into $ProjectPath" -ForegroundColor Cyan

# 1. Verify Python is available (hooks need it)
$python = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $python) {
  Write-Warning "Python 3 not found on PATH. Hooks will not run until Python is installed."
}

# 2. Copy hooks -> <project>/.claude/hooks
$hooksDest = Join-Path $ProjectPath ".claude\hooks"
New-Item -ItemType Directory -Force -Path $hooksDest | Out-Null
Copy-Item -Path (Join-Path $src "hooks\*.py") -Destination $hooksDest -Force
Write-Host "  hooks  -> .claude\hooks" -ForegroundColor Green

# 3. skills -> .claude/skills, loops + commands -> .claude/commands, agents -> .claude/agents
$map = @{ "skills" = "skills"; "loops" = "commands"; "commands" = "commands"; "agents" = "agents" }
foreach ($srcDir in $map.Keys) {
  $destName = $map[$srcDir]
  $dest = Join-Path $ProjectPath ".claude\$destName"
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  Copy-Item -Path (Join-Path $src "$srcDir\*") -Destination $dest -Recurse -Force
  Write-Host "  $srcDir -> .claude\$destName" -ForegroundColor Green
}

# 4. Append rules into <project>/CLAUDE.md
$claudeMd = Join-Path $ProjectPath "CLAUDE.md"
$banner = "`n`n<!-- ===== dev-pack rules (auto-installed) ===== -->`n"
Add-Content -Path $claudeMd -Value $banner -Encoding utf8
Get-ChildItem (Join-Path $src "rules\*.md") | Sort-Object Name | ForEach-Object {
  Add-Content -Path $claudeMd -Value (Get-Content $_.FullName -Raw -Encoding UTF8) -Encoding utf8
  Add-Content -Path $claudeMd -Value "`n" -Encoding utf8
}
Write-Host "  rules  -> CLAUDE.md (appended)" -ForegroundColor Green

# 5. Merge settings.json (manual-merge if one already exists)
$settingsDest = Join-Path $ProjectPath ".claude\settings.json"
$settingsSrc = Join-Path $src "hooks\settings.json"
if (Test-Path $settingsDest) {
  Copy-Item $settingsSrc (Join-Path $ProjectPath ".claude\settings.dev-pack.json") -Force
  Write-Warning "settings.json already exists. Wrote settings.dev-pack.json next to it - merge the 'hooks' block manually."
} else {
  Copy-Item $settingsSrc $settingsDest -Force
  Write-Host "  hooks  -> .claude\settings.json" -ForegroundColor Green
}

Write-Host "`nDone. Restart Claude Code in the project so hooks load." -ForegroundColor Cyan
