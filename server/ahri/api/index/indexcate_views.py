from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util, ObjectId
from utils.data_server import Mongo


class IndexCateView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    col = mongo.col('article', 'category')
    a_col = mongo.col('article', 'article')
    u_col = mongo.col('user', 'user')

    def get(self, request, *args, **kwargs):
        try:
            user_id = self.u_col.find_one({'username': 'ahri'})['_id']
            category = self.col.find({'private': False, 'author': ObjectId(user_id)})
            a = []
            for i in category:
                i['username'] = 'ahri'
                if self.a_col.find_one({'category': ObjectId(i['_id'])}):
                    i['first'] = self.a_col.find_one({'category': ObjectId(i['_id'])})['_id']
                else:
                    i['first'] = ''
                a.append(i)
            return Response({'code': 200, 'msg': '成功', 'data': json_util.dumps(a)})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
