from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('organisation/', include('organisation.urls')),
    path('teams/', include('teams.urls')),
    path('messaging/', include('messaging.urls')),
    path('schedule/', include('schedule.urls')),
    path('reports/', include('reports.urls')),
    path('datavis/', include('datavis.urls')),
]