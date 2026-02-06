from utils import home_dir, config_path, log_path, config, default_src_dir
from datetime import datetime, date
from pathlib import Path
import shutil
import json
import openpyxl

default_config = config()

if not Path.exists(config_path):
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
        while True:
            target_path = home_dir
            target_dirs_list = input("Please enter target directories, separated by commas (e.g. Images,Videos,Documents):\n")
            confirmation = ""
            while confirmation.lower() not in ["y", "n"]:
                confirmation = input(
                    f"Entered directories will be created under {home_dir}.\n Would you like to proceed? y/n: ")
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
            for dir in target_dirs_list.replace(" ", "").split(","):
                formats = input(f"Please enter desired file extensions to be saved in {target_path / dir} directory (e.g. xlsx,doc,gif):\n").replace(" ", "").split(",")
                sub_dir_example = Path(target_path / dir / f"{dir.lower()}_{date.today()}")
                sub_dirs = True
                while True:
                    sub_dir_check = input(
                        f"Would you like the files to be sorted into sub directories based on dates? (e.g. {sub_dir_example}) y/n: ")
                    if sub_dir_check.lower() not in ["y", "n"]:
                        print("Please enter 'y' or 'n'.")
                    else:
                        break
                if sub_dir_check.lower() == "n":
                    sub_dirs = False
                target_dirs.append({f"{dir}": {"formats": formats, "sub_dirs": sub_dirs}})
            with open("config.json", "w") as config_file:
                json.dump(config(src_dir=src_path, target_path=target_path, target_dirs=target_dirs), config_file, indent=4)
                print("'config.json' now configured")

with open("config.json", "r") as config_file:
    config = json.load(config_file)

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
            json.dump(config(new_dir), config_file, indent=4)
            print("'config.json' updated!")

if not Path.exists(log_path):
    wb = openpyxl.Workbook()
    ws = wb["Sheet"]
    ws.title = "Logs"
    header_row = ws["A1:E1"]
    log_headers = ["Source Dir", "Target Dir", "Old name", "New name", "Date sorted"]
    for i, cell in enumerate(header_row[0]):
        cell.value = log_headers[i]
    wb.save("logs.xlsx")

src_dir = Path(config["src_dir"])

log_rows = []

def log_to_doc(doc, rows):
    log_wb = openpyxl.load_workbook(doc)
    log_ws = log_wb["Logs"]

    for row in rows:
        log_ws.append(row)
    log_wb.save("logs.xlsx")

def sort_to_dir(src_dir, sort_dir, formats, use_sub_dirs):
    sort_dir_path = home_dir / sort_dir
    sort_dir_path.mkdir(exist_ok=True)
    for item in src_dir.iterdir():
        dt = datetime.fromtimestamp(item.stat().st_mtime).date()
        item_path = src_dir / item.name
        if use_sub_dirs:
            target_item_dir = sort_dir_path / f"{sort_dir.lower()}_{str(dt)}"
        else:
            target_item_dir = sort_dir_path
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
                    print(f"✓ {item.name} → {target_item_dir / item_name}")
                except PermissionError as e:
                    print(e)

def run_script():
    try:
        print(f"Sorting '{default_src_dir}'...")
        for dir_config in config["target_dirs_config"]["target_dirs"]:
            for name, formats in dir_config.items():
                formats_list = ["." + fmt if not fmt.startswith(".") else fmt for fmt in formats["formats"]]
                sort_to_dir(src_dir, name, formats_list, formats["sub_dirs"])
        if len(log_rows):
            log_to_doc("logs.xlsx", log_rows)
            print("Sorting complete!")
        else:
            print("No files to sort")
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    run_script()