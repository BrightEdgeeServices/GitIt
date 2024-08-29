Write-Host "Running $env:PROJECT_DIR\install.ps1..."  -ForegroundColor Yellow
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
poetry init
poetry config keyring.enabled false
if (Test-Path -Path "$env:PROJECT_DIR\pyproject.toml") {
    poetry install --with dev
}
pre-commit install
pre-commit autoupdate

