import os
import shutil
import zipfile
import tempfile

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
    def create_backup_zip():

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        zip_filename = (
            f"backup_{timestamp}.zip"
        )

        temp_zip = os.path.join(
            tempfile.gettempdir(),
            zip_filename
        )

        with zipfile.ZipFile(
            temp_zip,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zipf:

            for root, dirs, files in os.walk(
                "data"
            ):

                for file in files:

                    file_path = os.path.join(
                        root,
                        file
                    )

                    arcname = os.path.relpath(
                        file_path,
                        "data"
                    )

                    zipf.write(
                        file_path,
                        arcname
                    )

        return temp_zip

    @staticmethod
    def restore_zip_backup(
        uploaded_file
    ):

        temp_dir = tempfile.mkdtemp()

        zip_path = os.path.join(
            temp_dir,
            uploaded_file.name
        )

        with open(
            zip_path,
            "wb"
        ) as file:

            file.write(
                uploaded_file.getbuffer()
            )

        extract_dir = os.path.join(
            temp_dir,
            "restore"
        )

        os.makedirs(
            extract_dir,
            exist_ok=True
        )

        with zipfile.ZipFile(
            zip_path,
            "r"
        ) as zip_ref:

            zip_ref.extractall(
                extract_dir
            )

        if os.path.exists(
            "data"
        ):

            shutil.rmtree(
                "data"
            )

        shutil.copytree(
            extract_dir,
            "data"
        )

        return True

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