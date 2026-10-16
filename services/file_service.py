import json
import os

DATA_FOLDER = "data"


def load_json(filename):

    file_path = os.path.join(
        DATA_FOLDER,
        filename
    )

    if not os.path.exists(file_path):
        return []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_json(filename, data):

    file_path = os.path.join(
        DATA_FOLDER,
        filename
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )