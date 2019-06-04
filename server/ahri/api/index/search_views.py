import json
from django.http import JsonResponse
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util, ObjectId
from utils.data_server import Mongo
import time


class SearchView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    c_col = mongo.col('article', 'category')
    a_col = mongo.col('article', 'article')
    u_col = mongo.col('user', 'user')

    def is_pri(self, cate):
        a = []
        for i in cate:
            a.append(i['_id'])
        return a

    def get(self, request, *args, **kwargs):
        try:
            content = request.GET.get('content', None)
            cate = self.c_col.find({'private': False})
            article = self.a_col.find({'title': {'$regex': content}, 'removed': False})
            x = []
            y = []
            z = []
            for c in cate:
                z.append(c['_id'])
                if content in c['name']:
                    c['author_name'] = self.u_col.find_one({'_id': ObjectId(c['author'])})['username']
                    if self.a_col.find_one({'category': ObjectId(c['_id'])}):
                        c['first'] = self.a_col.find_one({'category': ObjectId(c['_id'])})['_id']
                    else:
                        c['first'] = ''
                    x.append(c)
            for j in article:
                if j['category'] in z:
                    j['author_name'] = self.u_col.find_one({'_id': ObjectId(j['author'])})['username']
                    y.append(j)
            data = {'category': json_util.dumps(x), 'article': json_util.dumps(y)}
            return Response({'code': 200, 'msg': '成功', 'data': data})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
