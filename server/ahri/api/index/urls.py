from django.urls import path
from . import index_views
from . import search_views
from . import read_views
from . import comment_views
from . import indexlast_views
from . import indexcate_views

app_name = 'index'

urlpatterns = [
    path('index/', index_views.IndexView.as_view()),
    path('read/', read_views.ReadView.as_view()),
    path('comment/', comment_views.CommentView.as_view()),
    path('index/search/', search_views.SearchView.as_view()),
    path('index/indexlast/', indexlast_views.IndexLastView.as_view()),
    path('index/indexcate/', indexcate_views.IndexCateView.as_view()),
]
