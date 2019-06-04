from django.urls import path
from . import bg_setting

app_name = 'setting'

urlpatterns = [
    path('bg_setting/', bg_setting.BGSettingView.as_view()),
]
