from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=25, null=False, blank=False)
    password = models.CharField(max_length=15, null=False, blank=False)
    firstName = models.CharField(max_length=25)
    lastName = models.CharField(max_length=25)
    groupID = models.CharField(max_length=10)

class Posts(models.Model):
    groupID = models.CharField(max_length=10, null=False, blank=False)
    postID = models.CharField(max_length=10, null=False, blank=False)
    poster = models.CharField(max_length=25, null=False, blank=False)
    post = models.CharField(max_length=100, null=False, blank=False)

class PostsReplies(models.Model):
    postID = models.CharField(max_length=10, null=False, blank=False)
    poster = models.CharField(max_length=25, null=False, blank=False)
    post = models.CharField(max_length=100, null=False, blank=False)
    
class Lists(models.Model):
    groupID = models.CharField(max_length=10, null=False, blank=False)
    listID = models.CharField(max_length=10, null=False, blank=False)
    listName = models.CharField(max_length=10, null=False, blank=False)
    
class ListItem(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    bought = models.BooleanField(default=False)
    list = models.ForeignKey(Lists, related_name='items', on_delete=models.CASCADE)