import shutil
from datetime import datetime

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

backup_folder = (
    f"backups/backup_{timestamp}"
)

shutil.copytree(
    "data",
    backup_folder
)

print(
    f"Backup created: {backup_folder}"
)