from bson import ObjectId
from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
import time
import random

from ahri.settings import MEDIA_ROOT, D
from utils.data_server import Mongo


def hello(request):
    mongo = Mongo()
    col = mongo.col('article', 'category')
    a_col = mongo.col('article', 'article')
    u_col = mongo.col('user', 'user')
    if request.POST.get('type') == 'n':
        try:
            user_id = request.POST.get('user', None)
            user = u_col.find_one({"_id": ObjectId(user_id)})
            if user:
                if user['role'] == 100:
                    category = col.find()
                else:
                    category = col.find({"author": ObjectId(user_id)})
                a = []
                for i in category:
                    # i['author_name'] = u_col.find_one({"_id": ObjectId(i['author'])})['username']
                    i['id'] = i['_id']
                    a.append(i)
                return render(request, 'editor/wangeditor/index.html',
                              context={'data': a, 'art': False, 'username': user['username'], 'user_id': user['_id']})
            else:
                # return redirect("http://192.168.1.2:8080/#/admin")
                return redirect("https://www.aaahri.com/#/admin/article/")
        except Exception as e:
            return render(request, 'editor/wangeditor/index.html')
    else:
        try:
            art = a_col.find_one({'_id': ObjectId(request.POST.get('type'))})
            user_id = request.POST.get('user', None)
            user = u_col.find_one({"_id": ObjectId(user_id)})
            if user:
                if user['role'] == 100:
                    category = col.find()
                else:
                    category = col.find({"author": ObjectId(user_id)})
                a = []
                for i in category:
                    i['id'] = i['_id']
                    a.append(i)
                return render(request, 'editor/wangeditor/index.html',
                              context={'data': a, 'art': art, 'art_id': art['_id'], 'username': user['username'],
                                       'user_id': user['_id']})
            else:
                # return redirect("http://192.168.1.2:8080/#/admin")
                return redirect("https://www.aaahri.com/#/admin/article/")
        except Exception as e:
            return render(request, 'editor/wangeditor/index.html')


def upload(request):
    file = request.FILES.get("FileName")
    name = file.name
    r = random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 6)
    ss = ""
    for i in r:
        ss += i
    name = ss + time.strftime('_%Y%m%d%H%M%S', time.localtime()) + os.path.splitext(name)[1]

    with open(os.path.join(MEDIA_ROOT + '/' + 'article', "A" + name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = D + '/media/article/' + "A" + name
    s = "{\"errno\": 0,\"data\": [\"" + url + "\"]}"
    return HttpResponse(s)
