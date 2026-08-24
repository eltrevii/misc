@(set "0=%~f0"^)#) & powershell -nop -c iex([io.file]::ReadAllText($env:0)) & exit /b
#sp 'HKCU:\Volatile Environment' 'trevina_jamon' @'

Clear-Host

function Give-SizeString {
    <#
        .SYNOPSIS
        Converts Bytes to KB, MB, etc. strings.

        .DESCRIPTION
        Takes an integer value (usually bytes) and returns the original number transformed into the proper unit along with the tag (B, KB, MB, ...).

        .PARAMETER RealSize
        The original value in bytes.

        .PARAMETER Round
        The number to round to. Default is 2 for decimal points.

        .PARAMETER Unit
        The unit at which to stop. If you want the size in MB, GB or TB, you can use this.

        .INPUTS
        RealSize can be passed to Give-SizeString using pipes.

        .EXAMPLE
        PS> 454745952256 | Give-SizeString
        ..Size Tag
          ---- ---
        423.52 GB

        .OUTPUTS
        System.Object
        The output is a PSCustomObject with the following properties:

        Size [int]
            The normalized/converted size for the unit.

        Tag [string]
            A tag for the corresponding unit (B, KB, MB, GB...).

        .EXAMPLE
        PS> Give-SizeString 454745952256
        ..Size Tag
          ---- ---
        423.52 GB

        .EXAMPLE
        PS> Give-SizeString 454745952256 -Round 0
        Size Tag
        ---- ---
         424 GB
    #>

    param (
        [Parameter(
            Mandatory=$true,
            ValueFromPipeline=$true
        )]
        [Int64] $RealSize,
        [Int32] $Round = 2,
        [string]$Unit  = ''
    )

    $sizes = @(
        "KB",
        "MB",
        "GB",
        "TB"
    )

    $sizeStr = "B"
    $index = 0
    $done = $false

    $newSize = $RealSize
    while ($index -lt $sizes.Length -and -not $done) {
        if ($Unit -eq $sizeStr) {
            $done = $true
            continue
        }

        if ($newSize -gt 1024) {
            $newSize = $newSize / 1024
            $sizeStr = $sizes[$index]
        } else {
            $done = $true
        }

        $index++
    }

    $result = [PSCustomObject]@{
        Size = [math]::Round($newSize, $Round)
        Tag  = $sizeStr
    }
    return $result
}

$pSymbol = "|"
$dSep    = "- -----"

# USE .Trim() FOR ALL VARIABLES !!!
# example: $mobo = Get-CimInstance -ClassName Win32_BaseBoard | Select-Object Manufacturer, Product | Format-List | Out-String
$mobo = Get-CimInstance -ClassName Win32_BaseBoard
$mobo_name = $mobo.Manufacturer
$mobo_prod = $mobo.Product
$secureBoot = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\SecureBoot\State" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty UEFISecureBootEnabled
$secureBootB = if ($secureBoot -eq 1) {'TRUE'} else {'FALSE'}
$secureBootColor = if ($secureBoot -eq 1) {'Green'} else {'Red'}

$pc = Get-CimInstance -ClassName Win32_ComputerSystem
$cpus = $pc.NumberOfLogicalProcessors
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu_name = $cpu.Manufacturer
$cpu_prod = ($cpu.Name).Trim()
$mem = Give-SizeString $pc.TotalPhysicalMemory -Round 0

$drives = Get-PSDrive
$drives_data = $drives | Where-Object { $_.Provider.Name -eq "FileSystem" -and $_.Name.Length -eq 1 -and $_.Free }

$iSymbol = ">"
$iSymbol2 = "< | "

$iText1 = "SYSTEM INFORMATION"
$iText2 = "/ by eltrevii :D /"
$iText3 = "Version 2026-08-24"

$iExtra1 = ""
$iExtra2 = "never is too late to try"
$iExtra3 = "gonna have to work hard"
$iExtra4 = " give everyone respect"
$iExtra5 = "  you must not surrender"
$iExtra6 = "   up you will go at the end of it all"
$iExtra7 = ""

Write-Host              "$iSymbol       ########################## $iSymbol2 $iExtra1"
Write-Host              "$iSymbol      ### $iText1 ###  $iSymbol2 $iExtra2"
Write-Host              "$iSymbol     ##########################   $iSymbol2 $iExtra3"
Write-Host              "$iSymbol    ### $iText2 ###    $iSymbol2 $iExtra4"
Write-Host              "$iSymbol   ##########################     $iSymbol2 $iExtra5"
Write-Host              "$iSymbol  ### $iText3 ###      $iSymbol2 $iExtra6"
Write-Host              "$iSymbol ##########################       $iSymbol2 $iExtra7"

Write-Host              ""

Write-Host $dSep
Write-Host -NoNewLine   "$pSymbol MOBO: "
Write-Host -NoNewLine   "[$mobo_name]" -ForegroundColor red
Write-Host -NoNewLine   " "
Write-Host              "$mobo_prod" -ForegroundColor magenta
Write-Host -NoNewLine   "$pSymbol  CPU: "
Write-Host -NoNewLine   "[$cpu_name]" -ForegroundColor red
Write-Host -NoNewLine   " "
Write-Host -NoNewLine   "$cpu_prod" -ForegroundColor magenta
Write-Host -NoNewLine   " | "
Write-Host              "THR: $cpus" -ForegroundColor green
Write-Host $dSep
Write-Host -NoNewLine   "$pSymbol  SEC: "
Write-Host              "$secureBootB" -ForegroundColor $secureBootColor
Write-Host -NoNewLine   "$pSymbol  MEM: "
Write-Host              "$($mem.Size) $($mem.Tag)" -ForegroundColor yellow

Write-Host $dSep
Write-Host "$pSymbol PART:"

foreach ($i in $drives_data) {
    $dataUsed = Give-SizeString $i.Used
    $dataFree = Give-SizeString $i.Free
    Write-Host -NoNewLine "$pSymbol  * $($i.Name): "
    Write-Host -NoNewLine "USED $($dataUsed.Size) $($dataUsed.Tag) | "
    Write-Host -NoNewLine "FREE $($dataFree.Size) $($dataFree.Tag)"
    Write-Host ""
}

Write-Host $dSep
Write-Host ""

#$done = gp 'Registry::HKEY_Users\S-1-5-21*\Volatile*' trevina_jamon -ea 0; if ($done) {rp $done.PSPath trevina_jamon -force -ea 0}

# '@.replace("$@","'@").replace("@$","@'")
#'@ -force -ea 0; $code='gp ''Registry::HKEY_Users\S-1-5-21*\Volatile*'' Testing_Coder -ea 0'

pause
