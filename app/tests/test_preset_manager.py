from pathlib import Path
from app.core.preset_manager import PresetManager, Preset, SCHEMA_VERSION
import json

def test_example_presets(tmp_path: Path):
    pm = PresetManager(presets_dir=tmp_path / "assets" / "presets")
    pm.ensure_example_presets()
    files = list((tmp_path / "assets" / "presets").glob("*.json"))
    assert len(files) >= 2

def test_validate_and_roundtrip(tmp_path: Path):
    pm = PresetManager(presets_dir=tmp_path / "assets" / "presets")
    pm.ensure_example_presets()
    src = pm.get_builtin("minimal_ring") or pm.list_builtin()[0]
    preset = pm.load(src)
    assert preset.schema_version == SCHEMA_VERSION
    out = tmp_path / "out.json"
    pm.save(preset, out)
    loaded = pm.load(out)
    assert loaded.output.fps in (24,25,30,50,60)

def test_migrate_future_version_raises(tmp_path: Path):
    pm = PresetManager(presets_dir=tmp_path / "assets" / "presets")
    data = {"schema_version": 999, "meta": {}, "output": {"resolution":{"width":1,"height":1}}, "background":{}, "visual":{}, "center_image":{}, "audio":{}}
    try:
        pm.validate_dict(data)
        assert False, "Should have raised"
    except ValueError:
        assert True
