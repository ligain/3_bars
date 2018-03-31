import json
import os


def load_from_json(filepath):
    status = False

    try:
        file = open(filepath, 'r')
    except FileNotFoundError as err:
        return status, str(err)

    try:
        result = json.load(file)
    except json.decoder.JSONDecodeError as err:
        return status, str(err)

    return True, result

