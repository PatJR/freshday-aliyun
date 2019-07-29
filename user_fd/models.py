from django.db import models
from base_model import BaseModel
from django.contrib.auth.models import AbstractUser


# AbstractUser 是用户模型的抽象基类， 有用户名和密码 等字段
# Create your models here.

class User(AbstractUser, BaseModel):
    """用户模型类"""
    # 即使不继承该类在Django中也会自动创建auth_user数据表 若不需要，该模型类流程可简化，直接import
    # User.creatuser()创建用户，用法详情见django2.2 document 用户认证
    class Meta:
        db_table = 'df_user'  # 数据库表名
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class AddressManage(models.Manager):
    """继承模型管理器类"""
    def get_default_adress(self, user):
        """查询默认收货地址"""
        try:
            # 不能只get  user user_id是一个一对多的外键，会查询到多个对象引发异常
            address = self.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            address = None  # 不存在默认收货地址
        return address


class Address(BaseModel):
    # UTF-8 一个数字一个字节  一个英文一个字节，一个汉字3至4个字节
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='所属账户')
    receiver = models.CharField(max_length=20, verbose_name='收件人')  # char  定长型数据0-255 个字节 一个汉字4个字节
    address = models.CharField(max_length=256, verbose_name='收件地址')
    postcode = models.CharField(max_length=6, verbose_name='邮编')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    # 自定义一个模型管理器对象
    objects = AddressManage()

    class Meta:
        db_table = 'df_adress'
        verbose_name = '地址'
        verbose_name_plural = verbose_name
