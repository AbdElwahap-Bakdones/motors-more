from threading import Timer
import datetime
import time
from . import models
from django.conf import settings
import jwt
from .event import USER_SID, USER_INFO
import threading
import schedule

COUNTDOWN_AUCTION = {}


def check_auction_time():
    # print('check')

    date = datetime.datetime.now()+datetime.timedelta(hours=1)
    print(datetime.datetime.now().time())

    auction = models.Auction.objects.filter(
        date__day=datetime.datetime.now().day, time__gt=datetime.datetime.now().time(), time__lt=date.time(),
        status='later auction')
    if auction.exists():
        if not auction.get().pk in COUNTDOWN_AUCTION:
            job_thread = threading.Thread(target=count_down, kwargs={
                                          'auction_id': auction.get().pk, 'auction_time': auction.get().time})
            job_thread.daemon = True
            job_thread.start()
        '''auction.get().pk'''
        users_have_request = models.UserInAuction.objects.filter(
            auction_id=auction.get().pk, status='waiting').values_list(
            'user_id', flat=True).values_list('id', flat=True)
        # user_
        data = {'auction_id': 'str(auction.get().pk)'}
        for user_id in users_have_request:
            if user_id in USER_SID:
                settings.SIO.enter_room(USER_SID[user_id], 'liveAuctionTime')
        settings.SIO.emit('liveAuctionTime', data, room='liveAuctionTime')

        print('auction time')


def count_down(*args, **kwargs):
    print('auciotm', kwargs.get('auction_time').minute)
    print('auction', kwargs.get('auction_time').second)
    x = datetime.datetime.now()
    print('x', x.minute)
    print('x', x.second)
    minute = kwargs.get('auction_time').minute-x.minute
    second = kwargs.get('auction_time').second-x.second
    seconds = (minute*60)+(second)
    print('x', seconds)
    time.sleep(10)
    # print(int(x))
    # t = Timer(5, hello_world, kwargs={'oo': 00})
    # t.start()


def hello_world(*args, **kwargs):
    print(kwargs)
    print("hello world")
    # ...
