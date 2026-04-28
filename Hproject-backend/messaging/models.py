from django.db import models
from django.contrib.auth.models import User
from organisation.models import Team


class Message(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
    ]

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE,
        related_name='received_messages'
    )
    subject = models.CharField(max_length=200)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f"{self.sender.username} → {self.team.name}: {self.subject}"

    @property
    def is_draft(self):
        return self.status == 'draft'

    @property
    def is_sent(self):
        return self.status == 'sent'
