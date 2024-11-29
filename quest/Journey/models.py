from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#class Tip(models.Model):
    #title = models.CharField(max_length=200)
    #description = models.TextField()

    #def _str_(self):
        #return self.title
# Create your models here.

class ImpactStats(models.Model):
    pads_donated = models.PositiveIntegerField(default=0)
    girls_empowered = models.PositiveIntegerField(default=0)

class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_pads = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

class Goal(models.Model):
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    target_pads = models.IntegerField()
    current_pads = models.IntegerField(default=0)

class UserReward(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

class Reward(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    points_required = models.IntegerField()

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/')

    def __str__(self):
        return self.name
    
class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    badges = models.ManyToManyField(Badge, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

