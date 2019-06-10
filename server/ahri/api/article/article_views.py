import json
import os
import random

from django.http import JsonResponse
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util, ObjectId
from utils.data_server import Mongo
import time
from ahri.settings import MEDIA_ROOT
from ahri.settings import D


def upload(request):
    try:
        img = request.FILES.get('thumbnail')
        username = request.POST.get('username')
        file_path = MEDIA_ROOT + '/' + username
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        if not os.path.exists(file_path + '/resource'):
            os.makedirs(file_path + '/resource')
        if not os.path.exists(file_path + '/category'):
            os.makedirs(file_path + '/category')
        if not os.path.exists(file_path + '/article'):
            os.makedirs(file_path + '/article')
        name = img.name
        t = time.strftime('%Y%m%d', time.localtime(time.time()))
        r = ''.join(random.sample(
            ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K',
             'k',
             'L', 'l', 'M', 'm', 'N' 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V',
             'v',
             'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z'], 8))
        filename = t + r + os.path.splitext(img.name)[-1]
        with open(os.path.join(MEDIA_ROOT + '/' + username + '/' + 'article', filename), 'wb') as fp:
            for chunk in img.chunks():
                fp.write(chunk)
        url = D + '/media/' + username + '/article/' + filename
        result = {'code': 200, 'url': url}
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})


class ArticleView(APIView):
    mongo = Mongo()
    col = mongo.col('article', 'article')
    c_col = mongo.col('article', 'category')
    u_col = mongo.col('user', 'user')

    def get(self, request, *args, **kwargs):
        if request.GET.get('_id'):
            try:
                article = self.col.find_one({"_id": ObjectId(request.GET.get('_id'))})
                return Response({'code': 200, 'msg': 'success', 'data': json_util.dumps(article)})
            except Exception as e:
                return Response({'code': 500, 'msg': str(e), 'data': {}})
        else:
            try:
                user_id = request.GET.get('user_id', None)
                user = self.u_col.find_one({"_id": ObjectId(user_id)})
                if user:
                    if user['role'] == 100:
                        article = self.col.find({'removed': False})
                    else:
                        article = self.col.find({"author": ObjectId(user_id), 'removed': False})
                    a = []
                    for i in article:
                        i['author_name'] = self.u_col.find_one({'_id': ObjectId(i['author'])})['username']
                        i['category_name'] = self.c_col.find_one({'_id': ObjectId(i['category'])})['name']
                        a.append(i)
                    return Response({'code': 200, 'msg': '成功', 'data': json_util.dumps(a)})
                else:
                    return Response({'code': 400, 'msg': '用户验证失败', 'data': {}})
            except Exception as e:
                return Response({'code': 500, 'msg': str(e), 'data': {}})

    def post(self, request, *args, **kwargs):
        try:
            user = json.loads(request.body)['user']
            if user:
                article = json.loads(request.body)['article']
                if self.col.find_one({'title': article['title'], 'author': ObjectId(user['_id']['$oid'])}):
                    return Response({'code': 401, 'msg': '文章标题重复', 'data': {}})
                cate = self.c_col.find_one({'_id': ObjectId(article['category'])})
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
                    'private': cate['private'],
                    'fabulous': 0,
                    'collection': 0,
                    'editor': article['editor']
                }
                x = self.col.insert(data)
                re = self.col.find_one({"_id": ObjectId(x)})
                re['author'] = user['username']
                return Response(
                    {'code': 200, 'msg': '成功', 'data': json_util.dumps(re)})
            else:
                return JsonResponse({'code': 400, 'msg': '用户验证失败！', 'data': {}})
        except Exception as e:
            return Response({'code': 500, 'msg': str(e), 'data': {}})

    def put(self, request, *args, **kwargs):
        try:
            put = QueryDict(request.body)
            user = json.loads(put.get('user'))
            if user:
                article = json.loads(put.get('article'))
                _id = article.pop('_id')
                article['change_date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                data = {'title': article['title'],
                        'category': ObjectId(article['category']),
                        'thumbnail': article['thumbnail'],
                        'desc': article['desc'],
                        'content': article['content'],
                        'change_date': time.strftime('%Y-%m-%d', time.localtime(time.time()))
                        }
                self.col.update({"_id": ObjectId(_id)}, {'$set': data})
                return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
            else:
                return JsonResponse({'code': 400, 'msg': '用户验证失败！', 'data': {}})
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
