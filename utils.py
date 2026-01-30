from pathlib import Path

home_dir = Path.home()
default_target_dir = home_dir / "Downloads"
config_path = Path("config.json")
log_path = Path("logs.xlsx")

default_config = {
            "src_dir": f"{default_target_dir}",
            "target_dirs": [
                {"Images": [".jpg",".png",".jpeg",".gif",".webp"]},
                {"Documents": [".xlsx",".doc",".pdf",".md",".markdown",".csv",".docx",".txt"]},
                {"Videos": [".mp4",".mov",".avi"]},
                {"Software": [".iso",".AppImage",".rpm"]}
            ]
        }