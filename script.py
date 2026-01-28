
from pathlib import Path
import json

home_dir = Path.home()

with open("config.json", "r") as config_file:
    config = json.load(config_file)

target_dir = Path(config["target_dir"])

def sort_to_dir(src_dir, sort_dir, formats):
    sort_dir_path = home_dir / sort_dir
    sort_dir_path.mkdir(exist_ok=True)
    for item in src_dir.iterdir():
        print(item)

def run_script():
    try:
        for dir in config["sort_dirs"]:
            for name, formats in dir.items():
                sort_to_dir(target_dir, name, formats)
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    run_script()