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
from ahri.settings import MEDIA_ROOT, D


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
        with open(os.path.join(MEDIA_ROOT + '/' + username + '/' + 'category', filename), 'wb') as fp:
            for chunk in img.chunks():
                fp.write(chunk)
        url = D + '/media/' + username + '/category/' + filename
        result = {'code': 200, 'url': url}
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})


class CategoryView(APIView):
    mongo = Mongo()
    col = mongo.col('article', 'category')
    a_col = mongo.col('article', 'article')
    u_col = mongo.col('user', 'user')

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.GET.get('user_id', None)
            user = self.u_col.find_one({"_id": ObjectId(user_id)})
            if user:
                if user['role'] == 100:
                    category = self.col.find()
                else:
                    category = self.col.find({"author": ObjectId(user_id)})
                a = []
                for i in category:
                    i['author_name'] = self.u_col.find_one({"_id": ObjectId(i['author'])})['username']
                    a.append(i)
                return Response({'code': 200, 'msg': '成功', 'data': json_util.dumps(a)})
            else:
                return Response({'code': 400, 'msg': '用户验证失败', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def post(self, request, *args, **kwargs):
        try:
            user = json.loads(request.body)['user']
            if user:
                form = json.loads(request.body)['form']
                if self.col.find_one({'name': form['name'], 'author': ObjectId(user['_id']['$oid'])}):
                    return Response({'code': 401, 'msg': '分类名已存在', 'data': {}})
                category = {
                    'name': form['name'],
                    'thumbnail': form['thumbnail'],
                    'desc': form['desc'],
                    'author': ObjectId(form['author']),
                    'create_date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
                    'change_date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
                    'private': form['private'],
                }
                x = self.col.insert(category)
                re = self.col.find_one({"_id": ObjectId(x)})
                re['author_name'] = user['username']
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
                category = json.loads(put.get('category'))
                _id = category.pop('_id')['$oid']
                author = self.col.find_one({"_id": ObjectId(_id)})['author']
                category['author'] = ObjectId(author)
                category.update({'change_date': time.strftime('%Y-%m-%d', time.localtime(time.time()))})
                # if self.col.find_one({'name': category['name'], 'author': ObjectId(author)}):
                #     return Response({'code': 401, 'msg': '分类名已存在', 'data': {}})
                self.col.update({"_id": ObjectId(_id)}, category)
                self.a_col.update_many({'category': ObjectId(_id)}, {'$set': {'private': category['private']}})
                return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
            else:
                return JsonResponse({'code': 400, 'msg': '用户验证失败！', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})

    def delete(self, request, *args, **kwargs):
        try:
            delete = QueryDict(request.body)
            _id = delete.get('_id')
            user_id = delete.get('user_id')
            author_id = self.u_col.find_one({"username": delete.get('author')})['_id']
            user = self.u_col.find_one({"_id": ObjectId(user_id)})
            article = self.a_col.find_one({"category": ObjectId(_id)})
            if article:
                return JsonResponse({'code': 500, 'msg': '分类非空', 'data': {}})
            if user['role'] == 100:
                self.col.delete_many({"_id": ObjectId(_id), "author": ObjectId(author_id)})
            else:
                self.col.delete_many({"_id": ObjectId(_id), "author": ObjectId(user_id)})
            return JsonResponse({'code': 200, 'msg': '成功', 'data': {}})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e), 'data': {}})
