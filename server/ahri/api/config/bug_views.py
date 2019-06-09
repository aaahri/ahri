import json

from bson import ObjectId, json_util
from django.http import JsonResponse, QueryDict
from rest_framework.views import APIView
from utils.data_server import Mongo
import time


class BugView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    col = mongo.col('setting', 'bug')
    u_col = mongo.col('user', 'user')

    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get('user_id'):
                bugs = self.col.find()
                a = []
                for i in bugs:
                    if i['user']:
                        i['username'] = self.u_col.find_one({'_id': ObjectId(i['user'])})['username']
                    else:
                        i['username'] = ''
                    a.append(i)
                return JsonResponse({'code': 200, 'msg': '成功', 'data': json_util.dumps(a)})
            return JsonResponse({'code': 400, 'msg': '成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def post(self, request, *args, **kwargs):
        try:
            d = json.loads(request.body)
            if d['bug']:
                user = d['user_id']
                if user:
                    user = ObjectId(d['user_id'])
                data = {
                    'user': user,
                    'bug': d['bug'],
                    'date': time.strftime('%Y-%m-%d', time.localtime(time.time()))
                }
                self.col.insert(data)
            return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def delete(self, request, *args, **kwargs):
        try:
            delete = QueryDict(request.body)
            _id = delete.get('_id')
            self.col.delete_many({"_id": ObjectId(_id)})
            return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
