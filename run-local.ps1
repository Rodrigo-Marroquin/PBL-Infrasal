# Plan B sin Docker: carga .env y levanta la API en el puerto 8000.
# Uso: .\run-local.ps1   (requiere: pip install -r requirements.txt)
param([string]$Python = "python")
Get-Content "$PSScriptRoot\.env" | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object {
    $k, $v = $_ -split '=', 2
    Set-Item -Path "env:$($k.Trim())" -Value $v.Trim()
}
Set-Location $PSScriptRoot
& $Python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
