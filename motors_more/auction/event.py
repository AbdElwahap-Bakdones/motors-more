from django.conf import settings
import jwt
from . import models
import time
USER_SID = {}
USER_INFO = {}
# USER_SIDS_IN_AUCTION {auction_id:{'user_count':user_count,user_id:{'sid':sid,'auction_id':auction_id,'user_id':user_id,'country':country,'province':province}}}
USER_INFO_IN_AUCTION = {int: {str: int, int: {str: int, str: int, str: int, str: str, str: str}}}
# OUTBID_DATA {auction_id:{'auction_id': 0,'car_bids_on_it': 0, 'price': 0, 'counter': 0, 'number_of_cars': 0,'car_index': 0, 'owner_car_id': 0}}
OUTBID_DATA = {int: {str: int, str: int, str: int, str: int, str: int, str: int, str: int}}
AUCTION_INFO = {}
COUNTDOWN_AUCTION = {}


@settings.SIO.event
def connect(sid, environ, auth):
    print('connect ++++++++++++++++++++++++++++++++++++++++ ', sid)
    user = jwt.decode(
        jwt=auth.get('token'),
        algorithms='HS256', key=settings.SECRET_KEY)
    # print(user.get('user_id'))
    USER_SID[user.get('user_id')] = sid
    user_info = models.User.objects.get(pk=user.get('user_id'))
    USER_INFO[sid] = {'pk': user_info.pk, 'email': user_info.email, 'user_kind': user_info.user_kind}
    has_auction = models.UserInAuction.objects.filter(user_id=user.get('user_id'), status='participant')
    print(USER_INFO_IN_AUCTION)
    for auction in USER_INFO_IN_AUCTION:
        if user_info.pk in USER_INFO_IN_AUCTION[auction]:
            print(USER_INFO_IN_AUCTION[auction])
            settings.SIO.enter_room(sid, auction)
    if False and has_auction.exists():
        print('hassssssss liveeeeeeeee auctionnnnnnnnnnnn')
        settings.SIO.emit('has_live_auction', {'auction_id': has_auction.get().auction_id.pk})
    settings.SIO.save_session(sid, {'username': sid})


@settings.SIO.event
def disconnect(sid):
    print('disconnect ---------------------------------- ', sid)


@settings.SIO.event
def join_auction(sid, data):
    try:
        print('joiiiiiiiiiiiiiiiiindeeeeeeeeeeeeeeeeeeeeeeee')
        user_info = models.User.objects.get(pk=USER_INFO[sid]['pk'])
        user_in_auction = models.UserInAuction.objects.filter(
            user_id=user_info.pk,
            auction_id=data.get('auction_id'),
            status__in=['waiting', 'participant'],
        )
        if not user_in_auction.filter(auction_id__notebook_conditions__lt=user_info.balance).exists():
            can_join(sid=sid, data={'can_join': False, 'message': 'you dont have enough balance'})
            return

        # user_in_auction.update(status='participant')

        if not data.get('uuction_id') in USER_INFO_IN_AUCTION:
            USER_INFO_IN_AUCTION[data.get('auction_id')] = {'user_count': 0}

        USER_INFO_IN_AUCTION[data.get('auction_id')][user_info.pk] = {'sid': sid, 'user_id': user_info.pk, 'auction_id': data.get(
            'user_id'), 'province': user_info.location.province_name, 'country': user_info.location.country_id.country_name}

        USER_INFO_IN_AUCTION[data.get('auction_id')]['user_count'] += 1

        settings.SIO.enter_room(sid, data.get('auction_id'))
        settings.SIO.emit(
            'user_joined', USER_INFO_IN_AUCTION[data.get('auction_id')],
            room=data.get('auction_id'), skip_sid=sid)
        can_join(sid=sid, data={'can_join': True, 'message': 'ok', 'auction_id': data.get('auction_id')})

    except Exception as e:
        print('Error in EVENT join_auction: ', e)


def start_auction(*args, **kwargs):
    del COUNTDOWN_AUCTION[kwargs['auction_id']]
    models.Auction.objects.filter(pk=kwargs['auction_id']).update(status='live auction')
    car = models.CarInAuction.objects.filter(auction_id=kwargs['auction_id']).order_by('car_id')
    print(car)
    for i in range(car.count()):
        OUTBID_DATA[kwargs['auction_id']] = {
            'auction_id': kwargs['auction_id'],
            'car_bids_on_it': car[i].pk, 'price': car[i].car_id.price, 'counter': 0, 'number_of_cars': car.count(),
            'car_index': i+1, 'owner_car_id': car[i].car_id.user_id.pk
        }
        count = 0
        while count < 30:
            count += 1
            OUTBID_DATA[kwargs['auction_id']]['counter'] = count
            settings.SIO.emit('start_auction', OUTBID_DATA[kwargs['auction_id']], room=kwargs['auction_id'])
            # print(kwargs)
            print("hello world")
            print(OUTBID_DATA[kwargs['auction_id']])
            time.sleep(1)
        time.sleep(5)
    settings.SIO.emit('auction')
    auction_end(kwargs=kwargs)


def auction_end(*args, **kwargs):
    settings.SIO.emit('auction_end', room=kwargs['auction_id'])
    del OUTBID_DATA[kwargs['auction_id']]
    del USER_INFO_IN_AUCTION[kwargs['auction_id']]
    models.Auction.objects.filter(pk=kwargs['auction_id']).update(status='finished auction')


@settings.SIO.event
def outbid(sid, data):
    try:

        print('outbiddddddddddd0s0s0s0s0s0s0s0')

    except Exception as e:
        print('Error in EVENT outbid: ', e)


def can_join(sid: int, data):
    print(data)
    settings.SIO.emit('can_join', data, room=sid)
