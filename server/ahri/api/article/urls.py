from django.urls import path
from . import category_views
from . import article_views
from . import comment_views

app_name = 'article'

urlpatterns = [
    path('category/', category_views.CategoryView.as_view()),
    path('category/upload/', category_views.upload, name='upload1'),
    path('article/', article_views.ArticleView.as_view()),
    path('article/upload/', article_views.upload, name='upload2'),
    path('comment_manage/', comment_views.CommentView.as_view()),
]
