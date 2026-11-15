# PeWoNu installer for Windows (PowerShell). One command installs uv, Python, the code and every
# dependency, then starts the system:
#   irm https://raw.githubusercontent.com/MrT-coder/pewonu/develop/install.ps1 | iex
# Optional environment variables: PEWONU_DIR (default ~\pewonu), PEWONU_BRANCH (default develop),
# PEWONU_REPO (git URL), PEWONU_NO_START=1 (install only, do not start).
$ErrorActionPreference = "Stop"

$Repo = if ($env:PEWONU_REPO) { $env:PEWONU_REPO } else { "https://github.com/MrT-coder/pewonu.git" }
$Branch = if ($env:PEWONU_BRANCH) { $env:PEWONU_BRANCH } else { "develop" }
$Dir = if ($env:PEWONU_DIR) { $env:PEWONU_DIR } else { Join-Path $HOME "pewonu" }

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "==> Installing uv (it also downloads the right Python for you)"
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    $env:Path = "$HOME\.local\bin;$env:Path"
}

if (Test-Path (Join-Path $Dir ".git")) {
    Write-Host "==> Updating $Dir"
    git -C $Dir pull --ff-only
} elseif (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "==> Downloading PeWoNu to $Dir"
    git clone --depth 1 --branch $Branch $Repo $Dir
} else {
    Write-Host "==> git not found: downloading the source archive to $Dir"
    $Zip = Join-Path ([System.IO.Path]::GetTempPath()) "pewonu.zip"
    $Tmp = Join-Path ([System.IO.Path]::GetTempPath()) "pewonu-src"
    Invoke-WebRequest "https://github.com/MrT-coder/pewonu/archive/refs/heads/$Branch.zip" -OutFile $Zip
    if (Test-Path $Tmp) { Remove-Item $Tmp -Recurse -Force }
    Expand-Archive $Zip -DestinationPath $Tmp
    New-Item -ItemType Directory -Force $Dir | Out-Null
    Copy-Item (Join-Path (Get-ChildItem $Tmp | Select-Object -First 1).FullName "*") $Dir -Recurse -Force
}

Set-Location $Dir
Write-Host "==> Installing Python and dependencies (first time takes a few minutes)"
uv sync --extra astronaut --extra ground
if ($LASTEXITCODE -ne 0) { throw "uv sync failed" }

Write-Host ""
Write-Host "PeWoNu is installed in $Dir"
Write-Host "Start it any time with:  cd `"$Dir`"; uv run pewonu"
Write-Host "Astronaut app: http://127.0.0.1:8550  (codes AST-0001, AST-0002, AST-0003)"
Write-Host "Ground base:   http://127.0.0.1:8560"
if ($env:PEWONU_NO_START -eq "1") { return }
Write-Host "==> Starting PeWoNu (press Ctrl+C to stop)"
uv run pewonu
