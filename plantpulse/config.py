from pathlib import Path
import yaml
DEFAULT=Path(__file__).resolve().parents[1]/"configs"/"pump01.yaml"
def load_yaml(path=None):
    with open(path or DEFAULT,encoding="utf-8") as f: return yaml.safe_load(f)
