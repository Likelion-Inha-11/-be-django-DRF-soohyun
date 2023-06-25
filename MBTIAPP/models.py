from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

#아이디 / 비밀번호 / 닉네임 / MBTI / 회원가입 / 

# Create your models here.

#회원가입

class Profile(AbstractUser):
    nickname = models.CharField(max_length=15);
    user_mbti = models.CharField(max_length=4);

    def __str__(self):
        return self.nickname
    
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    
class Post(models.Model):
    title =models.CharField(max_length=50)
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,default=1)
    content = models.TextField()
    categories = models.ManyToManyField(Category)


    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    content = models.CharField(max_length=150)

    def __str__(self):
        return self.content

