from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('<int:team_id>/', views.team_detail, name='team_detail'),
    path('<int:team_id>/email/', views.email_team, name='email_team'),
    path('<int:team_id>/schedule/', views.schedule_meeting, name='schedule_meeting'),
]