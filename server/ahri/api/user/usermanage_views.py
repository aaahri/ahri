import json
from django.http import JsonResponse
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util, ObjectId
from utils.data_server import Mongo


class UserManageView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    col = mongo.col('user', 'user')

    def get(self, request, *args, **kwargs):
        try:
            user = json.loads(request.GET.get('user', None))
            if user and user['role'] == 100:
                users = self.col.find()
                a = []
                for i in users:
                    a.append(i)
                return Response({'code': 200, 'msg': '成功', 'data': json_util.dumps(a)})
            return Response({'code': 400, 'msg': '用户验证失败', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def post(self, request, *args, **kwargs):
        try:
            id = json.loads(request.body)['id']
            user_id = json.loads(request.body)['user_id']
            disable = json.loads(request.body)['disable']
            user = self.col.find_one({'_id': ObjectId(id)})
            if user:
                self.col.update_one({'_id': ObjectId(user_id)}, {'$set': {'disable': disable}})
                users = self.col.find()
                a = []
                for i in users:
                    a.append(i)
                return Response({'code': 200, 'msg': '成功', 'data': json_util.dumps(a)})
            else:
                return JsonResponse({'code': 400, 'msg': '用户验证失败！', 'data': {}})
        except Exception as e:
            return Response({'code': 500, 'msg': str(e), 'data': {}})

    def put(self, request, *args, **kwargs):
        try:
            put = QueryDict(request.body)
            id = put.get('id')
            user_id = put.get('user_id')
            role = put.get('role')
            user = self.col.find_one({'_id': ObjectId(id)})
            if user:
                self.col.update_one({'_id': ObjectId(user_id)}, {'$set': {'role': int(role)}})
                return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
            else:
                return JsonResponse({'code': 400, 'msg': '用户验证失败！', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def delete(self, request, *args, **kwargs):
        try:
            delete = QueryDict(request.body)
            id = delete.get('id')
            user_id = delete.get('user_id')
            user = self.col.find_one({'_id': ObjectId(id)})
            if user and user['role'] == 100:
                self.col.delete_many({"_id": ObjectId(user_id)})
                users = self.col.find()
                a = []
                for i in users:
                    a.append(i)
                return Response({'code': 200, 'msg': '成功', 'data': json_util.dumps(a)})
            else:
                return JsonResponse({'code': 400, 'msg': '用户权限不足', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
