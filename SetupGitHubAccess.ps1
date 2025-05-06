param (
    [Parameter(Mandatory = $false, Position = 0)]
    [string]$RepoName,

    [Parameter(Mandatory = $false, Position = 1)]
    [string]$Organization,

    [Parameter(Mandatory = $false)]
    [Switch]$Help,

    # Used to indicate that the code is called by Pester to avoid unwanted code execution during Pester testing.
    [Parameter(Mandatory = $false)]
    [Switch]$Pester
)

function Show-Help {
    $separator = "-" * 80
    Write-Host $separator -ForegroundColor Cyan

    @"
    Usage:
    ------
    SetupGitHubAccess.ps1 RepoName Organization
    SetupGitHubAccess.ps1 -Help

    Arguments:
    (0) RepoName: The name of the GitHub repository.
    (1) Organization Acronym for the organization owning the project in GitHub.

    e.g. SetupGitHubAccess.ps1 MyProjectName MyGitHubOrganization
"@ | Write-Host

    Write-Host $separator -ForegroundColor Cyan
}

if (-not $Pester) {
    Write-Host ''
    $dateTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "=[ START $dateTime ]========================[ SetupGitHubAccess.ps1 ]=" -ForegroundColor Blue
    Write-Host "Executing $PSCommandPath..." -ForegroundColor Yellow
    Write-Host "Configure access to https://github.com/$Organization/$RepoName" -ForegroundColor Blue
    if ($ProjectName -eq "" -or $Help) {
        Show-Help
    }
    else {
        Write-Host "Configure access to repository" -ForegroundColor Magenta
        if (-not $Organization) {
            $Organization = $env:VENV_ORGANIZATION_NAME
        }
        if ($Organization -eq "BEE") {
            $Organization = "BrightEdgeeServices"
        }
        elseif ($Organization -eq "Citiq") {
            $Organization = "citiq-prepaid"
        }
        elseif ($Organization -eq "HdT")
        {
            $Organization = "hendrikdutoit"
        }
        elseif ($Organization -eq "RTE")
        {
            $Organization = "RealTimeEvents"
        }
        elseif ($Organization -eq "URS")
        {
            $Organization = "Universal-Rating-System"
        }

        if (-not $RepoName) {
            $RepoName = $env:PROJECT_NAME
        }
        git config push.autoSetupRemote True
        git remote set-url origin https://$env:GH_REPO_ACCESS_CURR_USER@github.com/$Organization/$RepoName
    }
    Write-Host '-[ END SetupGitHubAccess.ps1 ]--------------------------------------------------' -ForegroundColor Cyan
}
Write-Host ''
