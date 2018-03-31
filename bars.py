from data_loaders import load_from_json


def _cords_delta(user_longitude, user_latitude, bar):
    try:
        bar_longitude = bar['geometry']['coordinates'][0]
        bar_latitude = bar['geometry']['coordinates'][1]
    except KeyError:
        print('Invalid bars data')
        raise

    return (
        abs(user_longitude - bar_longitude),
        abs(user_latitude - bar_latitude),
        bar
    )


def _input_user_cords():
    result = False

    while True:
        raw_input = input("Enter geo coordinates separeted by comma "
                          "in format: longitude, latitude\n"
                          " for example: 37.621, 55.76536 -> ")
        try:
            result = list(map(float, raw_input.split(',')))
        except Exception:
            print('Invalid cords input. Try again.')
            continue

        if result:
            break

    return result


def load_data(filepath):
    ok, result = load_from_json(filepath)

    if not ok:
        print('An error occured: ', result)
        return

    return result


def get_biggest_bar(data):
    bars = data.get("features")

    if not bars:
        print("there is no root object 'features'")
        return

    try:
        result = max(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    except KeyError:
        print('Invalid bars data')
        raise

    return result


def get_smallest_bar(data):
    bars = data.get("features")

    if not bars:
        print("there is no root object 'features'")
        return

    try:
        result = min(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    except KeyError:
        print('Invalid bars data')
        raise

    return result


def get_closest_bar(data, longitude, latitude):
    bars = data.get("features")

    if not bars:
        print("there is no root object 'features'")
        return
    deltas = list(min(_cords_delta(longitude, latitude, bar) for bar in bars))
    closest_bar = deltas[2]
    return closest_bar


if __name__ == '__main__':
    bars_filepath = input("Enter file name or path to "
                          "file with bars info (default bars.json) -> ")

    if not bars_filepath:
        bars_filepath = 'bars.json'

    bars_data = load_data(bars_filepath)

    biggest = get_biggest_bar(bars_data)
    print('The biggest bar is named: {bar[properties][Attributes][Name]} '
          'with: {bar[properties][Attributes][SeatsCount]} seats'.format(bar=biggest))

    smallest = get_smallest_bar(bars_data)
    print('The smallest bar is named: {bar[properties][Attributes][Name]} '
          'with: {bar[properties][Attributes][SeatsCount]} seats'.format(bar=smallest))

    user_longitude, user_latitude = _input_user_cords()
    closest = get_closest_bar(bars_data, user_longitude, user_latitude)
    print('The closest bar is named: {bar[properties][Attributes][Name]} '
          'with longitude: {bar[geometry][coordinates][0]} '
          'and latitude: {bar[geometry][coordinates][1]}'.format(bar=closest))
