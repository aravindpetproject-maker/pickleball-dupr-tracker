from services.file_service import (
    load_json
)


class AuthService:

    FILE_NAME = "users.json"

    @staticmethod
    def login(

        username,

        password

    ):

        users = load_json(
            AuthService.FILE_NAME
        )

        for user in users:

            if (

                user["username"]
                ==
                username

                and

                user["password"]
                ==
                password

            ):

                return user

        return None