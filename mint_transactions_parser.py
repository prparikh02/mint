#!/usr/bin/env python
import argparse
import csv
import json


def init_argparser():
    parser = argparse.ArgumentParser()
    parser.description = ('Convert csv file with header to JSON format.')

    parser.add_argument(
        '-i',
        '--input',
        help='input CSV file from Mint',
        dest='input_file',
        default='./transactions.csv',
    )
    parser.add_argument(
        '-o',
        '--output',
        help='output destination of JSON',
        dest='output_file',
        default='./transactions.json',
    )

    return parser.parse_args()


def parse_records(in_file, **csv_reader_kwargs):
    with open(in_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, **csv_reader_kwargs)
        keys = next(csv_reader)
        for line in csv_reader:
            yield dict(zip(keys, line))


def write_to_json(in_file, out_file, **csv_reader_kwargs):
    if not out_file.endswith('.json'):
        out_file += '.json'

    converter = parse_records(in_file, **csv_reader_kwargs)

    with open(out_file, 'w') as json_file:
        json_file.write('[')  # write opening brace
        # write first record
        json_file.write(json.dumps(next(converter), indent=4))
        # write rest of the records
        for record in converter:
            json_file.write(',\n')  # append comma
            json_file.write(json.dumps(record, indent=4))
        # write closing brace
        json_file.write(']')


if __name__ == '__main__':
    args = init_argparser()

    write_to_json(
        args.input_file,
        args.output_file,
        delimiter=',',
        quotechar='"'
    )
