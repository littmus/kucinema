# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup as bs

from models import Movie, Schedule 

kucinema_trap = 'http://www.kucinetrap.kr/'
kucinema_theque = 'http://www.kucine.kr/'
schedule_postfix = 'async/weeklyschedule.php'
movie_postfix = 'async/movie.php?movie=%d'
#RE_MOVIE = re.compile('\$\("#day(?P<day>[\d]+)"\).append\(\'(?P<tag>.*)\'\);', re.UNICODE)
RE_MOVIE = re.compile('\$\("#day(?P<day>\d+)"\).append\(\'<div class="schMovie"><a href="../async/movie.php\?movie\=(?P<id>\d+)" onclick="return popupLayer\(this.href\)">(?P<title>.*)<br />(?P<time>[\d:~]+)</a></div>\'\);', re.UNICODE)


def parse(url):
    params = {
        'date': '20140905'
    }
    r = requests.post(url + schedule_postfix, params=params)

    soup = bs(r.text)
    script = soup('script')[0]

    list_movie = [m.groupdict() for m in RE_MOVIE.finditer(script.text)]
    for m in list_movie:
        print m['day'], m['title'], m['time'], m['id']
        movie = Movie(movie_id=m['id'], title=m['title'])
#        movie.save()

        time_start, time_end = m['time'].split('~')

        print m['title'], time_start, time_end
#        schedule = Schedule(movie=movie, time_start \ 

def movie_list():
    pass
