from utils import home_dir, config_path, log_path, config, default_src_dir
from datetime import datetime
from pathlib import Path
import shutil
import json
import sys
import openpyxl

default_config = config()

if not Path.exists(config_path):
    with open("config.json", "w") as config_file:
        json.dump(default_config, config_file, indent=4)
        print("Default 'config.json' generated.")
        action = ""
        while action.lower() not in ["y", "n"]:
            action = input(f"Proceed with organizing directory '{default_src_dir}'? y/n: ")
            if action.lower() not in ["y", "n"]:
                print("Please enter 'y' or 'n'")
    if action.lower() == "n":
        while True:
            src_path = Path(input("Please enter the full source directory for sorting:\n"))
            if not Path.exists(src_path):
                print("The provided source directory doesn't exist. Please enter an existing directory.")
            else:
                break
        while True:
            target_path = home_dir
            target_dirs = input("Please enter target directories, separated by commas (e.g. Images,Videos,Documents):\n")
            confirmation = ""
            while confirmation.lower() not in ["y", "n"]:
                confirmation = input(
                    f"Entered directories will be created under {home_dir}.\n Would you like to proceed? y/n: ")
                if confirmation not in ["y", "n"]:
                    print("Please enter 'y' or 'n'")
            if confirmation.lower() == "n":
                while True:
                    target_path = Path(input("Please enter the desired full target path:\n"))
                    if not Path.exists(target_path):
                        print("Provided target path doesn't exist. Please enter an existing path.")
            for dir in target_dirs.replace(" ", ""):
                target_dir_path = Path(target_path / dir)
                target_dir_path.mkdir(exist_ok=True)
elif not Path.exists(default_config["src_dir"]):
    print(f"Directory {default_config["src_dir"]} does not exist")
    option = int(input("Would you like to:\n1. Create the directory\n2. Update src_dir\nPlease enter option number: "))
    if option == 1:
        new_dir = Path(default_config["src_dir"])
        new_dir.mkdir()
        print("Directory created")
    elif option == 2:
        new_dir = Path(input("Please enter the new directory path: "))
        with open("config.json", "w") as config_file:
            json.dump(config(new_dir), config_file, indent=4)
            print("'config.json' updated!")

with open("config.json", "r") as config_file:
    config = json.load(config_file)

if not Path.exists(log_path):
    wb = openpyxl.Workbook()
    ws = wb["Sheet"]
    ws.title = "Logs"
    header_row = ws["A1:E1"]
    log_headers = ["Source Dir", "Target Dir", "Old name", "New name", "Date sorted"]
    for i, cell in enumerate(header_row[0]):
        cell.value = log_headers[i]
    wb.save("logs.xlsx")

target_dir = Path(config["src_dir"])

log_rows = []

def log_to_doc(doc, rows):
    log_wb = openpyxl.load_workbook(doc)
    log_ws = log_wb["Logs"]

    for row in rows:
        log_ws.append(row)
    log_wb.save("logs.xlsx")

def sort_to_dir(src_dir, sort_dir, formats):
    sort_dir_path = home_dir / sort_dir
    sort_dir_path.mkdir(exist_ok=True)
    for item in src_dir.iterdir():
        dt = datetime.fromtimestamp(item.stat().st_mtime).date()
        item_path = src_dir / item.name
        target_item_dir = sort_dir_path / f"{sort_dir.lower()}_{str(dt)}"
        item_name = item.name
        if item.is_file():
            if item.suffix.lower() in formats:
                counter = 0
                target_item_dir.mkdir(exist_ok=True)
                while Path.exists(target_item_dir / item_name):
                    counter += 1
                    item_name = item.stem + f"_{str(counter)}" + item.suffix
                log_row = [str(src_dir), str(target_item_dir), item.name, item_name if item_name != item.name else "", str(dt)]
                log_rows.append(log_row)
                try:
                    shutil.move(item_path, target_item_dir / item_name)
                except PermissionError as e:
                    print(e)

def run_script():
    try:
        print(f"Sorting '{default_src_dir}'...")
        for dir in config["target_dirs"]:
            for name, formats in dir.items():
                formats = [file_format.lower() for file_format in formats]
                sort_to_dir(target_dir, name, formats)
        if len(log_rows):
            log_to_doc("logs.xlsx", log_rows)
            print("Sorting complete!")
        else:
            print("No files to sort")
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    run_script()