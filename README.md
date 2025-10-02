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

## Presets (JSON)
Los presets se validan con pydantic (schema_version=1). Ejecuta:
```
python -m app.core.preset_manager
```
para generar dos presets de ejemplo en `app/assets/presets/` y probar la carga/validación.

## Audio IO
- `load_audio(path)` carga WAV/MP3/OGG como float32 en el SR nativo y devuelve `(data[ch,n], sr, info)` usando librosa.
- `normalize_sr(data, sr, target=44100, mono='mix')` reajusta el SR con librosa y maneja canales.
- `peak_normalize(data, peak)` normaliza por pico.
- `run_ffprobe(path)` + `parse_audio_info()` obtienen metadatos del audio.
- `aac_passthrough_ok(info, target_sr, target_channels)` indica si es viable el **passthrough AAC** (MVP: requiere AAC y 44.1 kHz).

Notas:
- FFmpeg/ffprobe puede resolverse desde `app/ffmpeg/` o el PATH del sistema.
