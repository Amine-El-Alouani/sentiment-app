# Mise en place complète du poste pour le TP1 (Windows PowerShell).
# Usage : powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "1/4 Vérification de Python"
py -3.11 --version

Write-Host "2/4 Création de l'environnement virtuel"
if (-not (Test-Path ".venv")) { py -3.11 -m venv .venv }
& .\.venv\Scripts\Activate.ps1

Write-Host "3/4 Installation des dépendances"
python -m pip install --upgrade pip
pip install -r requirements.txt
pip freeze | Out-File -Encoding utf8 requirements.lock

Write-Host "4/4 Diagnostic"
python scripts\check_setup.py
