# SetupPrivateRepoAccess.ps1
Write-Host ''

function Remove-RepositoryConfiguration {
    param (
        [Object]$RepoDetails
    )
    Write-Host "Remove configuration" -ForegroundColor Magenta
    $command = "poetry source remove $( $RepoDetails.name )"
    Write-Host "Executing: $command" -ForegroundColor Cyan
    Invoke-Expression $command
    $command = "poetry remove $( $RepoDetails.name )"
    Write-Host "Executing: $command" -ForegroundColor Cyan
    Invoke-Expression $command
}

function Publish-RepositoryConfiguration
{
    param (
        [Object]$RepoDetails
    )
    Write-Host "Add configuration" -ForegroundColor Magenta
    $command = "poetry source add --priority=explicit RTE https://github.com/$( $RepoDetails.org )/$( $RepoDetails.name ).git"
    Write-Host "Executing: $command" -ForegroundColor Cyan
    Invoke-Expression $command
    $command = "poetry add --source RTE git+https://github.com/$( $RepoDetails.org )/$( $RepoDetails.name ).git$( $RepoDetails.version_branch )"
    Write-Host "Executing: $command" -ForegroundColor Cyan
    Invoke-Expression $command
}

Write-Host ''
$dateTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "=[ START $dateTime ]===================[ SetupPrivateRepoAccess.ps1 ]=" -ForegroundColor Blue
Write-Host "Executing $PSCommandPath..." -ForegroundColor Yellow

# List of keys to configure in Poetry
poetry config "http-basic.BEE" "__token__" $env:GH_REPO_ACCESS_BEE_LOCAL_USER
poetry config "http-basic.RTE" "__token__" $env:GH_REPO_ACCESS_RTE_LOCAL_USER

$RepoDetails = [PSCustomObject]@{
    name = "PoetryPrivate"
    org = "BrightEdgeeServices"
    version_branch = "#master"
}
Remove-RepositoryConfiguration -RepoDetails $RepoDetails
#Publish-RepositoryConfiguration -RepoDetails $RepoDetails

Write-Host '-[ END SetupPrivateRepoAccess.ps1 ]---------------------------------------------' -ForegroundColor Cyan
Write-Host ''
