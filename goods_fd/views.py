from django.shortcuts import render, reverse, redirect
from django.http import HttpRequest
from django.views.generic import View
from django.core.cache import cache  # 缓存
from django.core.paginator import Paginator
from goods_fd.models import GoodsType, GoodsSKU, IndexGoodsBanner, IndexPromotionBanner, IndexGoodsTypeBanner
from django_redis import get_redis_connection
from order_fd.models import OrderGoods
from django.template import loader
from django.conf import settings
import os

# Create your views here.

class IndexView(View):
    def get(self, request):
        """显示首页"""
        # 尝试从缓存中获取数据
        context = cache.get('index_page_data')
        print(context)
        if context is None:
            print('缓存中没有数据')
            # 缓存中没有数据
            # 获取商品的种类信息
            types = GoodsType.objects.all()
            # 获取首页轮播商品信息
            goods_banner = IndexGoodsBanner.objects.all()
            print(goods_banner)
            # 获取首页促销活动信息
            promotion_banner = IndexPromotionBanner.objects.all()
            # 获取首页分类商品展示信息
            for type in types:  # GoodType
                print('获取type种类首页分类商品的图片信息')
                print(type)
                # 获取type种类首页分类商品的图片信息
                image_banner = IndexGoodsTypeBanner.objects.filter(type=type, display_type=1).order_by('index')
                print(image_banner)
                # 获取type种类首页分类商品的文字信息
                title_banner = IndexGoodsTypeBanner.objects.filter(type=type, display_type=0).order_by('index')
                print(title_banner)
                # 动态给type对象增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
                type.image_banner = image_banner
                print(type.image_banner)
                type.title_banner = title_banner
                print(type.title_banner)
            context = {'types': types,
                       'goods_banners': goods_banner,
                       'promotion_banners': promotion_banner}
            # 设置缓存
            print('设置缓存')
            #             key             value   timeout
            cache.set('index_page_data', context, 3600)
            # # 写静态文件
            # static_index_html = loader.render_to_string('static_index.html', context)
            # save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
            # with open(save_path, 'w', encode('utf-8')) as f:
            #     f.write(static_index_html)
        # 获取用户购物车中的商品数目
        user = request.user
        cart_count = 0
        if user.is_authenticated:
            # 用户已登陆
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

        # 组织模板上下文
        context.update(cart_count=cart_count)
        # 使用模板
        print(context)
        return render(request, 'index.html', context)


# /goods/商品id
class DetailView(View):
    '''详情页'''

    def get(self, request, goods_id):
        '''显示详情页'''
        print("详情页面")
        try:
            sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            print("商品不存在")
            return redirect(reverse('goods:index'))

        # 获取商品的分类信息
        types = GoodsType.objects.all()

        # 获取商品的评论信息
        sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')

        # 获取新品信息
        new_skus = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]

        # 获取同一个SPU的其他规格商品
        same_spu_skus = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=goods_id)

        # 获取用户购物车中商品的数目
        user = request.user
        cart_count = 0
        if user.is_authenticated:
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

            # 添加用户的历史记录
            conn = get_redis_connection('default')
            history_key = 'history_%d' % user.id
            # 移除列表中的goods_id redis-py文档方法：有记录移除，无记录不操作
            conn.lrem(history_key, 0, goods_id)
            # 把goods_id插入到列表的左侧
            conn.lpush(history_key, goods_id)
            # 只保存用户最新浏览的5条信息
            conn.ltrim(history_key, 0, 4)

        # 组织模板上下文
        context = {'sku': sku,
                   'types': types,
                   'sku_orders': sku_orders,
                   'new_skus': new_skus,
                   'same_spu_skus': same_spu_skus,
                   'cart_count': cart_count}

        # 使用模板
        return render(request, 'detail.html', context)


# 种类id 页码 排序方式
# restful api -> 请求一种资源
# /list?type_id=种类id&page=页码&sort=排序方式
# /list/种类id/页码/排序方式
# /list/种类id/页码?sort=排序方式
class ListView(View):
    '''列表页'''

    def get(self, request, type_id, page):
        '''显示列表页'''
        # 获取种类信息
        try:
            type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            # 种类不存在
            return redirect(reverse('goods:index'))

        # 获取商品的分类信息
        types = GoodsType.objects.all()

        # 获取排序的方式 # 获取分类商品的信息
        # sort=default 按照默认id排序
        # sort=price 按照商品价格排序
        # sort=hot 按照商品销量排序
        sort = request.GET.get('sort')

        if sort == 'price':
            skus = GoodsSKU.objects.filter(type=type).order_by('price')
        elif sort == 'hot':
            skus = GoodsSKU.objects.filter(type=type).order_by('-sales')
        else:
            sort = 'default'
            skus = GoodsSKU.objects.filter(type=type).order_by('-id')

        # 对数据进行分页       object_list  per_page
        paginator = Paginator(skus, 3)

        # 获取第page页的内容
        try:                 # 如果page大于或者非int类型paginator都会返回第一页
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        skus_page = paginator.page(page)

        # todo: 进行页码的控制，页面上最多显示5个页码

        # 获取新品信息
        new_skus = GoodsSKU.objects.filter(type=type).order_by('-create_time')[:2]

        # 获取用户购物车中商品的数目
        user = request.user
        cart_count = 0
        if user.is_authenticated:
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

        # 组织模板上下文
        context = {'type': type,            # 商品种类
                   'types': types,          # 商品种类分类
                   'skus_page': skus_page,
                   'new_skus': new_skus,
                   'cart_count': cart_count,
                   'sort': sort}

        # 使用模板
        print(sort)
        return render(request, 'list.html', context)


def pagedex(request,p):

    g = GoodsSKU.objects.all()

    paginator = Paginator(g,1)
    page = paginator.get_page(p)

    return render(request, 'pagetest.html', {'page': page})
