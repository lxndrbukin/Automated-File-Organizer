from utils import home_dir
from datetime import datetime
from pathlib import Path
import shutil

def sort_to_dir(src_dir, sort_dir, formats, use_sub_dirs, recursive, log_rows):
    sort_dir_path = home_dir / sort_dir
    sort_dir_path.mkdir(exist_ok=True)
    if recursive:
        files_to_process = src_dir.rglob("*")
    else:
        files_to_process = src_dir.iterdir()
    for file in files_to_process:
        file_date = datetime.fromtimestamp(file.stat().st_mtime).date()
        if use_sub_dirs:
            target_dir_path = sort_dir_path / f"{sort_dir.lower()}_{str(file_date)}"
        else:
            target_dir_path = sort_dir_path
        file_name = file.name
        if file.is_file():
            if file.suffix.lower() in formats:
                counter = 0
                target_dir_path.mkdir(exist_ok=True)
                while Path.exists(target_dir_path / file_name):
                    counter += 1
                    file_name = file.stem + f"_{str(counter)}" + file.suffix
                log_row = [file.name, file_name if file_name != file.name else "-", str(target_dir_path)]
                log_rows.append(log_row)
                try:
                    shutil.move(file, target_dir_path / file_name)
                except PermissionError as e:
                    print(e)