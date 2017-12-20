from django.db import models

# Create your models here.
class Host(models.Model):
    hostname = models.CharField(max_length=32,verbose_name="主机名")
    ip = models.GenericIPAddressField(protocol='both',verbose_name="IP")
    port = models.IntegerField(verbose_name='端口')


    def __str__(self):
        return self.hostname




from django.db import models

class Role(models.Model):
    title = models.CharField(verbose_name='角色标题',max_length=32)

    def __str__(self):
        return self.title

class Department(models.Model):
    caption = models.CharField(verbose_name='部门名称',max_length=23)
    def __str__(self):
        return self.caption


class UserInfo(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=32)
    email = models.CharField(verbose_name='邮箱',max_length=32)
    gender_choices = (
        (1,'男'),
        (2,'女'),
        (3,'少伟'),
    )
    gender = models.IntegerField(verbose_name='性别',choices=gender_choices)

    depart = models.ForeignKey(verbose_name="所属部门",to=Department)
    roles = models.ManyToManyField(verbose_name="扮演的角色", to=Role)