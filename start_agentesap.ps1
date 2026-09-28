$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating Python virtual environment..."
    py -3.12 -m venv .venv
}

$Python = Join-Path $Root ".venv\Scripts\python.exe"

Write-Host "Installing/updating dependencies..."
& $Python -m pip install --upgrade pip
& $Python -m pip install -r requirements.txt

if (-not $env:GITHUB_OWNER) { $env:GITHUB_OWNER = "araortiz99" }
if (-not $env:GITHUB_REPO) { $env:GITHUB_REPO = "agenteSAP" }
if (-not $env:GITHUB_REF) { $env:GITHUB_REF = "main" }

Write-Host ""
Write-Host "AgenteSAP: local read-only workbench"
Write-Host "Repository: $env:GITHUB_OWNER/$env:GITHUB_REPO"
Write-Host "Ref:        $env:GITHUB_REF"
Write-Host "SAP writes: disabled"
Write-Host ""

& $Python -m src.app
