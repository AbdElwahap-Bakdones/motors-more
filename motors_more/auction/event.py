from django.conf import settings
import jwt
from . import models, serializers
import time


# USER_SID = {user_id:sid}
USER_SID = {}
# USER_INFO ={sid:{'pk': user_info.pk, 'email': user_info.email, 'user_kind': user_info.user_kind}}
USER_INFO = {}
# USER_SIDS_IN_AUCTION {auction_id:{'user_count':user_count,user_id:{'sid':sid,'auction_id':auction_id,'user_id':user_id,'country':country,'province':province}}}
USER_INFO_IN_AUCTION = {int: {str: int, int: {str: int, str: int, str: int, str: str, str: str}}}
# OUTBID_DATA {auction_id:{'auction_id': 0,'car_bids_on_it': 0, 'price': 0, 'counter': 0, 'number_of_cars': 0,'car_index': 0, 'owner_car_id': 0}}
OUTBID_DATA = {int: {str: int, str: int, str: int, str: int, str: int, str: int, str: int}}
COUNTDOWN_AUCTION = {}
BIDDING = {0: False}


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
    has_auction = models.UserInAuction.objects.filter(
        user_id=user.get('user_id'),
        auction_id__status='live auction')

    if has_auction.filter(status='participant').exists():
        print('hassssssss liveeeeeeeee auctionnnnnnnnnnnn')
        for auction in USER_INFO_IN_AUCTION:
            if user_info.pk in USER_INFO_IN_AUCTION[auction]:
                settings.SIO.enter_room(sid, auction)
        settings.SIO.emit('has_live_auction', {'auction_id': has_auction.get().auction_id.pk}, room=sid)
        return

    if has_auction.filter(status='waiting').exists():
        print('senddddddddddddd notifyyyyyyyyyyyyyyyy tooooo joinnnnnnnnnnn')
        settings.SIO.emit('liveAuctionTime', {'auction_id': str(has_auction.first().auction_id.pk)}, room=sid)
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

        user_in_auction.update(status='participant')

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
    BIDDING[0] = False
    models.Auction.objects.filter(pk=kwargs['auction_id']).update(status='live auction')
    car = models.CarInAuction.objects.filter(auction_id=kwargs['auction_id']).order_by('car_id')
    print(car)
    for i in range(car.count()):
        OUTBID_DATA[kwargs['auction_id']] = {
            'auction_id': kwargs['auction_id'],
            'car_bids_on_it': car[i].car_id.pk, 'price': car[i].car_id.price, 'counter': 0, 'number_of_cars': car.count(),
            'car_index': i+1, 'owner_car_id': car[i].car_id.user_id.pk
        }
        count = 0
        while count < 30:
            count += 1
            OUTBID_DATA[kwargs['auction_id']]['counter'] = count
            print(BIDDING[0])
            if BIDDING[0]:
                count = 0
                BIDDING[0] = False
                time.sleep(0.2)
                continue
            settings.SIO.emit('start_auction', OUTBID_DATA[kwargs['auction_id']], room=kwargs['auction_id'])
            # print(kwargs)
            print("hello world")
            print(OUTBID_DATA[kwargs['auction_id']])
            time.sleep(1)
        if 'last_user_bidding' in OUTBID_DATA[kwargs['auction_id']]:
            print('last_user_bidding')
            data = {'auction_id': kwargs['auction_id'],
                    'buyer': 1,  # OUTBID_DATA[kwargs['auction_id']]['last_user_bidding'],
                    'seller': OUTBID_DATA[kwargs['auction_id']]['owner_car_id'],
                    'car_id': OUTBID_DATA[kwargs['auction_id']]['car_bids_on_it'],
                    'price': OUTBID_DATA[kwargs['auction_id']]['price']}
            serializer = serializers.AutoSoldSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            models.CarInAuction.objects.filter(
                car_id=OUTBID_DATA[kwargs['auction_id']]['car_bids_on_it']).update(
                status='sold')

        time.sleep(3)
    settings.SIO.emit('auction')
    auction_end(auction_id=kwargs['auction_id'])


def auction_end(auction_id: int):
    settings.SIO.emit('auction_end', room=auction_id)
    del OUTBID_DATA[auction_id]
    del USER_INFO_IN_AUCTION[auction_id]
    models.UserInAuction.objects.filter(auction_id=auction_id)
    models.Auction.objects.filter(pk=auction_id).update(status='finished auction')
    cars = models.CarInAuction.objects.filter(auction_id=auction_id, status='for sale').values_list('car_id', flat=True)
    models.RequestAuction.objects.filter(car_id__in=cars).update(status='pending')


@settings.SIO.event
def outbid(sid, data):
    try:
        print('outbidoutbidoutbidoutbidoutbidoutbid')
        if OUTBID_DATA[data['auction_id']]['counter'] == 0:
            print('erorrrrrorororororroo111111111111111111')
            settings.SIO.emit('bidding_error', {'message': 'auction has finash'}, room=sid)

            return
        if False and USER_INFO[sid].get('pk') == data['owner_car_id']:
            print('erorrrrrorororororro2222222222222222222')
            settings.SIO.emit('bidding_error', {'message': 'you can\'t bidding on your own cars'}, room=sid)
            return
        BIDDING[0] = True
        print(data)
        models.Car.objects.filter(pk=data['car_bids_on_it']).update(price=data['amount'])
        OUTBID_DATA[data['auction_id']]['price'] += data['amount']
        OUTBID_DATA[data['auction_id']]['last_user_bidding'] = USER_INFO[sid].get('pk')
    except Exception as e:
        print('Error in EVENT outbid: ', e)


def can_join(sid: int, data):
    print(data)
    settings.SIO.emit('can_join', data, room=sid)
