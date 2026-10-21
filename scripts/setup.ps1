# Mise en place complète du poste pour le TP1 (Windows PowerShell).
# Usage : powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "1/4 Vérification de Python"
py --version

Write-Host "2/4 Création de l'environnement virtuel"
if (-not (Test-Path ".venv\Scripts\python.exe")) {
	if (Test-Path ".venv") { Remove-Item -Recurse -Force ".venv" }
	py -m venv .venv
}
$VenvPython = Join-Path $PWD ".venv\Scripts\python.exe"

Write-Host "3/4 Installation des dépendances"
& $VenvPython -m pip install pandas scikit-learn pytest

Write-Host "4/4 Diagnostic"
& $VenvPython scripts\check_setup.py
