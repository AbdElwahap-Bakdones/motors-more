from threading import Timer
import datetime
import time
from . import models
from django.conf import settings
import jwt
from .event import USER_SID, COUNTDOWN_AUCTION, start_auction
import threading
import schedule


def check_auction_time():
    # print('check')

    try:
        date = datetime.datetime.now()+datetime.timedelta(minutes=59)
        print(datetime.datetime.now().time())

        auction = models.Auction.objects.filter(status='later auction', date__day=datetime.datetime.now(
        ).day, time__gt=datetime.datetime.now().time(), time__lt=date.time(), )
        if auction.exists():
            if not auction.get().pk in COUNTDOWN_AUCTION:
                COUNTDOWN_AUCTION[auction.get().pk] = True
                job_thread = threading.Thread(target=count_down, kwargs={
                    'auction_id': auction.get().pk, 'auction_time': auction.get().time})
                job_thread.daemon = True
                job_thread.start()
            users_have_participant = list(models.UserInAuction.objects.filter(
                auction_id=auction.get().pk, status='participant').values_list(
                'user_id', flat=True))
            data = {'auction_id': str(auction.get().pk)}
            # for user_id in users_have_request:
            #     if user_id in USER_SID:
            #         settings.SIO.enter_room(USER_SID[user_id], 'liveAuctionTime')
            for user_id in USER_SID:
                print(users_have_participant)
                print(type(users_have_participant))
                if users_have_participant.count(user_id) <= 0:
                    print(users_have_participant.count(user_id))
                    settings.SIO.enter_room(USER_SID[user_id], 'liveAuctionTime')
            settings.SIO.emit('liveAuctionTime', data, room='liveAuctionTime')
            print('auction time')
    except Exception as e:
        print('Error in check_auction_time  :', e)


def count_down(*args, **kwargs):
    x = datetime.datetime.now()
    minute = kwargs.get('auction_time').minute-x.minute
    second = kwargs.get('auction_time').second-x.second
    seconds = (minute*60)+(second)
    print('x', seconds)
    task = Timer(seconds, start_auction, kwargs={'auction_id': kwargs['auction_id']})
    task.start()
