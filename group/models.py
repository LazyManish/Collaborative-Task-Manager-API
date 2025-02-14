from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):

    name = models.CharField(max_length=50, null= False, blank= False)
    description = models.TextField()
    group_id = models.CharField(max_length=10, unique=True)
    group_password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    

class Membership(models.Model):

    ROLE_CHOICES = [
        ('admin','Admin'),
        ('member','Member')
    ]

    group = models.ForeignKey(Group, on_delete= models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES, max_length=10, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} of {self.group} ({self.role})" 
    



