# NCS Visualizer (MVP)
Proyecto Python 3.11 (Windows 11) para generar videos estilo “visualizer NCS” con GUI (PySide6).

## Instalación rápida
```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pip-tools
pip-compile --resolver=backtracking --upgrade --generate-hashes -o requirements.txt requirements.in
pip-sync requirements.txt
.\scripts\run.ps1
```
