from django.contrib.auth.models import AbstractUser
from django.db import models



class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name="workers")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "urgent", "Urgent"
        HIGH = "high", "High"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True, related_name="tasks")
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    def __str__(self):
        return self.name
