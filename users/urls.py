from sched import scheduler
from django.urls import path, re_path
from .views import signup, profile, ProfileUpdateView, scheduler, member, follow
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from board.views import base_views

app_name = 'users'

urlpatterns = [
    path('', login_required(base_views.index), name='index'), # '/' 에 해당되는 path
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('member/', member, name='member'),
    re_path(r'^profile/(?P<pk>[0-9]+)/$', profile, name='profile'),
    re_path(r'^profile_update/$', login_required(ProfileUpdateView.as_view()), name='profile_update'),
    path('<str:username>/follow/', follow, name="follow"),
]
