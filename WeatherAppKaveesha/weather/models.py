from django.db import models

# Create your models here.
class Location(models.Model):
    city=models.CharField(max_length=100,default="Unassigned",unique=True)
    
class User(models.Model):
    email_id = models.EmailField(unique=True)
    location=models.ForeignKey(Location, on_delete=models.CASCADE)
