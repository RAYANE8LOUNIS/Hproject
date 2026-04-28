from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('organisation/', include('organisation.urls')),
    path('teams/', include('teams.urls')),
    path('messages/', include('messaging.urls')),
    path('schedule/', include('schedule.urls')),
    path('datavis/', include('datavis.urls')),
    path('reports/', include('reports.urls')),
]