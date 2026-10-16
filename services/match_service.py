from datetime import datetime

from services.file_service import (
    load_json,
    save_json
)


class MatchService:

    FILE_NAME = "matches.json"

    @staticmethod
    def get_matches():

        return load_json(
            MatchService.FILE_NAME
        )

    @staticmethod
    def add_match(match):

        matches = load_json(
            MatchService.FILE_NAME
        )

        next_id = max(
            [
                m["id"]
                for m in matches
            ],
            default=0
        ) + 1

        match["id"] = next_id

        match["createdAt"] = str(
            datetime.now()
        )

        matches.append(match)

        save_json(
            MatchService.FILE_NAME,
            matches
        )

        return match

    @staticmethod
    def delete_match(
        match_id
    ):

        matches = load_json(
            MatchService.FILE_NAME
        )

        matches = [
            m for m in matches
            if m["id"] != match_id
        ]

        save_json(
            MatchService.FILE_NAME,
            matches
        )

    @staticmethod
    def update_match(
        match_id,
        updated_match
    ):

        matches = load_json(
            MatchService.FILE_NAME
        )

        for index, match in enumerate(matches):

            if match["id"] == match_id:

                matches[index].update(
                    updated_match
                )

                save_json(
                    MatchService.FILE_NAME,
                    matches
                )

                return True

        return False