# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs


kucinema_trap = 'http://www.kucinetrap.kr/'
kucinema_theque = 'http://www.kucine.kr/'
schedule_postfix = 'async/weeklyschedule.php'

def parse(url):
    params = {
        'date': '20140831'
    }
    r = requests.post(url + schedule_postfix, params=params)

    print r.text

parse(kucinema_trap)
#parse(kucinema_theque)
