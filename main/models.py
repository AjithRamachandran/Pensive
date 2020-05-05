from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from taggit.managers import TaggableManager
from django_countries.fields import CountryField

class Profile(models.Model):        
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    Bio = models.TextField(max_length=100, default="Hi, I am Using Pensive!")
    Country = CountryField(multiple=True)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Question(models.Model):
    QuestionId = models.AutoField(primary_key=True)
    OwnerUserId = models.ForeignKey(User, on_delete=models.CASCADE)
    Score = models.IntegerField(default=0)
    Title = models.CharField(max_length=100)
    Body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager() 


class Answer(models.Model):
    AnswerId = models.IntegerField(primary_key=True)
    OwnerUserId = models.ForeignKey(User, on_delete=models.CASCADE)
    ParentId = models.ForeignKey(Question, on_delete=models.CASCADE)
    Score = models.IntegerField(default=0)
    IsAcceptedAnswer = models.BooleanField(default='False')
    Body = models.TextField()

class Vote(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Score(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    Answer = models.ForeignKey(Answer, on_delete=models.CASCADE)