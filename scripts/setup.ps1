Param()
Write-Host "Creando entorno y sincronizando dependencias..." -ForegroundColor Cyan
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pip-tools
pip-compile --resolver=backtracking --upgrade --generate-hashes -o requirements.txt requirements.in
pip-sync requirements.txt
Write-Host "Listo. Ejecuta scripts\run.ps1 para lanzar la app." -ForegroundColor Green
