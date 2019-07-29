# ----------------------------------Django 测试脚本------------------------------
# import sys
# sys.path.insert(0, '../')
# sys.path.insert(0, '../apps')
# import os
# if not os.getenv('DJANGO_SETTINGS_MODULE'):
#     os.environ['DJANGO_SETTINGS_MODULE'] = 'freshday.settings'
# # 让django进行初始化设置
# import django
# django.setup()
# ----------------------------------------------------------------------------------
from celery import shared_task
from goods_fd.models import GoodsType, GoodsSKU, IndexGoodsBanner, IndexPromotionBanner, IndexGoodsTypeBanner
from django.template import loader, RequestContext,Context
from django.conf import settings
from django.shortcuts import render
import os


@shared_task
def generate_static_index_html():
    '''产生首页静态页面'''
    # 获取商品的种类信息
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    for tp in types:  # GoodsType
        print('type类型', type(tp))
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexGoodsTypeBanner.objects.filter(type=tp, display_type=1).order_by('index')
        print('image类型', image_banners)
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexGoodsTypeBanner.objects.filter(type=tp, display_type=0).order_by('index')
        print('title类型', title_banners)
        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        tp.image_banner = image_banners
        tp.title_banner = title_banners


    # 组织模板上下文
    context = {'types': types,
               'goods_banners': goods_banners,
               'promotion_banners': promotion_banners}

    # 使用模板
    # 1.加载模板文件,返回模板对象
    # temp = loader.get_template('static_index.html')
    static_index_html = loader.render_to_string('static_index.html', context)
    # 2.模板渲染
    # static_index_html = temp.render(context)
    str(static_index_html)
    # 生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static\\index.html')
    print(save_path)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(static_index_html)

if __name__ == '__main__':
    generate_static_index_html()