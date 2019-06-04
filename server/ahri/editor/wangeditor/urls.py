from . import views
from django.urls import path


urlpatterns = [
    path('wangeditor/', views.hello),
    path('wangeditor/upload/', views.upload),
]
