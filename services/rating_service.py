from datetime import datetime

from services.file_service import (
    load_json,
    save_json
)


class RatingService:

    FILE_NAME = "ratings.json"

    @staticmethod
    def add_rating_history(record):

        ratings = load_json(
            RatingService.FILE_NAME
        )

        record["id"] = max(
            [
                r["id"]
                for r in ratings
            ],
            default=0
        ) + 1

        record["createdAt"] = str(
            datetime.now()
        )

        ratings.append(record)

        save_json(
            RatingService.FILE_NAME,
            ratings
        )

    @staticmethod
    def get_history():

        return load_json(
            RatingService.FILE_NAME
        )