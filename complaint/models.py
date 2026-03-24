from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Complaint(models.Model):
    username=models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    student_class = models.CharField(max_length=20)
    category = models.CharField(max_length=50,)