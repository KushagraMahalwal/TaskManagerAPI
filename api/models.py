from django.db import models
from django.conf import settings   # <-- use this


class TaskManager(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # <-- important
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    title = models.CharField(max_length=250)
    description = models.TextField()
    completed = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    