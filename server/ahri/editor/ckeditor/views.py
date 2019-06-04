from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import time
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def hello(request):
    print(request.POST.get('user'))
    return render(request, 'editor/ckeditor/index.html')


@method_decorator(csrf_exempt)
def upload(request):
    file = request.FILES.get("upload")
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
    s = "{\"uploaded\": true,\"url\": \"" + url + "\"}"
    return HttpResponse(s)
