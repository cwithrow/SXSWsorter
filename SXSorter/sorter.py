#
# Grab data from free/badges not required SXSW shows and sort by bands https://www.austinchronicle.com/sxsw/unofficial/
import os
import requests
import pandas
import parse_data


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


def load_data(filepath):
    # Load from file
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main():
    wdir = '/Users/candicewithrow/code/SXSorter/data'
    music_url = 'https://www.austinchronicle.com/sxsw/unofficial/'

    try:
        html_data = load_data(os.path.join(wdir,'SXSWfreeData.txt'))
    except FileNotFoundError:
        print('File not found, fetching from url')
        html_data = grab_data(music_url, os.path.join(wdir,'SXSWfreeData.txt'))

    parse_data.parseShows(html_data)


    # get into dictionary


if __name__ == '__main__':
    main()