
from django.urls import path
from . import views

urlpatterns = [
    path('ckeditor/', views.hello),
    path('ckeditor/upload/', views.upload),
]
