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
    if auction.exists():
        users_have_request = models.UserInAuction.objects.filter(
            auction_id=auction.get().pk, status='waiting').values_list(
            'user_id', flat=True).values_list('id', flat=True)
        # user_
        data = {'auction_id': str(auction.get().pk)}
        settings.SIO.emit('liveAuctionTime', data)
        print('auction time')
