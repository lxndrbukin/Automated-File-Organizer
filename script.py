from datetime import datetime
from pathlib import Path
import shutil
import json

home_dir = Path.home()

with open("config.json", "r") as config_file:
    config = json.load(config_file)

target_dir = Path(config["target_dir"])

def sort_to_dir(src_dir, sort_dir, formats):
    sort_dir_path = home_dir / sort_dir
    sort_dir_path.mkdir(exist_ok=True)
    for item in src_dir.iterdir():
        dt = datetime.fromtimestamp(item.stat().st_mtime).date()
        item_path = src_dir / item.name
        target_item_path = sort_dir_path / f"{sort_dir.lower()}_{str(dt)}"
        if item.is_file():
            if item.suffix in formats:
                target_item_path.mkdir(exist_ok=True)
                shutil.move(item_path, target_item_path / item.name)

def run_script():
    try:
        for dir in config["sort_dirs"]:
            for name, formats in dir.items():
                sort_to_dir(target_dir, name, formats)
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    run_script()