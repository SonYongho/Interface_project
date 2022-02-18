
from django.contrib import admin
from django.urls import path, include
from cal import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('board/', include('board.urls')),
    path('', views.CalendarView.as_view(), name='index'), # '/' 에 해당되는 path
    path('cal/', include('cal.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
