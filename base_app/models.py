from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username
    



class Event(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location_name = models.CharField(max_length=100)
    slots_limit = models.PositiveIntegerField()
    slots_available = models.PositiveIntegerField()
    registered_users = models.ManyToManyField(UserProfile, blank=True)

    def __str__(self):
        return self.title



