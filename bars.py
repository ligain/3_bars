import json
import argparse
from math import sin, cos, radians, acos


def calc_geo_distance(user_longitude, user_latitude, bar, earth_radius=6371.0):
    """
    Calculate distance between 2 geo coordinates
    using this algorithm https://en.wikipedia.org/wiki/Great-circle_distance
    """

    bar_longitude = radians(bar['geometry']['coordinates'][0])
    bar_latitude = radians(bar['geometry']['coordinates'][1])

    user_longitude = radians(user_longitude)
    user_latitude = radians(user_latitude)

    delta_angle = acos(
        sin(bar_latitude) * sin(user_latitude) +
        cos(bar_latitude) * cos(user_latitude) * cos(bar_longitude - user_longitude)
    )

    distance = earth_radius * delta_angle

    return (
        distance,
        bar
    )


def load_data(filepath):
    with open(filepath, 'r') as json_file:
        decoded_data = json.load(json_file)
    return decoded_data


def get_biggest_bar(bars):
    return max(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(bars):
    return min(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])


def get_closest_bar(bars, longitude, latitude):
    return min(bars, key=lambda bar: calc_geo_distance(longitude, latitude, bar))


def get_args():
    parser = argparse.ArgumentParser(
        description='Скрипт расчета информации о московских барах.'
    )
    parser.add_argument(
        '-f', '--filepath',
        help='Путь к файлу с информацией о барах в формате json',
        default='bars.json'
    )
    parser.add_argument(
        '--longitude',
        help='Долгота вашего местонахождения',
        type=float,
        required=True
    )
    parser.add_argument(
        '--latitude',
        help='Широта вашего местонахождения',
        type=float,
        required=True
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    bars_raw_data = load_data(args.filepath)

    if not bars_raw_data:
        exit('Отсутствует информация о барах')

    bars_data = bars_raw_data.get('features')

    biggest_bar = get_biggest_bar(bars_data)
    print('Самый большой бар: {bar[properties][Attributes][Name]} '
          'с: {bar[properties][Attributes][SeatsCount]} мест'.format(bar=biggest_bar))

    smallest_bar = get_smallest_bar(bars_data)
    print('Наименьший бар: {bar[properties][Attributes][Name]} '
          'с: {bar[properties][Attributes][SeatsCount]} мест'.format(bar=smallest_bar))

    closest_bar = get_closest_bar(bars_data, args.longitude, args.latitude)
    print('Ближайший бар: {bar[properties][Attributes][Name]} '
          'с долготой: {bar[geometry][coordinates][0]} '
          'и широтой: {bar[geometry][coordinates][1]}'.format(bar=closest_bar))
