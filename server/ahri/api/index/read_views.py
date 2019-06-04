import json
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util, ObjectId
from utils.data_server import Mongo
import time


class ReadView(APIView):
    mongo = Mongo(ip='111.67.206.108')
    col = mongo.col('article', 'article')
    c_col = mongo.col('article', 'category')
    u_col = mongo.col('user', 'user')

    def get(self, request, *args, **kwargs):
        try:
            _id = self.col.find_one({"_id": ObjectId(request.GET.get('id'))})['category']
            article = self.col.find({"category": ObjectId(_id)})
            a = []
            for i in article:
                i['author_name'] = self.u_col.find_one({'_id': ObjectId(i['author'])})['username']
                a.append(i)
            return Response({'code': 200, 'msg': 'success', 'data': json_util.dumps(a)})
        except Exception as e:
            return Response({'code': 500, 'msg': str(e), 'data': {}})
