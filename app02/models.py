from django.db import models

# Create your models here.
class Host(models.Model):
    hostname = models.CharField(max_length=32,verbose_name="主机名")
    ip = models.GenericIPAddressField(protocol='both',verbose_name="IP")
    port = models.IntegerField(verbose_name='端口')


    def __str__(self):
        return self.hostname