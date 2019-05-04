from pathlib import Path

import yaml

CONFIGS_PATH = Path("../../configs/secrets.yaml")

with open(CONFIGS_PATH) as stream:
    CONFIGS = yaml.safe_load(stream)
