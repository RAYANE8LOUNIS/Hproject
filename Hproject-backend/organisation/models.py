from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    specialisation = models.CharField(max_length=200, blank=True)
    leader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='led_departments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def team_count(self):
        return self.teams.count()


class TeamType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('restructured', 'Restructured'),
        ('disbanded', 'Disbanded'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    purpose = models.TextField(blank=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teams'
    )

    team_type = models.ForeignKey(
        TeamType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teams'
    )

    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_teams'
    )

    members = models.ManyToManyField(
        User,
        related_name='teams',
        blank=True
    )

    slack_channel = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    code_repository = models.URLField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Dependency(models.Model):
    upstream_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='upstream_dependencies'
    )
    downstream_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='downstream_dependencies'
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('upstream_team', 'downstream_team')

    def __str__(self):
        return f"{self.upstream_team} → {self.downstream_team}"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50)
    object_id = models.IntegerField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name}"