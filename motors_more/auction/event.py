from django.conf import settings


USER_SID = {}


@settings.SIO.event
def connect(sid, token):
    # sid = 123
    print(sid)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++ ')
    settings.SIO.save_session(sid, {'username': sid})


@settings.SIO.event
def hello(sid, data):
    print(data)
    # print(data)
    print('helooooooooooooooooooooooooooo ')
    # SIO.save_session(sid, {'username': sid})
