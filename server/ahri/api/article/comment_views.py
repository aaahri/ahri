import json
from django.http import JsonResponse
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util, ObjectId
from utils.data_server import Mongo
import time


class CommentView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    col = mongo.col('article', 'comment')
    a_col = mongo.col('article', 'article')
    u_col = mongo.col('user', 'user')

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.GET.get('user_id', None)
            user = self.u_col.find_one({"_id": ObjectId(user_id)})
            if user:
                if user['role'] == 100:
                    comment = self.col.find({'removed': False})
                else:
                    comment = self.col.find({'removed': False, "author": ObjectId(user_id)})
                a = []
                for i in comment:
                    i['user_name'] = self.u_col.find_one({"_id": ObjectId(i['user'])})['username']
                    i['art_title'] = self.a_col.find_one({"_id": ObjectId(i['article'])})['title']
                    a.append(i)
                return Response({'code': 200, 'msg': '成功', 'data': json_util.dumps(a)})
            else:
                return Response({'code': 400, 'msg': '用户验证失败', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def delete(self, request, *args, **kwargs):
        try:
            delete = QueryDict(request.body)
            _id = delete.get('_id')
            self.col.update({"_id": ObjectId(_id)}, {'$set': {'removed': True}})
            return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
