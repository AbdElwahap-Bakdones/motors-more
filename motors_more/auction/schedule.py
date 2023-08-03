from threading import Timer
import datetime
import time
from . import models
from django.conf import settings
import jwt
from .event import USER_SID, USER_INFO, OUTBID_DATA, AUCTION_INFO
import threading
import schedule

COUNTDOWN_AUCTION = {}


def check_auction_time():
    # print('check')

    date = datetime.datetime.now()+datetime.timedelta(hours=1)
    # print(datetime.datetime.now().time())

    auction = models.Auction.objects.filter(status='later auction')
    # date__day=datetime.datetime.now().day, time__gt=datetime.datetime.now().time(), time__lt=date.time(),
    # )
    if auction.exists():
        if not auction.get().pk in COUNTDOWN_AUCTION:
            COUNTDOWN_AUCTION[auction.get().pk] = True
            job_thread = threading.Thread(target=count_down, kwargs={
                                          'auction_id': auction.get().pk, 'auction_time': auction.get().time})
            job_thread.daemon = True
            job_thread.start()

        users_have_request = models.UserInAuction.objects.filter(
            auction_id=auction.get().pk, status='waiting').values_list(
            'user_id', flat=True).values_list('user_id', flat=True)
        data = {'auction_id': str(auction.get().pk)}
        for user_id in users_have_request:
            if user_id in USER_SID:
                settings.SIO.enter_room(USER_SID[user_id], 'liveAuctionTime')
        settings.SIO.emit('liveAuctionTime', data, room='liveAuctionTime')
        print('auction time')


def count_down(*args, **kwargs):
    x = datetime.datetime.now()
    minute = kwargs.get('auction_time').minute-x.minute
    second = kwargs.get('auction_time').second-x.second
    seconds = (minute*60)+(second)
    print('x', seconds)
    task = Timer(15, start_auction, kwargs={'auction_id': kwargs['auction_id']})
    task.start()


def start_auction(*args, **kwargs):
    del COUNTDOWN_AUCTION[kwargs['auction_id']]
    models.Auction.objects.filter(pk=kwargs['auction_id']).update(status='live auction')
    car = models.CarInAuction.objects.filter(auction_id=kwargs['auction_id']).order_by('car_id')
    print(car)
    OUTBID_DATA[kwargs['auction_id']] = {'auction_id': kwargs['auction_id'],
                                         'car_bids_on_it': {}, 'price': car.first().car_id.price, 'counter': 0}
    count = 0
    while count < 30:
        count += 1
        OUTBID_DATA[kwargs['auction_id']]['counter'] = count
        settings.SIO.emit('start_auction', OUTBID_DATA[kwargs['auction_id']], room=kwargs['auction_id'])
        # print(kwargs)
        print("hello world")
        print(OUTBID_DATA[kwargs['auction_id']])
        time.sleep(1)


def auction_starting(*args, **kwargs):
    AUCTION_INFO[kwargs['']]
