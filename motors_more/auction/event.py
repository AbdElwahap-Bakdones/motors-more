from django.conf import settings
import jwt
from . import models
USER_SID = {}
USER_INFO = {}
# USER_SIDS_IN_AUCTION {auction_id:{'sid':sid,'auction_id':auction_id,'user_id':user_id,'country':country,'province':province}}
USER_SIDS_IN_AUCTION = {int: {str: int, str: int, str: int, str: str, str: str}}
# OUTBID_DATA {auction_id:{}}
OUTBID_DATA = {int: dict}


@settings.SIO.event
def connect(sid, environ, auth):
    user = jwt.decode(
        jwt=auth.get('token'),
        algorithms='HS256', key=settings.SECRET_KEY)
    # print(user.get('user_id'))
    USER_SID[user.get('user_id')] = sid
    USER_INFO[sid] = models.User.objects.get(pk=user.get('user_id'))

    if models.UserInAuction.objects.filter(user_id=user.get('user_id'), status='participant').exists():
        print('hassssssss liveeeeeeeee auctionnnnnnnnnnnn')
        settings.SIO.emit('has_live_auction', {'has_live_auction': True})
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++ ')
    settings.SIO.save_session(sid, {'username': sid})


@settings.SIO.event
def disconnect(sid):
    print('disconnect ----------------------------------', sid)


@settings.SIO.event
def join_auction(sid, data):
    try:
        print('joiiiiiiiiiiiiiiiiinde')
        print(USER_INFO[sid]['email'])
        user_info = models.User.objects.get(pk=USER_INFO[sid]['pk'])
        user_in_auction = models.UserInAuction.objects.filter(
            user_id=user_info.pk,
            auction_id=data.get('auction_id'),
            status__in=['waiting', 'participant'],
            auction_id__notebook_conditions__lt=user_info.balance)
        if user_in_auction.exists():
            user_in_auction.update(status='participant')
            USER_SIDS_IN_AUCTION[data.get('auction_id')] = {'sid': sid, 'user_id': user_info.pk, 'auction_id': data.get(
                'user_id',), 'province': user_info.location.province_name, 'country': user_info.location.country_id.country_name}
            settings.SIO.enter_room(sid, data.get('auction_id'))
            settings.SIO.emit('user_joined', USER_SIDS_IN_AUCTION[data.get('auction_id')])
    except Exception as e:
        print('Error in EVENT join_auction: ', e)


@settings.SIO.event
def outbid(sid, data):
    try:

        print('outbiddddddddddd0s0s0s0s0s0s0s0')

    except Exception as e:
        print('Error in EVENT outbid: ', e)


@settings.SIO.event
def hello(sid, data):
    print(data)
    # print(data)
    print('  helooooooooooooooooooooooooooo ')
    # SIO.save_session(sid, {'username': sid})
