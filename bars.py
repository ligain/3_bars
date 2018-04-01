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


def load_data(filepath):
    with open(filepath, 'r') as json_file:
        decoded_data = json.load(json_file)
    return decoded_data


def get_biggest_bar(bars):
    return max(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(bars):
    return min(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])


def get_closest_bar(bars, longitude, latitude):
    # generate and sort a list of tuples with coordinates differences like:
    # [(0.45, 0.5656, {...}), (0.0012, 0.322, {...}), (0.985, 0.124554, {...}), ...]
    deltas = list(min(calc_geo_cords_delta(longitude, latitude, bar) for bar in bars))
    closest_bar = deltas[2]
    return closest_bar


def get_args():
    parser = argparse.ArgumentParser(
        description='Скрипт расчета информации о московских барах.')
    parser.add_argument('-f', '--filepath',
                        help='Путь к файлу с информацией '
                             'о барах в формате json',
                        default='bars.json')
    parser.add_argument('--longitude',
                        help='Долгота вашего местонахождения',
                        type=float,
                        required=True)
    parser.add_argument('--latitude',
                        help='Широта вашего местонахождения',
                        type=float,
                        required=True)
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
