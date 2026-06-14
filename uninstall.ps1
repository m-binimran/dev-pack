<#
.SYNOPSIS
  Remove dev-pack from a target project. Only deletes files dev-pack installed.
.EXAMPLE
  ./uninstall.ps1 -ProjectPath "C:\path\to\your\project"
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

Write-Host "Removing dev-pack from $ProjectPath" -ForegroundColor Cyan

# 1. hooks (by our filenames only)
Get-ChildItem (Join-Path $src "hooks\*.py") | ForEach-Object {
  $t = Join-Path $ProjectPath ".claude\hooks\$($_.Name)"
  if (Test-Path $t) { Remove-Item $t -Force }
}
# 2. skills (by our folder names)
Get-ChildItem (Join-Path $src "skills") -Directory | ForEach-Object {
  $t = Join-Path $ProjectPath ".claude\skills\$($_.Name)"
  if (Test-Path $t) { Remove-Item $t -Recurse -Force }
}
# 3. loops -> commands
Get-ChildItem (Join-Path $src "loops\*.md") | ForEach-Object {
  $t = Join-Path $ProjectPath ".claude\commands\$($_.Name)"
  if (Test-Path $t) { Remove-Item $t -Force }
}
# 4. agents
Get-ChildItem (Join-Path $src "agents\*.md") | ForEach-Object {
  $t = Join-Path $ProjectPath ".claude\agents\$($_.Name)"
  if (Test-Path $t) { Remove-Item $t -Force }
}
Write-Host "  removed hooks, skills, commands, agents" -ForegroundColor Green

# 5. strip the appended rules block from CLAUDE.md (from our marker to end)
$claudeMd = Join-Path $ProjectPath "CLAUDE.md"
$marker = "<!-- ===== dev-pack rules (auto-installed) ===== -->"
if (Test-Path $claudeMd) {
  $content = Get-Content $claudeMd -Raw -Encoding UTF8
  $idx = $content.IndexOf($marker)
  if ($idx -ge 0) {
    ($content.Substring(0, $idx).TrimEnd() + "`n") | Set-Content $claudeMd -Encoding utf8 -NoNewline
    Write-Host "  stripped dev-pack rules from CLAUDE.md" -ForegroundColor Green
  } else {
    Write-Warning "Marker not found in CLAUDE.md; remove the dev-pack rules manually."
  }
}

# 6. settings.json (only remove if it is exactly ours)
$settingsDest = Join-Path $ProjectPath ".claude\settings.json"
$settingsSrc = Join-Path $src "hooks\settings.json"
if (Test-Path $settingsDest) {
  $a = (Get-Content $settingsDest -Raw).Trim()
  $b = (Get-Content $settingsSrc -Raw).Trim()
  if ($a -eq $b) {
    Remove-Item $settingsDest -Force
    Write-Host "  removed .claude\settings.json (was dev-pack's)" -ForegroundColor Green
  } else {
    Write-Warning ".claude\settings.json has your own changes; remove the dev-pack 'hooks' block manually."
  }
}

Write-Host "Done. Restart Claude Code so the changes take effect." -ForegroundColor Cyan
