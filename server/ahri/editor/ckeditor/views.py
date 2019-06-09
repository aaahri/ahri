from bson import ObjectId, json_util
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import os
import time
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from utils.data_server import Mongo


def hello(request):
    mongo = Mongo()
    col = mongo.col('article', 'category')
    a_col = mongo.col('article', 'article')
    u_col = mongo.col('user', 'user')
    print(request.POST.get('user'))
    if request.POST.get('type') == 'e':
        try:
            article = col.find_one({"_id": ObjectId(request.GET.get('_id'))})
            # return Response({'code': 200, 'msg': 'success', 'data': json_util.dumps(article)})
            return render(request, 'editor/ckeditor/index.html')
        except Exception as e:
            return render(request, 'editor/ckeditor/index.html')
    else:
        try:
            user_id = request.POST.get('user', None)
            user = u_col.find_one({"_id": ObjectId(user_id)})
            if not user:
                if user['role'] == 100:
                    category = col.find()
                else:
                    category = col.find({"author": ObjectId(user_id)})
                a = []
                for i in category:
                    i['author_name'] = u_col.find_one({"_id": ObjectId(i['author'])})['username']
                    a.append(i)
                print(a)
                return render(request, 'editor/ckeditor/index.html', context={'data': a})
            else:
                return redirect("http://baidu.com")
                return render(request, 'editor/ckeditor/index.html')
        except Exception as e:
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
