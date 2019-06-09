import json
import random

from django.http import JsonResponse
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util, ObjectId
from utils.data_server import Mongo
from utils.send_email import SendEmail
import time
import re
import hashlib


class RegisterView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    col = mongo.col('user', 'user')

    def get(self, request, *args, **kwargs):
        try:
            email = request.GET.get('email', None)
            tag = False
            el = ['@gmail.com', '@qq.com', '@163.com', '@126.com', '@outlook.com', '@yahoo.com', '@sina.com',
                  '@188.com', '@sohu.com', '@mail.com']
            for i in el:
                if i in email:
                    tag = True
            if not tag:
                return Response({'code': 402, 'msg': '不支持该类型邮箱！', 'data': {}})
            op = request.GET.get('op', None)
            send = SendEmail()
            if op == '1':
                if self.col.find_one({'email': email}):
                    return Response({'code': 401, 'msg': '邮箱已存在', 'data': {}})
                else:
                    re_str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
                    if email and re.match(re_str, email):
                        code = ''.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4))
                        send.send(email, 1, code)
                        return Response({'code': 200, 'msg': '成功', 'data': {'code': code, 'email': email}})
                    else:
                        return Response({'code': 400, 'msg': '邮箱格式错误', 'data': {}})
            elif op == '2':
                if self.col.find_one({'email': email}):
                    code = ''.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4))
                    send.send(email, 1, code)
                    return Response({'code': 200, 'msg': '成功', 'data': {'code': code, 'email': email}})
                else:
                    return Response({'code': 401, 'msg': '邮箱不存在', 'data': {}})
            else:
                return Response({'code': 410, 'msg': '参数错误', 'data': {}})
        except Exception as e:
            return Response({'code': 500, 'msg': str(e), 'data': {}})

    def post(self, request, *args, **kwargs):
        try:
            form = json.loads(request.body)['form']
            if self.col.find_one({'username': form['username']}):
                return Response({'code': 401, 'msg': '用户名已存在', 'data': {}})
            b = hashlib.md5()
            b.update(form['password'].encode(encoding='utf-8'))
            user = {
                'username': form['username'],
                'password': b.hexdigest(),
                'avatar': '',
                'fullname': '',
                'sex': '不男不女',
                'birthday': '',
                'description': 'My name is ' + form['username'],
                'last': '',
                'email': form['email'],
                'telephone': '',
                'role': 5,
                'join_date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
                'mark': '',
                'level': '0',
                'empirical': '0',
                'lang': 'zh',
                'disable': False,
            }
            self.col.insert(user)
            return Response({'code': 200, 'msg': '成功', 'data': {}})
        except Exception as e:
            return Response({'code': 500, 'msg': str(e), 'data': {}})

    def put(self, request, *args, **kwargs):
        try:
            put = QueryDict(request.body)
            email = put.get('email')
            password = put.get('password')
            if email:
                b = hashlib.md5()
                b.update(password.encode(encoding='utf-8'))
                self.col.update_one({'email': email}, {'$set': {'password': b.hexdigest()}})
                return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
            else:
                return JsonResponse({'code': 400, 'msg': '邮箱不存在！', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
