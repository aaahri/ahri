import json
import time

from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util, ObjectId
from utils.data_server import Mongo
import hashlib


class LoginView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    col = mongo.col('user', 'user')

    def post(self, request, *args, **kwargs):
        try:
            form = json.loads(request.body)['form']
            b = hashlib.md5()
            b.update(form['password'].encode(encoding='utf-8'))
            password = b.hexdigest()
            user = self.col.find_one(
                {'$or': [{'username': form['username'], 'password': password},
                         {'email': form['username'], 'password': password}]})
            if user:
                if user['disable']:
                    return Response({'code': 401, 'msg': '用户被禁用', 'data': {}})
                t = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                self.col.update({"_id": ObjectId(user['_id'])},
                                {'$set': {'last': t}})
                user['last'] = t
                return Response({'code': 200, 'msg': 'success', 'data': json_util.dumps(user)})
            return Response({'code': 400, 'msg': '用户名或密码错误', 'data': {}})
        except Exception as e:
            return Response({'code': 500, 'msg': str(e), 'data': {}})
