param (
    [Parameter(Mandatory = $false, Position = 0)]
    [string]$Variant,

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
    SetUpDocker.ps1 -Variant VariantName
    SetUpDocker.ps1 -Help

    Arguments:
    (0) Variant: Set the docker compose configuration file. If no variant name is
                 provided it will configure docker-compose.yaml else if the variant
                 name is "myvaraint" it will configure docker-compose-myvariant.yaml.
    e.g. SetUpDocker.ps1 MyVariant
"@ | Write-Host

    Write-Host $separator -ForegroundColor Cyan
}

if (-not $Pester) {
    Write-Host ''
    $dateTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "=[ START $dateTime ]=============================[ SetUpDocker.ps1 ]=" -ForegroundColor Blue
    Write-Host "Executing $PSCommandPath..." -ForegroundColor Yellow
    Write-Host "Create and start Docker containers." -ForegroundColor Yellow

    if ($ProjectName -eq "" -or $Help) {
        Show-Help
    }
    else {
        $DockerConfigFileName = "docker-compose.yaml"
        if ($Variant) {
            $DockerConfigFileName = "docker-compose-$Variant.yaml"
        }
        if (Test-Path $DockerConfigFileName) {
            if (Test-Path ./CreateDbSqlScript.ps1) {
                & ./CreateDbSqlScript.ps1
            }
            docker compose -f $DockerConfigFileName down -v
            docker compose -f $DockerConfigFileName rm --force
            docker volume prune -a  --force
            docker builder prune --force
            docker compose -f $DockerConfigFileName create
            docker compose -f $DockerConfigFileName start
        }
        else {
            Write-Host "The $DockerConfigFileName does not exist!" -ForegroundColor Red
        }

        Write-Host '-[ END SetUpDocker ]------------------------------------------------------------' -ForegroundColor Cyan
        Write-Host ''
    }
}
