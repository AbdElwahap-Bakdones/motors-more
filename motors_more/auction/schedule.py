import datetime
import time
from .models import Auction


def print_something():
    print('start')
    date = datetime.datetime.now()+datetime.timedelta(minutes=10)
    # print(date.time())
    print(Auction.objects.all().values_list('date__day', flat=True)[0])
    # if Auction.objects.all().values_list('time', flat=True)[0] < date.time():
    #     print('>>>>>>>>>>>')
    print(datetime.datetime.now().day)
    if Auction.objects.filter(
            date__day=datetime.datetime.now().day, time__lt=date.time(),
            status='later auction').exists():
        print('auction time')
    # settings.SIO.emit('liveAuctionTime')
