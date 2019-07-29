from celery import Celery
import os
"""设置celery实例"""
# ----------------------------------------------------------------------------

"""为celery模块设置默认的Django settings 模块
    避免始终将settings 模块传递给celery程序
"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freshday.settings')

"""创建一个Celery的实例
参数
main (str):主模块的名称，如果运行为“_main__”。这用作自动生成任务名称的前缀。
目前没找到什么影响，就是该实例的一个名字"""
app = Celery('freshady')
""" namespace = 'CELERY' 所有的celery有关系的配置 键  都应有一个  CELERY_  的前缀
    目的是防止与DJANGO 的 settings的配置重叠
    将配置导入
"""
app.config_from_object('django.conf:settings', namespace='CELERY')

""" 从所有已注册的Django应用程序配置中加载任务模块 """
app.autodiscover_tasks()