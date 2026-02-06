from pathlib import Path
import json

home_dir = Path.home()
default_src_dir = home_dir / "Downloads"
config_path = Path("config.json")
log_path = Path("logs.xlsx")

default_target_dirs = [
                {"Images": {"formats": [".jpg",".png",".jpeg",".gif",".webp"], "sub_dirs": True, "recursive": False}},
                {"Documents": {"formats":[".xlsx",".doc",".pdf",".md",".markdown",".csv",".docx",".txt"], "sub_dirs": True, "recursive": False }},
                {"Videos": {"formats": [".mp4",".mov",".avi"], "sub_dirs": True, "recursive": False}},
                {"Software": {"formats": [".iso",".AppImage",".rpm"], "sub_dirs": True, "recursive": False}}
            ]

def config(src_dir=default_src_dir, target_path=home_dir, target_dirs=default_target_dirs):
    return {
            "src_dir": str(src_dir),
            "target_dirs_config": {
                "target_path": str(target_path),
                "target_dirs": target_dirs
            }
        }