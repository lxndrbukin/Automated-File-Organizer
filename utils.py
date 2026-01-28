from pathlib import Path

home_dir = Path.home()
default_target_dir = home_dir / "Downloads"
config_path = Path("config.json")

default_config = {
            "target_dir": f"{default_target_dir}",
            "sort_dirs": [
                {"Images": [".jpg",".png",".jpeg",".gif",".webp"]},
                {"Documents": [".xlsx",".doc",".pdf",".md",".markdown",".csv",".docx",".txt"]},
                {"Videos": [".mp4",".mov",".avi"]},
                {"Software": [".iso",".AppImage",".rpm"]}
            ]
        }