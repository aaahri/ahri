import json
import os
import random

from django.http import JsonResponse
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util, ObjectId

from ahri.settings import MEDIA_ROOT, D
from utils.data_server import Mongo
import time
import re
import hashlib


def upload(request):
    try:
        img = request.FILES.get('avatar')
        username = request.POST.get('username')
        file_path = MEDIA_ROOT + '/' + username
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        t = time.strftime('%Y%m%d', time.localtime(time.time()))
        r = ''.join(random.sample(
            ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K',
             'k',
             'L', 'l', 'M', 'm', 'N' 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V',
             'v',
             'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z'], 8))
        filename = t + r + os.path.splitext(img.name)[-1]
        with open(os.path.join(MEDIA_ROOT + '/' + username, filename), 'wb') as fp:
            for chunk in img.chunks():
                fp.write(chunk)
        url = D + '/media/' + username + '/' + filename
        result = {'code': 200, 'url': url}
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})


class AuthView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    col = mongo.col('user', 'user')

    def get(self, request, *args, **kwargs):
        try:
            user = json.loads(request.GET.get('user', None))
            if user['role'] == 100:
                all = self.col.find()
                a = []
                for i in all:
                    a.append(i)
                return Response({'code': 200, 'msg': '成功', 'data': json_util.dumps(a)})
            return Response({'code': 400, 'msg': '用户验证失败', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def put(self, request, *args, **kwargs):
        try:
            put = QueryDict(request.body)
            user = json.loads(put.get('user'))
            if user:
                _id = user.pop('_id')['$oid']
                self.col.update({"_id": ObjectId(_id)}, user)
                return JsonResponse(
                    {'code': 200, 'msg': '成功', 'data': json_util.dumps(self.col.find_one({"_id": ObjectId(_id)}))})
            else:
                return JsonResponse({'code': 400, 'msg': '用户验证失败！', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
