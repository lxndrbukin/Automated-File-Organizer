from utils import default_src_dir, home_dir
from pathlib import Path
import json

default_target_dirs = [
                {"Images": {"formats": [".jpg",".png",".jpeg",".gif",".webp"], "sub_dirs": True, "recursive": False}},
                {"Documents": {"formats":[".xlsx",".doc",".pdf",".md",".markdown",".csv",".docx",".txt"], "sub_dirs": True, "recursive": False }},
                {"Videos": {"formats": [".mp4",".mov",".avi"], "sub_dirs": True, "recursive": False}},
                {"Software": {"formats": [".iso",".AppImage",".rpm"], "sub_dirs": True, "recursive": False}}
            ]

def create_config(src_dir=default_src_dir, target_path=home_dir, target_dirs=default_target_dirs):
    return {
            "src_dir": str(src_dir),
            "target_dirs_config": {
                "target_path": str(target_path),
                "target_dirs": target_dirs
            }
        }

def load_config():
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)
    return config_data

def validate_config(config):
    if not Path.exists(Path(config["src_dir"])):
        print(f"Directory {config["src_dir"]} does not exist")
        option = ""
        while option not in ["1", "2"]:
            option = input("Would you like to:\n1. Create the directory\n2. Update src_dir\nPlease enter option number: ")
            if option not in ["1", "2"]:
                print("Please enter 1 or 2")
        if option == "1":
            new_dir = Path(config["src_dir"])
            new_dir.mkdir()
            print("Directory created")
        elif option == "2":
            new_dir = Path(input("Please enter the new directory path: "))
            with open("config.json", "w") as config_file:
                json.dump(create_config(new_dir), config_file, indent=4)
                print("'config.json' updated!")