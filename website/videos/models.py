from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.



class Comment(models.Model):
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    comment = models.CharField(max_length=250, default = 'unavailable')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    picture = models.ImageField(null=True,upload_to='images')
    ratedUsers = models.ManyToManyField(User, blank = True, related_name='ratedUsersComment')
    def __str__(self):
        return self.comment[:30]
    class Meta:
        ordering =["-created"]

class Video(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    video = models.FileField(upload_to='videos')
    thumbnail = models.ImageField(upload_to='images')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    views = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, blank = True,null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    ratedUsers = models.ManyToManyField(User, blank = True, related_name='ratedUsersVideo' )
    def __str__(self):
        return self.title
    class Meta:
        ordering = ["-created"]


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile',on_delete=models.CASCADE)
    username = models.CharField(max_length=30, default = "Anonymous")
    picture = models.ImageField(upload_to='images', default = "media/images/defaultprofilepicture.png")
    description = models.CharField(max_length=50)
    videos = models.ManyToManyField(Video,blank=True)
    def __str__(self):
        return self.username
    class Meta:
        ordering = ["-username"]
