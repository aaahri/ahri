import json
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
            comment = self.col.find({"article": ObjectId(request.GET.get('article')), 'removed': False})
            a = []
            for i in comment:
                i['user_name'] = self.u_col.find_one({'_id': ObjectId(i['user'])})['username']
                a.append(i)
            return Response({'code': 200, 'msg': 'success', 'data': json_util.dumps(a)})
        except Exception as e:
            return Response({'code': 500, 'msg': str(e), 'data': {}})

    def post(self, request, *args, **kwargs):
        try:
            user = json.loads(request.body)['user']
            if user:
                content = json.loads(request.body)['content']
                article = json.loads(request.body)['article']
                data = {
                    'content': content,
                    'date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
                    'author': self.a_col.find_one({'_id': ObjectId(article)})['author'],
                    'user': ObjectId(user['_id']['$oid']),
                    'article': ObjectId(article),
                    'removed': False,
                    'fabulous': 0
                }
                x = self.col.insert(data)
                re = self.col.find_one({"_id": ObjectId(x)})
                re['user_name'] = user['username']
                return Response(
                    {'code': 200, 'msg': '成功', 'data': json_util.dumps(re)})
            else:
                return Response({'code': 400, 'msg': '用户验证失败！', 'data': {}})
        except Exception as e:
            return Response({'code': 500, 'msg': str(e), 'data': {}})
