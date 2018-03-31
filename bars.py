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
    cords = False

    while True:
        raw_input = input("Введите координаты, разделенные запятой "
                          "в формате: долгота, широта\n"
                          " например: 37.621, 55.76536 -> ")
        try:
            cords = list(map(float, raw_input.split(',')))
        except ValueError:
            print('Invalid cords input. Try again.')
            continue

        if cords:
            break

    return cords


def load_data(filepath):
    ok, res = load_from_json(filepath)

    if not ok:
        print('An error occured: ', res)
        return

    return res


def get_biggest_bar(bars_data):
    bars = bars_data.get("features")

    if not bars:
        print("there is no root object 'features'")
        return

    try:
        biggest = max(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    except KeyError:
        print('Invalid bars data')
        raise

    return biggest


def get_smallest_bar(bars_data):
    bars = bars_data.get("features")

    if not bars:
        print("there is no root object 'features'")
        return

    try:
        smallest = min(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    except KeyError:
        print('Invalid bars data')
        raise

    return smallest


def get_closest_bar(bars_data, longitude, latitude):
    bars = bars_data.get("features")

    if not bars:
        print("there is no root object 'features'")
        return
    deltas = list(min(_cords_delta(longitude, latitude, bar) for bar in bars))
    closest_bar = deltas[2]
    return closest_bar


if __name__ == '__main__':
    bars_filepath = input("Введите имя файла с информацией  "
                          "о барах или путь к нему (по-умолчанию bars.json) -> ")

    if not bars_filepath:
        bars_filepath = 'bars.json'

    bars_data = load_data(bars_filepath)

    biggest = get_biggest_bar(bars_data)
    print('Самый большой бар: {bar[properties][Attributes][Name]} '
          'с: {bar[properties][Attributes][SeatsCount]} мест'.format(bar=biggest))

    smallest = get_smallest_bar(bars_data)
    print('Наименьший бар: {bar[properties][Attributes][Name]} '
          'с: {bar[properties][Attributes][SeatsCount]} мест'.format(bar=smallest))

    user_longitude, user_latitude = _input_user_cords()
    closest = get_closest_bar(bars_data, user_longitude, user_latitude)
    print('Ближайший бар: {bar[properties][Attributes][Name]} '
          'с долготой: {bar[geometry][coordinates][0]} '
          'и широтой: {bar[geometry][coordinates][1]}'.format(bar=closest))
