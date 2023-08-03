import datetime
import time
from . import models
from django.conf import settings
import jwt
from .event import USER_SID, USER_INFO


def check_auction_time():
    # print('check')

    date = datetime.datetime.now()+datetime.timedelta(hours=1)
    print(datetime.datetime.now().time())

    auction = models.Auction.objects.filter(
        date__day=datetime.datetime.now().day, time__gt=datetime.datetime.now().time(), time__lt=date.time(),
        status='later auction')
    if True or auction.exists():
        '''auction.get().pk'''
        users_have_request = models.UserInAuction.objects.filter(
            auction_id=4, status='waiting').values_list(
            'user_id', flat=True).values_list('id', flat=True)
        # user_
        print(users_have_request)
        data = {'auction_id': 'str(auction.get().pk)'}
        for user_id in users_have_request:
            if user_id in USER_SID:
                settings.SIO.enter_room(USER_SID[user_id], 'liveAuctionTime')
        settings.SIO.emit('liveAuctionTime', data, room='liveAuctionTime')

        print('auction time')
