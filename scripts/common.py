from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(relative_path):
    path = ROOT / relative_path
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def dump_yaml(relative_path, data):
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=100)

def load_json(relative_path, default=None):
    import json
    path = ROOT / relative_path
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def dump_json(relative_path, data):
    import json
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
