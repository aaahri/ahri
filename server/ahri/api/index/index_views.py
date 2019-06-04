import json
from django.http import JsonResponse
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util, ObjectId
from utils.data_server import Mongo
import time


class IndexView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    col = mongo.col('index', 'index')

    def get(self, request, *args, **kwargs):
        try:
            article = self.col.find_one()
            if not article:
                return Response({'code': 300, 'msg': '未设置', 'data': {}})
            return Response({'code': 200, 'msg': '成功', 'data': json_util.dumps(article)})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def post(self, request, *args, **kwargs):
        try:
            user = json.loads(request.body)['user']
            if user:
                article = json.loads(request.body)['article']
                data = {
                    'title': article['title'],
                    'desc': article['desc'],
                    'category': ObjectId(article['category']),
                    'thumbnail': article['thumbnail'],
                    'author': ObjectId(user['_id']['$oid']),
                    'create_date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
                    'change_date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
                    'content': article['content'],
                    'removed': False,
                    'fabulous': 0,
                    'collection': 0
                }
                self.col.update({"_id": ObjectId('5ceb61033ef98cf0e0b0d3e2')}, data)
                return Response({'code': 200, 'msg': '成功', 'data': {}})
            else:
                return JsonResponse({'code': 400, 'msg': '用户验证失败！', 'data': {}})
        except Exception as e:
            return Response({'code': 500, 'msg': str(e), 'data': {}})

    def put(self, request, *args, **kwargs):
        try:
            put = QueryDict(request.body)
            user = json.loads(put.get('user'))
            if user:
                category = json.loads(put.get('category'))
                _id = category.pop('_id')['$oid']
                author = self.col.find_one({"_id": ObjectId(_id)})['author']
                category['author'] = ObjectId(author)
                category.update({'change_date': time.strftime('%Y-%m-%d', time.localtime(time.time()))})
                if self.col.find_one({'name': category['name'], 'author': ObjectId(author)}):
                    return Response({'code': 401, 'msg': '分类名已存在', 'data': {}})
                self.col.update({"_id": ObjectId(_id)}, category)
                return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
            else:
                return JsonResponse({'code': 400, 'msg': '用户验证失败！', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def delete(self, request, *args, **kwargs):
        try:
            delete = QueryDict(request.body)
            _id = delete.get('_id')
            return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
