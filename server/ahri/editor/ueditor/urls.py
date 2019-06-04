from . import views
from . import page_views
from django.urls import path
from django.conf import settings

app_name = 'ueditor'

urlpatterns = [
    path("ueditor/", page_views.hello),
    path("ueditor/upload/", views.UploadView.as_view(), name='upload')
]

if hasattr(settings, "UEDITOR_UPLOAD_PATH"):
    urlpatterns += [
        path("f/<filename>", views.send_file, name='send_file')
    ]
