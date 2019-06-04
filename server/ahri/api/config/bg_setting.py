import json
import os
import random

from django.http import JsonResponse
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util, ObjectId
from utils.data_server import Mongo
import time
from ahri.settings import MEDIA_ROOT, D


def upload(request):
    try:
        img = request.FILES.get('thumbnail')
        username = request.POST.get('username')
        file_path = MEDIA_ROOT + '/' + username
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        if not os.path.exists(file_path + '/resource'):
            os.makedirs(file_path + '/resource')
        if not os.path.exists(file_path + '/category'):
            os.makedirs(file_path + '/category')
        if not os.path.exists(file_path + '/article'):
            os.makedirs(file_path + '/article')
        name = img.name
        t = time.strftime('%Y%m%d', time.localtime(time.time()))
        r = ''.join(random.sample(
            ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K',
             'k',
             'L', 'l', 'M', 'm', 'N' 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V',
             'v',
             'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z'], 8))
        filename = t + r + os.path.splitext(img.name)[-1]
        with open(os.path.join(MEDIA_ROOT + '/' + username + '/' + 'article', filename), 'wb') as fp:
            for chunk in img.chunks():
                fp.write(chunk)
        url = D + '/media/' + username + '/article/' + filename
        result = {'code': 200, 'url': url}
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})


class BGSettingView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    col = mongo.col('setting', 'bg')
    u_col = mongo.col('user', 'user')

    def get(self, request, *args, **kwargs):
        if request.GET.get('bg') == 'bg':
            user_id = request.GET.get('user_id')
            try:
                bg = self.col.find_one({"user": ObjectId(user_id), 'is_bg': True})
                return JsonResponse({'code': 200, 'msg': '成功', 'data': json_util.dumps(bg)})
            except Exception as e:
                return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
        else:
            try:
                user_id = request.GET.get('user_id')
                bg = self.col.find({"user": ObjectId(user_id)})
                a = []
                a.append({
                    'url': D + '/media/bg.jpg'
                })
                for i in bg:
                    a.append(i)
                return JsonResponse({'code': 200, 'msg': '成功', 'data': json_util.dumps(a)})
            except Exception as e:
                return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def post(self, request, *args, **kwargs):
        try:
            img = request.FILES.get('bg')
            username = request.POST.get('username')
            user_id = request.POST.get('user_id')
            file_path = MEDIA_ROOT + '/' + username
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            if not os.path.exists(file_path + '/resource'):
                os.makedirs(file_path + '/resource')
            t = time.strftime('%Y%m%d', time.localtime(time.time()))
            r = ''.join(random.sample(
                ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j',
                 'K',
                 'k',
                 'L', 'l', 'M', 'm', 'N' 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V',
                 'v',
                 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z'], 8))
            filename = t + r + os.path.splitext(img.name)[-1]
            with open(os.path.join(MEDIA_ROOT + '/' + username + '/resource', filename), 'wb') as fp:
                for chunk in img.chunks():
                    fp.write(chunk)
            url = D + '/media/' + username + '/resource/' + filename
            x = self.col.insert({
                'user': ObjectId(user_id),
                'username': username,
                'url': url,
                'is_bg': False
            })
            result = {'code': 200, 'msg': '成功', 'data': json_util.dumps(self.col.find_one({'_id': ObjectId(x)}))}
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def put(self, request, *args, **kwargs):
        try:
            put = QueryDict(request.body)
            user_id = put.get('user_id')
            url = put.get('url')
            self.col.update_many({'user': ObjectId(user_id)}, {'$set': {'is_bg': False}})
            self.col.update_one({'user': ObjectId(user_id), 'url': url}, {'$set': {'is_bg': True}})
            return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def delete(self, request, *args, **kwargs):
        try:
            delete = QueryDict(request.body)
            _id = delete.get('_id')
            self.col.delete_one({"_id": ObjectId(_id)})
            return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
