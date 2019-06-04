from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import time
import random


def hello(request):
    return render(request, 'editor/wangeditor/index.html')


def upload(request):
    file = request.FILES.get("FileName")
    name = file.name
    r = random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 6)
    ss = ""
    for i in r:
        ss += i
    name = ss + time.strftime('_%Y%m%d%H%M%S', time.localtime()) + os.path.splitext(name)[1]
    with open(os.path.join(settings.MEDIA_ROOT, "A" + name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    url = request.build_absolute_uri(settings.MEDIA_URL + "A" + name)
    s = "{\"errno\": 0,\"data\": [\"" + url + "\"]}"
    return HttpResponse(s)
