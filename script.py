from utils import config_path, log_path, default_src_dir
from wizard import create_config_wizard
from config import create_config, load_config, validate_config
from logger import initialize_log, log_to_doc
from file_organizer import sort_to_dir
from pathlib import Path
from tabulate import tabulate
import argparse

default_config = create_config()

if not Path.exists(config_path):
    create_config_wizard()

config = load_config()
validate_config(config)

initialize_log(log_path)

src_dir = Path(config["src_dir"])

log_rows = []

def run_script(dry_run=False):
    try:
        if dry_run:
            print("Dry-run mode: No files will be moved.")
        print(f"Sorting '{src_dir}'...\n" if not dry_run else f"Checking '{src_dir}'...\n")
        for category_config in config["target_dirs_config"]["target_dirs"]:
            for name, formats in category_config.items():
                formats_list = ["." + fmt if not fmt.startswith(".") else fmt for fmt in formats["formats"]]
                sort_to_dir(src_dir, name, formats_list, formats["sub_dirs"], formats["recursive"], log_rows, dry_run)
        if len(log_rows):
            log_to_doc("logs.xlsx", log_rows)
            print(f"{'Sorting' if not dry_run else 'Check'} complete! {len(log_rows)} file(s) {'organized' if not dry_run else 'available'}.\n")
            display_rows = [[row[0], row[1] or "-", Path(row[2]).parts[-1]]
                            for row in log_rows]
            print(tabulate(display_rows, headers=["File", "Renamed To", "Destination Folder"]))
        else:
            print("No files to sort" if not dry_run else "No files to check")
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart file organizer")
    parser.add_argument("--src", type=str, help="Source directory (overrides config)")
    parser.add_argument("--dry-run", action="store_true", help="Log without moving files")
    args = parser.parse_args()
    if args.src:
        src_dir = Path(args.src)
    run_script(dry_run=args.dry_run)