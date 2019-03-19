'''
Parse soup data into dictionary
'''
import bs4
from bs4 import BeautifulSoup
import datetime
import string



def addRecord(day,curr_day, records_list ):
    record = {}




def fixDate(dom):
    return datetime.strptime('03-' + dom + '-2019', '%m-%d-%Y')


def addDay(day):
    date = day.string.strip().split()[2]
    date = fixDate(date)
    return date


def get_club(location):
    name = None
    addr = None
    time = 0
    loc_list = location.split(',')
    exc_list = ['space 24 twenty']

    if loc_list[0].translate(str.maketrans('', '', string.punctuation)).replace(' ', '').isalpha()\
                or loc_list[0].lower in exc_list:
        name = loc_list[0]

    if len(loc_list) > 1:
        if 'pm' in loc_list[-1].lower():
            time = loc_list[-1].strip()
            if name:
                addr = ''.join(loc_list[1:-1])
            else:
                addr = loc_list[0:-1]
        else:
            if name:
                addr = loc_list[1:]
            else:
                addr = loc_list[0:]
    elif len(loc_list) == 1 and name is None:
        addr = loc_list[0]

    return name, addr, time


def get_performers(perf_str):
    perf_str = perf_str.lower().replace('&amp;', '&')

    if ';' in perf_str:
        perf_list = perf_str.split(';')
    else:
        perf_list = perf_str.split(',')

    if 'w/' in perf_list[0]:
        show_name, perf_list[0] = perf_list[0].split('w/')
    else:
        show_name = None
    performers = []
    for p in perf_list:
        plist = p.split()
        if ':' in plist[-1]:
            p_time = plist[-1].lstrip('(').rstrip(')')
            p_name = ' '.join(plist[0:-1]).title().strip()
        else:
            p_time = None
            p_name = p.title().strip()
        performers.append((p_name, p_time))

    return show_name.title().strip(), performers


def parseShows(html_data):
    soup = BeautifulSoup(html_data, "html.parser")

    # Begin SXSW content
    shows = soup.find(id='SXSW')


    # save_data(os.path.join(wdir,'free_shows.txt'), show_data)

    #  find date tags

    show_list = []

    for div in shows.findAll('div', attrs={'class': 'unofficial-date'}):
        day = div.string.strip()
        print(day)
        club = div.find_next('h2', attrs={'class': 'clubs'})
        while club:

            try:
                if type(club.next) != bs4.element.NavigableString:
                    # if link, store it
                    loc_link = ''.join(['https://www.austinchronicle.com', club.next['href']])
                else:
                    loc_link = None

                club_name, location, show_time = get_club(club.text.split('\xa0')[0].strip())
            except AttributeError:
                print('Location error')

            try:
                info = club.find_next('a', attrs={'class': "unofficial-tickets"})
            except AttributeError:
                print('ticket error')

            else:
                if info:
                    ticket_info = info.text
                    ticket_link = info['href']
                else:
                    ticket_info = 'No tickets'
                    ticket_link = None
                    # print(ticket_info, ticket_link)

            try:
                perf = club.find_next('div', attrs={'class': 'performers'})
            except AttributeError:
                print('No more performers')
            else:
                show_name, performers = get_performers(perf.text)
                for p in performers:
                    show = {'date': day, 'club': club_name, 'location': location, 'location_link': loc_link,
                            'show_time': show_time, 'ticket_info': ticket_info, 'ticket_link': ticket_link,
                            'show_name': show_name, 'perf_name': p[0], 'perf_time': p[1]}
                    print(show)
                    show_list.append(show)
            try:
                club = club.find_next('h2', attrs={'class': 'clubs'})

            except AttributeError:
                print('No more clubs')

        return show_list


            # for artist in
            # addRecord(str_date, curr_day, shows_list)

        #     if day.string == curr_day:
        #
        # else:
        #     curr_day = day.string
        #     print(

        # if day.next.attrs['class'][0] == 'unofficial-date':
        #     print(True)
        # else:
        #     print(False)


# create


