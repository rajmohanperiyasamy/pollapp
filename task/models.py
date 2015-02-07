from django.db import models
    
class Task(models.Model):
    completed = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    
    
class Employees(models.Model):
    EmpId = models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile=models.CharField(max_length=20,blank=True)
    email=models.EmailField(max_length=254, blank=False, unique=True)
    country = models.CharField(max_length=100, blank=True)
    