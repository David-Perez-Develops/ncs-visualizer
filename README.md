# Generador de videos estilo NCS (MVP)

Este proyecto es un generador de videos musicales inspirado en el estilo de NoCopyrightSounds. Incluye una interfaz gráfica basada en PySide6 y un motor de visualización modular que permitirá construir efectos reactivos al audio.

## Requisitos
- Python 3.11
- FFmpeg disponible en el sistema o incluido en `app/ffmpeg/` (especialmente en Windows)

## Instalación
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\pip install -r requirements.txt
# Unix/Mac
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución
```bash
python -m app.main
```

## Scripts de desarrollo
- Windows: `scripts/dev_run.bat`
- Unix/Mac: `scripts/dev_run.sh`
