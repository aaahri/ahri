from django.urls import path
from . import register_views
from . import login_views
from . import auth_views
from . import usermanage_views

app_name = 'auth'

urlpatterns = [
    path('register/', register_views.RegisterView.as_view()),
    path('login/', login_views.LoginView.as_view()),
    path('', auth_views.AuthView.as_view()),
    path('upload/', auth_views.upload),
    path('usermanage/', usermanage_views.UserManageView.as_view()),
]
