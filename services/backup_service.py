import os
import shutil

from datetime import datetime


class BackupService:

    @staticmethod
    def create_backup():

        # Create backup folder

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_folder = os.path.join(
            "backups",
            f"backup_{timestamp}"
        )

        shutil.copytree(
            "data",
            backup_folder
        )

        # Keep only latest 5 backups

        MAX_BACKUPS = 5

        if os.path.exists(
            "backups"
        ):

            backups = sorted(
                os.listdir(
                    "backups"
                )
            )

            while len(backups) > MAX_BACKUPS:

                oldest_backup = backups[0]

                shutil.rmtree(
                    os.path.join(
                        "backups",
                        oldest_backup
                    )
                )

                backups.pop(0)

        return backup_folder

    @staticmethod
    def get_backups():

        if not os.path.exists(
            "backups"
        ):
            return []

        return sorted(
            os.listdir(
                "backups"
            ),
            reverse=True
        )

    @staticmethod
    def restore_backup(
        backup_name
    ):

        source = os.path.join(
            "backups",
            backup_name
        )

        if not os.path.exists(
            source
        ):
            return False

        if os.path.exists(
            "data"
        ):

            shutil.rmtree(
                "data"
            )

        shutil.copytree(
            source,
            "data"
        )

        return True