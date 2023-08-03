from django.conf import settings
import jwt
from . import models
USER_SID = {}
USER_INFO = {}
USER_SIDS_IN_AUCTION = {}


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
def hello(sid, data):
    print(data)
    # print(data)
    print('  helooooooooooooooooooooooooooo ')
    # SIO.save_session(sid, {'username': sid})


@settings.SIO.event
def join_auction(sid, data):
    try:
        print('joiiiiiiiiiiiiiiiiinde')
        print(USER_INFO[sid]['email'])
        models.UserInAuction.objects.filter(user_id=USER_INFO[sid]['pk']).update(stats='participant')
        # USER_SIDS_IN_AUCTION
        settings.SIO.enter_room(sid, data.get.get('auction_id'))
        user_info = models.User.objects.filter(pk=USER_SID)
        data = {}
        settings.SIO.emit('user_joined')
    except Exception as e:
        print('Error in EVENT join_auction: ', e)


@settings.SIO.event
def outbid(sid, data):
    try:

        print('outbiddddddddddd0s0s0s0s0s0s0s0')

    except Exception as e:
        print('Error in EVENT outbid: ', e)
