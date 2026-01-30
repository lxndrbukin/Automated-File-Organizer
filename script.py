from utils import home_dir, config_path, log_path, default_config, default_target_dir
from datetime import datetime
from pathlib import Path
import shutil
import json
import sys
import openpyxl

if not Path.exists(config_path):
    with open("config.json", "w") as config_file:
        json.dump(default_config, config_file, indent=4)
        print("Default 'config.json' generated.")
        action = ""
        while action.lower() not in ["y", "n"]:
            action = input(f"Proceed with organizing directory '{default_target_dir}'? y/n: ")
            if action.lower() not in ["y", "n"]:
                print("Please enter 'y' or 'n'")
    if action.lower() == 'n':
        print("Configure 'config.json' to your needs and re-run the script.")
        sys.exit()

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
        print(f"Sorting '{default_target_dir}'...")
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