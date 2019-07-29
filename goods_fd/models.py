from django.db import models
from base_model import BaseModel
from django.contrib.auth.models import AbstractUser  # 导入用户抽象基类
from tinymce.models import HTMLField  # 导入富文本字段类型


# Create your models here.


class GoodsType(BaseModel):
    name = models.CharField(max_length=20, verbose_name='种类名称')
    logo = models.CharField(max_length=20, verbose_name='标识')
    # upload_to¶
    # 此属性提供了设置上载目录和文件名的方法，可以通过两种方式进行设置。
    # 在这两种情况下，该值都将传递给该 Storage.save()方法。
    # 文件将会从media_root/xxx上传
    image = models.ImageField(upload_to='type', verbose_name='商品类型图片')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name


class Goods(BaseModel):
    '''商品SPU模型类'''
    name = models.CharField(max_length=20, verbose_name='商品SPU名称')
    # 富文本类型：带有格式样式的文本   ，引入的非Django 类型
    detail = HTMLField(blank=True, verbose_name='商品详情')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name


class GoodsSKU(BaseModel):
    """商品SKU模型"""
    stasus_choice = (
        (0, '上线'),
        (1, '下线')
    )
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='商品种类')
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='商品SPU')
    name = models.CharField(max_length=20, verbose_name='商品名称')
    describe = models.CharField(max_length=256, verbose_name='商品简介')
    # max_digits 最大位数 ， decimal_places 小数部分位数
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    units = models.CharField(max_length=20, verbose_name='商品单位')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    image = models.ImageField(upload_to='goods_fd', verbose_name='商品图片')
    status = models.SmallIntegerField(default=1, choices=stasus_choice, verbose_name='商品状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'df_good_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class GoodsImage(BaseModel):
    image = models.ImageField(upload_to='GoodsSKU', verbose_name='图片路径')
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='商品')


    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class IndexGoodsBanner(BaseModel):
    """首页轮播商品展示模型类"""

    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name


class IndexGoodsTypeBanner(BaseModel):
    """首页分类商品展示模型类"""
    DISPLAY_TYPE = (
        (0, '标题'),
        (1, '图片')
    )
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='商品SKU')
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='商品类型')
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE, verbose_name='展示标识/类型')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    def __str__(self):
        return self.sku.name
    class Meta:
        db_table = 'df_index_type_gppds'
        verbose_name = '主页分类展示商品'
        verbose_name_plural = verbose_name


class IndexPromotionBanner(BaseModel):
    """首页促销活动模型类"""
    name = models.CharField(max_length=20, verbose_name='活动名称')
    url = models.URLField(verbose_name='活动链接')
    image = models.ImageField(upload_to='banner')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = '主页促销活动'
        verbose_name_plural = verbose_name
