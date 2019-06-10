"""ahri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.views.static import serve
from ahri.settings import MEDIA_ROOT

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("favicon.ico", RedirectView.as_view(url='static/favicon.ico')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    path('api/auth/', include('api.user.urls')),
    path('api/', include('api.index.urls')),
    path('api/', include('api.article.urls')),
    path('api/', include('api.config.urls')),
    path('api/db/', include('api.database.urls')),
    path('editor/', include('editor.ckeditor.urls')),
    # path('editor/', include('editor.ueditor.urls')),
    path('editor/', include('editor.wangeditor.urls')),
]
