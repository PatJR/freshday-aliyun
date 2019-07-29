from django.db import models

class BaseModel(models.Model):
    '''创建抽象类，可以被继承，不会创建表'''

    #  auto_now_add 首次创建对象的时间戳，在第一次创建对象时自动添加日期和时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # auto_now 适用于最后更新时间戳， 每次保存对象时将时间保存为现在
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        # 说明是一个抽象类，不会创建表
        abstract = True
