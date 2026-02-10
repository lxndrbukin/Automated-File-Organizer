from datetime import datetime
from pathlib import Path
import shutil

def sort_to_dir(src_dir, target_path, sort_dir, formats, use_sub_dirs, recursive, log_rows, dry_run, verbose):
    sort_dir_path = target_path / sort_dir
    sort_dir_path.mkdir(parents=True, exist_ok=True)
    if recursive:
        files_to_process = src_dir.rglob("*")
    else:
        files_to_process = src_dir.iterdir()
    files_num = 0
    for file in files_to_process:
        file_date = datetime.fromtimestamp(file.stat().st_mtime).date()
        if use_sub_dirs:
            target_dir_path = sort_dir_path / f"{sort_dir.lower()}_{str(file_date)}"
        else:
            target_dir_path = sort_dir_path
        file_name = file.name
        if file.is_file():
            if file.suffix.lower() in formats:
                files_num += 1
                counter = 0
                target_dir_path.mkdir(exist_ok=True)
                while Path.exists(target_dir_path / file_name):
                    counter += 1
                    file_name = file.stem + f"_{str(counter)}" + file.suffix
                log_row = [file.name, file_name if file_name != file.name else "-", str(target_dir_path)]
                log_rows.append(log_row)
                if not dry_run:
                    try:
                        if verbose:
                            print(f"Moving '{file.name}' → '{target_dir_path}/{file_name}'")
                        shutil.move(file, target_dir_path / file_name)
                    except PermissionError as e:
                        print(e)
                else:
                    print(f"[DRY-RUN] Would move {file} to {target_dir_path / file_name}")
        if verbose and not file.is_file():
            print(f"Skipping directory {file}")
    if verbose:
        print(f"Found {files_num} matching file(s) in '{sort_dir}' category")