from django.db import models
from django.db.models.fields import CharField
from django.utils import timezone
from django.contrib.auth.models import User
from autoslug import AutoSlugField

TASK_STATUS = {
    ("created", "created"),
    ("assigned", "assigned"),
    ("completed", "completed")
}

def assign_sequences(task):
    if task.d_tasks.all().count() > 0:
        max_sequence = task.d_tasks.all().order_by('-sequence').first().sequence
    else:
        max_sequence = 0
    task.sequence = 1 + max_sequence
    task.save()
    return (max_sequence + 1)

class Task(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="reporter", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey("Team", related_name="assignee", on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    project = models.ForeignKey('Project', related_name="task_project", on_delete=models.CASCADE, null=True)
    d_tasks = models.ManyToManyField('self', symmetrical=False, blank=True)
    sequence = models.IntegerField(default=0, null=True, blank=True)
    completion_time = models.IntegerField()
    status = models.CharField(max_length=30, choices=TASK_STATUS, default="created", blank=True)

    def __str__(self):
        return self.name + " (" + self.project.name + ")"
    
    def save(self):
        super().save()
        this_project = self.project
        this_project.tasks.add(self)
        # assign_priority(self)
        return 



class Project(models.Model):
    name = models.CharField(max_length=50, null=True)
    start_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tasks = models.ManyToManyField('Task', related_name="sub_tasks", blank=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name + " (" + self.created_by.username + ")"

class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, blank=True)
    assigned_tasks = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    pending_tasks = models.ManyToManyField("Task", related_name="team_pending_tasks", blank=True)
    is_available = models.BooleanField(default=True,blank=True)

    def __str__(self):
        return self.name