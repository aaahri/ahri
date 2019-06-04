from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util
from utils.data_server import Mongo


class IndexLastView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    col = mongo.col('article', 'article')

    def get(self, request, *args, **kwargs):
        try:
            article = self.col.find({'removed': False, 'private': False}).sort([('_id', -1)]).limit(10)
            return Response({'code': 200, 'msg': '成功', 'data': json_util.dumps(article)})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
