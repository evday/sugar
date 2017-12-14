from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class StarkConfig(AppConfig):
    name = 'stark'

    #设置启动文件，参考admin
    def ready(self):
        autodiscover_modules('stark',)

