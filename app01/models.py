from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=32,verbose_name="用户名")
    emil = models.EmailField(max_length=32,verbose_name="邮箱")
    pwd = models.CharField(max_length=32,verbose_name="密码")

    roles = models.ForeignKey(to="Role",verbose_name="用户角色")

    def __str__(self):
        return self.name

class Role(models.Model):
    caption = models.CharField(max_length=32,verbose_name="角色")

    def __str__(self):
        return self.caption