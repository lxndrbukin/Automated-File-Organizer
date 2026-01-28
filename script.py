from datetime import datetime
from pathlib import Path
import shutil
import json
import sys
from utils import home_dir, config_path, default_config, default_target_dir

if not Path.exists(config_path):
    with open("config.json", "w") as config_file:
        json.dump(default_config, config_file, indent=4)
        print("Default 'config.json' generated.")
        action = ""
        while action.lower() not in ["y", "n"]:
            action = input(f"Proceed with organizing directory '{default_target_dir}'? y/n: ")
            if action not in ["y", "n"]:
                print("Please enter 'y' or 'n'")

    if action.lower() == 'y':
        print(f"Sorting '{default_target_dir}'...")
    elif action.lower() == 'n':
        print("Configure 'config.json' to your needs and re-run the script.")
        sys.exit()

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