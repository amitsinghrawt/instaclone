# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models

# Create your models here.


class UserModel(models.Model):
    email = models.EmailField(null=False)
    username = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    password = models.CharField(max_length=40)

    created_on = models.DateTimeField(auto_now_add=True)
      # updated-on field
    updated_on = models.DateTimeField(auto_now=True)

class Seccion_token(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    last_request_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4()

class PostModel(models.Model):
    user = models.ForeignKey(UserModel)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=200)
    caption = models.CharField(max_length=200)
    category_post = models.CharField(max_length=200, default="others")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    has_liked = False


    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post=self))

    @property
    def comments(self):
        return CommentModel.objects.filter(post=self).order_by('-created_on')


class LikeModel(models.Model):
        user = models.ForeignKey(UserModel)
        post = models.ForeignKey(PostModel)
        created_on = models.DateTimeField(auto_now_add=True)
        updated_on = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
        user = models.ForeignKey(UserModel)
        post = models.ForeignKey(PostModel)
        comment_text = models.CharField(max_length=555)
        created_on = models.DateTimeField(auto_now_add=True)
        updated_on = models.DateTimeField(auto_now=True)

class swachh_bharat(models.Model):
        post = models.ForeignKey(PostModel)
        text = models.CharField(max_length=500)

class UpvoteModel(models.Model):
    user = models.ForeignKey(UserModel)
    comment = models.ForeignKey(CommentModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
