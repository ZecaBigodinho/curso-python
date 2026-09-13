# ============================================================
# CourseForge Watcher -- Instalador de Tarefa Agendada (Windows)
# ============================================================

param(
    [switch]$StartNow,
    [switch]$NonInteractive
)

$ErrorActionPreference = "Stop"

# -- Configuracao ----------------------------------------------
$TaskName = "CourseForge Watcher"
$TaskDescription = "Monitora a fila de jobs do CourseForge Hermes e executa geracao de conteudo automaticamente."
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$WatcherScript = Join-Path $ProjectRoot "courseforge_watcher.py"

# Detectar pythonw.exe (sem janela de console)
$PythonW = (Get-Command pythonw -ErrorAction SilentlyContinue).Source
if (-not $PythonW) {
    $Python = (Get-Command python -ErrorAction SilentlyContinue).Source
    if (-not $Python) {
        Write-Error "Python nao encontrado no PATH. Instale Python 3.10+ primeiro."
        exit 1
    }
    $PythonW = $Python -replace "python\.exe$", "pythonw.exe"
    if (-not (Test-Path $PythonW)) {
        Write-Warning "pythonw.exe nao encontrado. Usando python.exe."
        $PythonW = $Python
    }
}

# Verificar se o script existe
if (-not (Test-Path $WatcherScript)) {
    Write-Error "Script do watcher nao encontrado: $WatcherScript"
    exit 1
}

Write-Host ""
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  CourseForge Watcher -- Instalador" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Python:    $PythonW" -ForegroundColor Gray
Write-Host "  Script:    $WatcherScript" -ForegroundColor Gray
Write-Host "  Tarefa:    $TaskName" -ForegroundColor Gray
Write-Host ""

# -- Remover tarefa existente (se houver) ----------------------
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "[INFO] Removendo tarefa existente..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# -- Criar a tarefa --------------------------------------------
$Action = New-ScheduledTaskAction `
    -Execute $PythonW `
    -Argument "`"$WatcherScript`"" `
    -WorkingDirectory $ProjectRoot

$Trigger = New-ScheduledTaskTrigger -AtLogOn

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartInterval (New-TimeSpan -Minutes 5) `
    -RestartCount 3 `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0)

$Principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Description $TaskDescription `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    | Out-Null

Write-Host ""
Write-Host "[OK] Tarefa '$TaskName' criada com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "  A tarefa sera iniciada automaticamente ao fazer logon." -ForegroundColor Gray
Write-Host "  Para iniciar agora:   Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
Write-Host "  Para verificar:       Get-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
Write-Host "  Para remover:         Unregister-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
Write-Host ""

# -- Iniciar tarefa --------------------------------------------
if ($StartNow) {
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "[OK] Watcher iniciado!" -ForegroundColor Green
} elseif (-not $NonInteractive) {
    $iniciar = Read-Host "Deseja iniciar o watcher agora? (s/N)"
    if ($iniciar -match "^[sS]") {
        Start-ScheduledTask -TaskName $TaskName
        Write-Host "[OK] Watcher iniciado!" -ForegroundColor Green
    } else {
        Write-Host "[INFO] O watcher iniciara no proximo logon." -ForegroundColor Yellow
    }
} else {
    Write-Host "[INFO] O watcher iniciara no proximo logon." -ForegroundColor Yellow
}
