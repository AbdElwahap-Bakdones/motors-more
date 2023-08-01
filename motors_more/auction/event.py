from django.conf import settings
import jwt

USER_SID = {}
USER_SIDS_IN_AUCTION = {}


@settings.SIO.event
def connect(sid, environ, auth):
    print('connect ', sid)
    print('auth ', auth)

    token = jwt.decode(
        jwt='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk2MDk2ODk3LCJpYXQiOjE2OTA5MTI4OTcsImp0aSI6ImExMTBiNThlMmYzNDQ0MDc5NGM2ZjU2Yzg4ZGI4YmI1IiwidXNlcl9pZCI6MX0.f0PtSH0VUF59lz2M0VKC2M8essYFZxLhwqEUzQYQRUw',
        algorithms='HS256', key=settings.SECRET_KEY)
    print(token.get('user_id'))
    USER_SID[token.get('user_id')] = sid
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++ ')
    settings.SIO.save_session(sid, {'username': sid})


@settings.SIO.event
def disconnect(sid):
    print('disconnect ----------------------------------', sid)


@settings.SIO.event
def hello(sid, data):
    print(data)
    # print(data)
    print('helooooooooooooooooooooooooooo ')
    # SIO.save_session(sid, {'username': sid})


@settings.SIO.event
def join_auction(sid, data):
    try:
        print('joiiiiiiiiiiiiiiiiinde')
        settings.SIO.enter_room(sid, data.get.get('auction_id'))
    except Exception as e:
        print('Error in EVENT join_auction: ', e)


@settings.SIO.event
def outbid(sid, data):
    try:

        print('outbiddddddddddd0s0s0s0s0s0s0s0')

    except Exception as e:
        print('Error in EVENT outbid: ', e)
