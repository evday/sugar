from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=32,verbose_name="用户名")

class Role(models.Model):
    caption = models.CharField(max_length=32,verbose_name="角色")