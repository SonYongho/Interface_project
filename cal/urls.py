from django.urls import re_path, path
from . import views

app_name = 'cal'
urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    re_path(r'^event/new/$', views.event_create, name='event_new'),
    path('event/detail/<int:event_id>/', views.event_detail, name='detail'),
	path('event/edit/<int:event_id>/', views.event_modify, name='event_edit'),
    path('event/delete/<int:event_id>/', views.event_delete, name='event_delete'),
]
