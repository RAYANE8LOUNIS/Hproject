from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'team', 'status', 'is_read', 'created_at', 'sent_at')
    list_filter = ('status', 'is_read', 'team')
    search_fields = ('subject', 'body', 'sender__username', 'team__name')
    readonly_fields = ('created_at', 'updated_at', 'sent_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'team')
