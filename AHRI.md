# 请求方式：

#### GET请求：

```javascript
let self = this;
this.axios
    .get("http://127.0.0.1:9000/api/auth/", {
    params: {
        data: {
            username: {
                a: 1,
                b: 2
            },
            password: self.password
        }
    }
})
    .then(response => {
    if (response.data.code === 200) {
        console.log(response.data);
    } else {
        alert("failed");
    }
})
    .catch(response => {
    console.log(response);
});
```

```python
json.loads(request.GET.get('data')) # dist
```

#### POST请求：

```javascript
let self = this;
this.axios({
    url: "http://127.0.0.1:9000/api/auth/",
    method: "post",
    //发送格式为json
    data: JSON.stringify({
        form: { 
            username: self.username,
            password: self.password
        }
    }),
    headers: {
        "Content-Type": "application/json"
    }
}).then(
    function(response) {
        console.log(response.data);
    },
    function(response) {
        console.log(response.data);
    }
);
```

```python
form = json.loads(request.body)['form'] # dist
```

#### PUT请求：

```javascript
import Qs from "qs";
let self = this;
this.axios
    .put(
    "http://127.0.0.1:9000/api/category/",
    Qs.stringify({
        category: JSON.stringify(self.edit_area),
        user: JSON.stringify(self.user)
    })
)
    .then(response => {
    console.log(response.data);
    if (response.data.code === 200) {
        this.show = false;
        for (let i = 0; i < this.category.length; i++) {
            if (i.id == this.edit_area.id) {
                i = this.edit_area;
            }
        }
        msg(self.$t("lang.category.editsuccess"), "#2ecc71");
    } else if (response.data.code === 400) {
        msg(this.$t("lang.category.authFail"), "red");
    }
})
    .catch(response => {
    msg("未知错误..", "#FF9966");
    console.log(response);
});
```

```python
user = json.loads(put.get('user')) # dist
user['_id']['$oid'] # str
category = json.loads(put.get('category')) # dist
category['_id']['$oid'] # str
```

#### DELETE请求：

```javascript
let self = this;
this.axios
    .delete("http://127.0.0.1:9000/api/category/", {
    data: Qs.stringify({
        _id: val._id.$oid,
        user_id: self.user._id.$oid,
        author: val.author
    })
})
    .then(response => {
    if (response.data.code === 200) {
        for (let i = 0; i < this.category.length; i++) {
            if (this.category[i]._id == val._id) {
                this.category.splice(i, 1);
            }
        }
    } else {
        alert("failed");
    }
})
    .catch(response => {
    console.log(response);
});
```

```python
delete.get('_id') # str
delete.get('user_id') # str
delete.get('author') # str
```

# 全局API：

#### 0x0001	用户注册

###### GET	注册、获取邮箱验证码	/api/auth/register

```javascript
params: {
	email: "xxxx@xx.xx"
}
```

```python
email = request.GET.get('email', None) # str
```


```json
// 200成功
{'code': 200, 'msg': '成功', 'data': {'code': 'code', 'email': "xxxx@xx.xx"}}
// 400邮箱格式错误
{'code': 400, 'msg': '邮箱格式错误', 'data': {}}
// 401邮箱已存在
{'code': 401, 'msg': '邮箱已存在', 'data': {}}
// 500服务器错误
{'code': 500, 'msg': str(e), 'data': {}}
```

###### POST	提交用户信息	/api/auth/register

```javascript
data: JSON.stringify({
    form: {
        username: "username",
        password: "password",
        email: "xxxx@xx.xx"
    }
}),
```

```python
form = json.loads(request.body)['form'] # dist
```

```json
// 返回值
// 200成功
{'code': 200, 'msg': '成功', 'data': {}}
// 400用户名已存在
{'code': 401, 'msg': '用户名已存在', 'data': {}}
// 500服务器错误
{'code': 500, 'msg': str(e), 'data': {}}
```

#### 0x0002	用户登录

###### POST	登录	/api/auth/login

```javascript
data: JSON.stringify({
    form: {
        username: "username",
        password: "password" }
}),
```

```python
form = json.loads(request.body)['form'] # dist
```

```json
// 200成功
{'code': 200, 'msg': 'success', 'data': json_util.dumps(user)}
// 400用户名或密码错误
{'code': 400, 'msg': '用户名或密码错误', 'data': {}}
// 500服务器错误
{'code': 500, 'msg': str(e), 'data': {}}
```

#### 0x0003	分类管理	/api/category

###### GET	获取分类

```javascript
params: {
    user_id: self.user._id.$oid
}
```

```python
user_id = request.GET.get('user_id', None) # str
```

```json
{'code': 200, 'msg': '成功', 'data': json_util.dumps(a)}
{'code': 400, 'msg': '用户验证失败', 'data': {}}
{'code': 500, 'msg': str(e), 'data': {}}
```

###### POST	添加分类

```javascript
data: JSON.stringify({
    form: self.edit_area,
    user: self.user
})
```

```python
user = json.loads(request.body)['user'] # dist
form = json.loads(request.body)['form'] # dist
```

```json
{'code': 401, 'msg': '分类名已存在', 'data': {}}
{'code': 200, 'msg': '成功', 'data': json_util.dumps(re)}
{'code': 400, 'msg': '用户验证失败！', 'data': {}}
{'code': 500, 'msg': str(e), 'data': {}}
```

###### PUT	更改分类

```javascript
Qs.stringify({
    category: JSON.stringify(self.edit_area),
    user: JSON.stringify(self.user)
})
```

```python
put = QueryDict(request.body)
user = json.loads(put.get('user')) # dist
category = json.loads(put.get('category')) # dist
```

```json
{'code': 401, 'msg': '分类名已存在', 'data': {}}
{'code': 200, 'msg': '成功', 'data': {}}
{'code': 400, 'msg': '用户验证失败！', 'data': {}}
{'code': 500, 'msg': str(e), 'data': {}}
```
###### DELETE	删除分类

```javascript
data: Qs.stringify({
    _id: val._id.$oid,
    user_id: self.user._id.$oid,
    author: val.author
})
```

```python
delete = QueryDict(request.body)
_id = delete.get('_id') # str
user_id = delete.get('user_id') # str
delete.get('author') # str
```

```json
{'code': 200, 'msg': '成功', 'data': {}}
{'code': 500, 'msg': str(e), 'data': {}}
```

#### 0x0004	文章管理	/api/article
###### GET	获取文章

```javascript
// 全部文章
params: {
    user_id: self.user._id.$oid
}

// 单个文章
params: {
    _id: id
}
```

```python
request.GET.get('user_id', None) # str

request.GET.get('_id') # str
```

```json
{'code': 200, 'msg': 'success', 'data': json_util.dumps(article)}
{'code': 500, 'msg': str(e), 'data': {}}

{'code': 200, 'msg': '成功', 'data': json_util.dumps(a)}
{'code': 400, 'msg': '用户验证失败', 'data': {}}
{'code': 500, 'msg': str(e), 'data': {}}
```

###### POST	添加文章

```javascript
data: JSON.stringify({
    article: self.article,
    user: self.user
})
```

```python
user = json.loads(request.body)['user'] # dist
article = json.loads(request.body)['article'] # dist
```

```json
{'code': 401, 'msg': '文章标题重复', 'data': {}}
{'code': 200, 'msg': '成功', 'data': json_util.dumps(re)}
{'code': 400, 'msg': '用户验证失败！', 'data': {}}
{'code': 500, 'msg': str(e), 'data': {}}
```

###### PUT	更改文章

```javascript
Qs.stringify({
    article: JSON.stringify(self.article),
    user: JSON.stringify(self.user)
})
```

```python
put = QueryDict(request.body)
user = json.loads(put.get('user')) # dist
article = json.loads(put.get('article')) # dist
```

```json
{'code': 401, 'msg': '文章标题重复', 'data': {}}
{'code': 200, 'msg': '成功', 'data': {}}
{'code': 400, 'msg': '用户验证失败！', 'data': {}}
{'code': 500, 'msg': str(e), 'data': {}}
```
###### DELETE	删除文章

```javascript
data: Qs.stringify({
    _id: val.$oid
})
```

```python
delete = QueryDict(request.body)
_id = delete.get('_id') # str
```

```json
{'code': 200, 'msg': '成功', 'data': {}}
{'code': 500, 'msg': str(e), 'data': {}}
```
#### 0x0004	评论管理	/api/comment_manage
###### GET	获取评论

```javascript
params: {
    user_id: self.user._id.$oid
}
```

```python
user_id = request.GET.get('user_id', None) # str
```

```json
{'code': 200, 'msg': '成功', 'data': json_util.dumps(a)}
{'code': 400, 'msg': '用户验证失败', 'data': {}}
{'code': 500, 'msg': str(e), 'data': {}}
```

###### DELETE	删除评论

```javascript
data: Qs.stringify({
    _id: val.$oid
})
```

```python
delete = QueryDict(request.body)
_id = delete.get('_id') # str
```

```json
{'code': 200, 'msg': '成功', 'data': {}}
{'code': 500, 'msg': str(e), 'data': {}}
```

