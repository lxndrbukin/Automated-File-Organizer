# Automated File Organizer

A Python-based **automated file organizer** that sorts files from a source directory into categorized folders based on file type. Features an **interactive configuration wizard**, **conflict resolution with auto-renaming**, **Excel logging for audit trails**, and **flexible subdirectory organization**.

---

## Features

- **Smart File Sorting**: Automatically organizes files by type (Images, Documents, Videos, Software, etc.)
- **Interactive Configuration Wizard**: First-run setup with guided prompts for custom configurations
- **Flexible Organization**: Optional date-based subdirectories (e.g., `images_2026-02-05/`)
- **Conflict Resolution**: Automatic file renaming when duplicates exist (`vacation.jpg` → `vacation_1.jpg`)
- **Excel Logging**: Persistent audit trail of all file operations in `logs.xlsx`
- **Case-Insensitive Matching**: Handles `.jpg`, `.JPG`, `.Jpg` identically
- **Robust Validation**: Checks directory existence, handles permission errors gracefully
- **Custom Configurations**: Support for multiple config files and target directories

---

## Requirements

- Python 3.8+
- `openpyxl` library

```bash
pip install openpyxl
```

---

## Installation

1. Clone or download this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip install openpyxl
   ```

---

## Usage

### First Run - Interactive Setup

```bash
python script.py
```

On first run, you'll be prompted to create a configuration:

```
Would you like to use a default 'config.json' file? y/n: y
Default 'config.json' generated.
```

**Default Configuration:**
- **Source Directory**: `~/Downloads`
- **Target Location**: `~/` (home directory)
- **Categories**:
  - Images: `.jpg`, `.png`, `.jpeg`, `.gif`, `.webp`
  - Documents: `.xlsx`, `.doc`, `.pdf`, `.md`, `.csv`, `.txt`, etc.
  - Videos: `.mp4`, `.mov`, `.avi`
  - Software: `.iso`, `.AppImage`, `.rpm`
- **Subdirectories**: Enabled (files sorted into date-based folders)

### Custom Configuration

Choose "n" during setup to create a custom configuration:

```
Would you like to use a default 'config.json' file? y/n: n

Please enter the full source directory for sorting:
/home/user/Documents/ToSort

Please enter target directories, separated by commas (e.g. Images,Videos,Documents):
Photos,Work,Personal

Please enter desired file extensions to be saved in /home/user/Photos directory (e.g. xlsx,doc,gif):
jpg,png,raw

Would you like the files to be sorted into sub directories based on dates? (e.g. /home/user/Photos/photos_2026-02-05) y/n: y
```

### Subsequent Runs

After configuration, simply run:

```bash
python script.py
```

The script will automatically:
1. Validate source directory exists
2. Sort files into categorized folders
3. Handle naming conflicts
4. Log all operations to Excel

---

## File Structure

```
.
├── script.py          # Main organizer script
├── utils.py           # Configuration and path utilities
├── config.json        # User configuration (auto-created)
├── logs.xlsx          # Operation log (auto-created)
└── README.md
```

### Example `config.json`

```json
{
  "src_dir": "/home/user/Downloads",
  "target_dirs_config": {
    "target_path": "/home/user",
    "target_dirs": [
      {
        "Images": {
          "formats": [".jpg", ".png", ".jpeg"],
          "sub_dirs": true
        }
      },
      {
        "Documents": {
          "formats": [".pdf", ".docx", ".txt"],
          "sub_dirs": false
        }
      }
    ]
  }
}
```

### Example Organization Output

**Before:**
```
~/Downloads/
├── vacation.jpg
├── report.pdf
├── photo.PNG
├── notes.txt
└── vacation.jpg (duplicate)
```

**After (with subdirectories enabled):**
```
~/Images/
└── images_2026-02-05/
    ├── vacation.jpg
    ├── photo.png
    └── vacation_1.jpg

~/Documents/
└── documents_2026-02-05/
    ├── report.pdf
    └── notes.txt
```

---

## Excel Logging

All file operations are logged to `logs.xlsx` with the following information:

| Source Dir        | Target Dir              | Old name     | New name      | Date sorted |
|-------------------|-------------------------|--------------|---------------|-------------|
| /home/user/Downloads | /home/user/Images/images_2026-02-05 | vacation.jpg |               | 2026-02-05  |
| /home/user/Downloads | /home/user/Images/images_2026-02-05 | vacation.jpg | vacation_1.jpg | 2026-02-05  |
| /home/user/Downloads | /home/user/Documents/documents_2026-02-05 | report.pdf   |               | 2026-02-05  |

- **Old name**: Original filename
- **New name**: Only populated if file was renamed due to conflict
- **Date sorted**: File modification date (used for subdirectory organization)

---

## Configuration Options

### Source Directory (`src_dir`)
The directory to scan for files to organize.

### Target Path (`target_path`)
The base directory where organized folders will be created.

### Target Directories
Each category has:
- **formats**: List of file extensions (with or without leading dot)
- **sub_dirs**: Boolean - if `true`, creates date-based subdirectories

---

## Error Handling

The script handles common issues gracefully:

- **Missing source directory**: Prompts to create or update configuration
- **Permission errors**: Logs error and continues with remaining files
- **File conflicts**: Automatically renames duplicates with incrementing numbers
- **Invalid input**: Re-prompts with clear error messages
- **Locked Excel file**: Displays error if `logs.xlsx` is open in another program

---

## Use Cases

- **Download folder cleanup**: Automatically organize cluttered Downloads
- **Project file management**: Sort mixed project files by type
- **Photo organization**: Separate images by date
- **Document archiving**: Organize documents without date folders for cleaner structure
- **Automated workflows**: Run periodically (via cron/Task Scheduler) to maintain organization

---

## Notes

- File extensions are **case-insensitive** (`.JPG` = `.jpg`)
- Files are **moved**, not copied (original location is emptied)
- **Date-based subdirectories** use file modification time
- Conflict resolution is **automatic** - no prompts needed
- The script only processes files (ignores subdirectories in source)
- Empty runs (no matching files) won't create log entries

---

## Future Improvements

- [x] Interactive configuration wizard
- [x] Conflict resolution with auto-renaming
- [x] Excel logging for audit trails
- [x] Configurable subdirectory creation
- [ ] Dry-run mode to preview changes
- [ ] Terminal summary table with statistics (using `tabulate`)
- [ ] Undo functionality using log file
- [ ] Recursive directory processing
- [ ] File size filters and limits
- [ ] Archive old files feature
- [ ] Command-line arguments (`--dry-run`, `--config`, `--verbose`)
- [ ] Progress bar for large operations
- [ ] Exclude patterns for system files

---

## Troubleshooting

**"Directory does not exist" error:**
- Check your `config.json` file
- Ensure `src_dir` path is valid
- Choose option 1 to create directory or option 2 to update path

**Files not being sorted:**
- Verify file extensions match those in `config.json`
- Check that files are in the source directory (not subdirectories)
- Ensure you have read permissions for source files

**Excel log not updating:**
- Close `logs.xlsx` if it's open in Excel or another program
- Check write permissions for the script directory

---

## License

This project is open source and available for personal and educational use.
