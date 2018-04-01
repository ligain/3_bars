import json
import argparse


def calc_geo_cords_delta(user_longitude, user_latitude, bar):
    bar_longitude = bar['geometry']['coordinates'][0]
    bar_latitude = bar['geometry']['coordinates'][1]

    return (
        abs(user_longitude - bar_longitude),
        abs(user_latitude - bar_latitude),
        bar
    )


def input_user_cords():
    raw_input = input("Введите координаты, разделенные запятой "
                      "в формате: долгота, широта\n"
                      " например: 37.621, 55.76536 -> ")
    cords = list(map(float, raw_input.split(',')))
    return cords


def load_data(filepath):
    with open(filepath, 'r') as json_file:
        output = json.load(json_file)
    return output


def get_biggest_bar(bars_data):
    bars = bars_data.get("features")
    return max(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(bars_data):
    bars = bars_data.get("features")
    return min(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])


def get_closest_bar(bars_data, longitude, latitude):
    bars = bars_data.get("features")
    deltas = list(min(calc_geo_cords_delta(longitude, latitude, bar) for bar in bars))
    closest_bar = deltas[2]
    return closest_bar


def get_args():
    parser = argparse.ArgumentParser(
        description='Скрипт расчета информации о московских барах.')
    parser.add_argument("-f", "--filename",
                        help="Путь к файлу с информацией "
                             "о барах в формате json",
                        default='bars.json')
    parser.add_argument("--longitude",
                        help="Долгота вашего местонахождения",
                        type=float)
    parser.add_argument("--latitude",
                        help="Широта вашего местонахождения",
                        type=float)
    args = parser.parse_args()
    return args.filename, args.longitude, args.latitude


if __name__ == '__main__':
    bars_filepath, user_longitude, user_latitude = get_args()

    bars_data = load_data(bars_filepath)

    if not bars_data:
        print('Отсутствует информация о барах')
        exit()

    biggest = get_biggest_bar(bars_data)
    print('Самый большой бар: {bar[properties][Attributes][Name]} '
          'с: {bar[properties][Attributes][SeatsCount]} мест'.format(bar=biggest))

    smallest = get_smallest_bar(bars_data)
    print('Наименьший бар: {bar[properties][Attributes][Name]} '
          'с: {bar[properties][Attributes][SeatsCount]} мест'.format(bar=smallest))

    if not user_longitude or not user_latitude:
        user_longitude, user_latitude = input_user_cords()

    closest = get_closest_bar(bars_data, user_longitude, user_latitude)
    print('Ближайший бар: {bar[properties][Attributes][Name]} '
          'с долготой: {bar[geometry][coordinates][0]} '
          'и широтой: {bar[geometry][coordinates][1]}'.format(bar=closest))
