from utils import home_dir, config_path
from config import create_config
from pathlib import Path
from datetime import date
import json

default_config = create_config()

def create_config_wizard():
    action = ""
    while action.lower() not in ["y", "n"]:
        action = input(f"Would you like to use a default 'config.json' file? y/n: ")
        if action.lower() not in ["y", "n"]:
            print("Please enter 'y' or 'n'")
    if action.lower() == "y":
        with open("config.json", "w") as config_file:
            json.dump(default_config, config_file, indent=4)
            print("Default 'config.json' generated.")
    if action.lower() == "n":
        while True:
            src_path = Path(input("Please enter the full source directory for sorting:\n"))
            if not Path.exists(src_path):
                print("The provided source directory doesn't exist. Please enter an existing directory.")
            else:
                break
        target_path = home_dir
        target_dirs_list = input(
            "Please enter target directories, separated by commas (e.g. Images,Videos,Documents):\n")
        confirmation = ""
        while confirmation.lower() not in ["y", "n"]:
            confirmation = input(
                f"Entered directories will be created under {home_dir}.\nWould you like to proceed? y/n: ")
            if confirmation.lower() not in ["y", "n"]:
                print("Please enter 'y' or 'n'")
            if confirmation.lower() == "n":
                while True:
                    target_path = Path(input("Please enter the desired full target path:\n"))
                    if not Path.exists(target_path):
                        print("Provided target path doesn't exist. Please enter an existing path.")
                    else:
                        break
            target_dirs = []
            for category in target_dirs_list.replace(" ", "").split(","):
                recursive_check = ""
                while recursive_check.lower() not in ["y", "n"]:
                    recursive_check = input(f"Scan subdirectories recursively when organizing {category}? y/n: ")
                    if recursive_check.lower() not in ["y", "n"]:
                        print("Please enter 'y' or 'n'")
                recursive = recursive_check.lower() == "y"
                formats = input(
                    f"Please enter desired file extensions to be saved in {target_path / category} directory (e.g. xlsx,doc,gif):\n").replace(
                    " ", "").split(",")
                sub_dir_example = Path(target_path / category / f"{category.lower()}_{date.today()}")
                sub_dirs = True
                while True:
                    sub_dir_check = input(
                        f"Would you like the files to be sorted into subdirectories based on dates? (e.g. {sub_dir_example}) y/n: ")
                    if sub_dir_check.lower() not in ["y", "n"]:
                        print("Please enter 'y' or 'n'.")
                    else:
                        break
                if sub_dir_check.lower() == "n":
                    sub_dirs = False
                target_dirs.append({f"{category}": {"formats": formats, "sub_dirs": sub_dirs, "recursive": recursive}})
            with open("config.json", "w") as config_file:
                json.dump(create_config(src_dir=src_path, target_path=target_path, target_dirs=target_dirs), config_file,
                          indent=4)
                print("'config.json' now configured")
