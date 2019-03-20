#
# Grab data from free/badges not required SXSW shows and sort by bands https://www.austinchronicle.com/sxsw/unofficial/
import os
import requests
import json

import pandas as pd

from SXSorter import parse_data


def grab_data(url,filepath):
    # Grab data from site

    try:
        response = requests.get(url)
    except requests.ConnectionError:
        print("failed to connect")
    else:
        if response.status_code == 200:
            save_data(filepath, response.text)
            return response.text
        else:
            raise requests.ConnectionError('Connection Error: code %r' % response.status_code)


def save_data(filepath, data):
    with open(filepath, 'w') as output:
        output.write(data)
    print('Data saved to %r' % filepath)

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def load_data(filepath):
    # Load from file
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main():
    wdir = '/Users/candicewithrow/code/SXSorter/data'
    music_url = 'https://www.austinchronicle.com/sxsw/unofficial/'
    output_file  = 'SXSWfreeShows.json'

    try:
        html_data = load_data(os.path.join(wdir,'SXSWfreeData.txt'))
    except FileNotFoundError:
        print('File not found, fetching from url')
        html_data = grab_data(music_url, os.path.join(wdir,'SXSWfreeData.txt'))

    # parse html show data and return a list of records with all performers separated out
    all_performances = parse_data.parseShows(html_data)

    # save to json
    save_json(os.path.join(wdir, output_file), all_performances)

    print('Show data extracted and sorted into performers in file %r' % output_file)

    perf_df = pd.read_json(os.path.join(wdir, output_file), orient='record')
    print(perf_df[perf_df['perf_name'] == 'Calliope Musicals'])


if __name__ == '__main__':
    main()