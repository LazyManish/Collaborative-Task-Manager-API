from django.db import models
from django.contrib.auth.models import User
from group.models import Group

# Create your models here.


class TaskModel(models.Model):

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('completed','Completed')
    ]

    title = models.CharField(max_length=50, null= False, blank=False)
    description = models.TextField()
    due_date = models.DateTimeField(auto_now_add=False, auto_now= False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=15)
    assigned_to = models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete= models.CASCADE, related_name="tasks", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} of group {self.group}"
    

