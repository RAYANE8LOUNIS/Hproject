from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('compose/', views.compose, name='compose'),
    path('sent/', views.sent, name='sent'),
    path('drafts/', views.drafts, name='drafts'),
    path('success/', views.send_success, name='send_success'),
    path('<int:pk>/', views.message_detail, name='message_detail'),
    path('<int:pk>/edit/', views.edit_draft, name='edit_draft'),
    path('<int:pk>/delete/', views.delete_message, name='delete_message'),
]
