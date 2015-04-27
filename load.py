# -*- coding: utf-8 -*-
import os
import re
import datetime
import requests
from bs4 import BeautifulSoup as bs
import django
import arrow

os.environ['DJANGO_SETTINGS_MODULE'] = 'kucinema.settings'
django.setup()

from kucinema.models import Movie, Schedule 

kucinema_trap = 'http://www.kucinetrap.kr/'
kucinema_theque = 'http://www.kucine.kr/'
schedule_postfix = 'async/schedule.php'
movie_postfix = 'async/movie.php?movie=%s'

def get_info(url, mid):
    r = requests.get(url + movie_postfix % mid)
    soup = bs(r.text)
    
    info = soup.find('div', class_='fl')
    info_p = info.find('p')
    infos = info_p.text.strip().split('\n')

    intro = soup.find('div', class_='cb')
    intros = []
    for p in intro.find_all('p'):
        intros.append(p.text.strip())

    intro = '\n'.join(intros)
    return infos, intro

def parse(url, date):
    data = {
        'date': date.format('YYYYMMDD'),
    }
    r = requests.post(url + schedule_postfix, data=data)
    soup = bs(r.text)
    
    timetable = soup.find('table', id='timetable')
    if timetable is None:
        return -1

    rows = timetable.find_all('tr')
    if len(rows) == 0:
        return -1

    for row in timetable.find_all('tr'):
        col = row.find_all('td')

        time = col[1].text.strip()
        title = col[2].text.strip()
        mid = col[2].find('a')['href'].split('=')[1]
        reservation = col[5].find('a')['href']
        
        movie, created = Movie.objects.get_or_create(id=mid, title=title,
                    reservation=reservation)
        if created:
            print get_info(url, mid)

        time_start, time_end = time.split(' - ')

        time_start = map(int,time_start.split(':'))
        time_start = datetime.time(time_start[0], time_start[1])
        time_end = map(int,time_end.split(':'))
        time_end = datetime.time(time_end[0], time_end[1])

        schedule = Schedule(movie=movie, date=date.date(),
                        time_start=time_start, time_end=time_end)

        if col[2].find('img') is not None:
            schedule.early = True
        
        schedule.save()

        print schedule

today = arrow.now()
for i in range(0,15):
    day = today.replace(days=i)
    parse(kucinema_trap, day)
    #parse(kucinema_theque, day)
