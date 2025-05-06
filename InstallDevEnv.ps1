Write-Host ''
$dateTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "=[ START $dateTime ]============================[ InstallDevEnv.ps1 ]=" -ForegroundColor Blue
Write-Host "Executing $PSCommandPath..." -ForegroundColor Yellow

(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
poetry init
& "$env:PROJECT_DIR\SetupDotEnv.ps1"
if (Test-Path -Path "$env:PROJECT_DIR\SetupGitHubAccess.ps1") {
    & "$env:PROJECT_DIR\SetupGitHubAccess"

} else {
    Write-Host "No $env:PROJECT_DIR\SetupGitHubAccess.ps1 file"
}
if (Test-Path -Path "$env:PROJECT_DIR\SetupPrivateRepoAccess.ps1") {
    & "$env:PROJECT_DIR\SetupPrivateRepoAccess.ps1"
}
if (Test-Path -Path "$env:PROJECT_DIR\pyproject.toml") {
    poetry lock
    poetry install --with dev
    Poetry sync --with dev
}
pre-commit install
pre-commit autoupdate
if (Test-Path -Path "$env:PROJECT_DIR\DockerRebuild.ps1") {
    & "$env:PROJECT_DIR\DockerRebuild.ps1"
}
Write-Host '-[ END InstallDevEnv.ps1 ]------------------------------------------------------' -ForegroundColor Cyan
Write-Host ''
