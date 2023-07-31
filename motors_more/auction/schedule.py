import datetime
import time
from . import models
from django.conf import settings
import jwt
from .event import USER_SID


def check_auction_time():
    # print('check')
    date = datetime.datetime.now()+datetime.timedelta(minutes=10)
    # print(datetime.datetime.now().time())
    auction = models.Auction.objects.filter(
        date__day=datetime.datetime.now().day, time__gt=datetime.datetime.now().time(), time__lt=date.time(),
        status='later auction').values_list('pk', flat=True)
    users_have_request = models.UserInAuction.objects.filter(
        auction_id__in=auction, status='waiting').values_list(
        'user_id', flat=True)
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
    print(jwt.decode(jwt='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9', algorithms='HS256', key=settings.SECRET_KEY))
    print(users_have_request)
    if models.Auction.objects.filter(
            date__day=datetime.datetime.now().day, time__gt=datetime.datetime.now().time(), time__lt=date.time(),
            status='later auction').exists():
        settings.SIO.emit('liveAuctionTime')
        print('auction time')
