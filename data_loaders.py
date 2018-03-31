import json


def load_from_json(filepath):
    status = False

    try:
        json_file = open(filepath, 'r')
    except FileNotFoundError as err:
        return status, str(err)

    try:
        output = json.load(json_file)
    except json.decoder.JSONDecodeError as err:
        return status, str(err)

    return True, output
