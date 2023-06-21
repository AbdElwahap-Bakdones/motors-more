from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from subprocess import call

import requests
from ipaddress import ip_address, ip_network


@require_POST
@csrf_exempt
def pull(request):
    # Verify if request came from GitHub
    forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))
    client_ip_address = ip_address(forwarded_for)
    whitelist = requests.get('https://api.github.com/meta').json()['hooks']

    for valid_ip in whitelist:
        if client_ip_address in ip_network(valid_ip):
            break
    else:
        print('Permission denied.')
        return HttpResponseForbidden('Permission denied.')
    
    print('pull from github')
    comm = 'cd /home/AbdElwahapBak2/motors-more \ngit clean \ngit restore -fd\ngit pull \ncd /var/www/\ntouch /var/www/abdelwahapbak2_pythonanywhere_com_wsgi.py\n'
    rc = call(comm, shell=True)
    return HttpResponse('pulling')
