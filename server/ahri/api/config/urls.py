from django.urls import path
from . import bg_setting_views
from . import bug_views

app_name = 'setting'

urlpatterns = [
    path('bg_setting/', bg_setting_views.BGSettingView.as_view()),
    path('bug/', bug_views.BugView.as_view()),
]
