from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from goods_fd.models import GoodsSKU
from django_redis import get_redis_connection
from django.contrib.auth.mixins import LoginRequiredMixin
import time
# Create your views here.
# 添加商品到购物车:
# 1）请求方式，采用ajax post
# 如果涉及到数据的修改(新增，更新，删除), 采用post
# 如果只涉及到数据的获取，采用get
# 2) 传递参数: 商品id(sku_id) 商品数量(count)


# ajax发起的请求都在后台，在浏览器中看不到效果
# /cart_fd/add
class CartAddView(View):
    '''购物车记录添加'''
    def post(self, request):
        '''购物车记录添加'''
        print('收到post')
        start = time.time()
        user = request.user
        if not user.is_authenticated:
            # 用户未登录
            return JsonResponse({'res':0, 'errmsg':'请先登录'})

        # 接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        ptime = time.time()
        print('接收数据耗时', ptime-start)
        # 数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 校验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            return JsonResponse({'res':2, 'errmsg':'商品数目出错'})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res':3, 'errmsg':'商品不存在'})
        vtime = time.time()
        print('add校验耗时', vtime-ptime)
        # 业务处理:添加购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        # 先尝试获取sku_id的值 -> hget cart_key 属性
        # 如果sku_id在hash中不存在，hget返回None
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            # 累加购物车中商品的数目
            count += int(cart_count)

        # 校验商品的库存
        if count > sku.stock:
            return JsonResponse({'res':4, 'errmsg':'商品库存不足'})

        # 设置hash中sku_id对应的值
        # hset->如果sku_id已经存在，更新数据， 如果sku_id不存在，添加数据
        conn.hset(cart_key, sku_id, count)
        rtime = time.time()
        print('add存储redis耗时', rtime-vtime)
        # 计算用户购物车商品的条目数
        total_count = conn.hlen(cart_key)
        print('add总耗时',time.time()-start)
        # 返回应答
        print("返回应答")
        return JsonResponse({'res':5, 'total_count':total_count, 'message':'添加成功'})


# /cart_fd/
class CartInfoView(LoginRequiredMixin, View):
    '''购物车页面显示'''
    def get(self, request):
        '''显示'''
        # 获取登录的用户
        user = request.user
        # 获取用户购物车中商品的信息
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        # {'商品id':商品数量, ...}
        cart_dict = conn.hgetall(cart_key)

        skus = []
        # 保存用户购物车中商品的总数目和总价格
        total_count = 0
        total_price = 0
        # 遍历获取商品的信息
        for sku_id, count in cart_dict.items():
            # 根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 计算商品的小计
            amount = sku.price*int(count)
            # 动态给sku对象增加一个属性amount, 保存商品的小计
            sku.amount = amount
            # 动态给sku对象增加一个属性count, 保存购物车中对应商品的数量
            sku.count = count.decode('utf8')       # 从redis 读取出来的是byte类型数据
            # 添加
            skus.append(sku)

            # 累加计算商品的总数目和总价格
            total_count += int(count)
            total_price += amount

        # 组织上下文
        context = {'total_count': total_count,
                   'total_price': total_price,
                   'skus': skus}

        # 使用模板
        return render(request, 'cart.html', context)


# 更新购物车记录
# 采用ajax post请求
# 前端需要传递的参数:商品id(sku_id) 更新的商品数量(count)
# /cart_fd/update
class CartUpdateView(View):
    '''购物车记录更新'''
    def post(self, request):
        '''购物车记录更新'''
        print('POST购物车记录更新')
        start = time.time()
        user = request.user
        if not user.is_authenticated:
            # 用户未登录
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})
        usertime = time.time()
        print('用户校验耗时',usertime-start)
        # 接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        print('更新', sku_id, count)
        recivertime = time.time()
        print('update接接收数据耗时', recivertime-usertime)
        # 数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 校验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})
        vtime = time.time()
        print('up 校验耗时', vtime-recivertime)
        # 业务处理:更新购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id

        # 校验商品的库存
        if count > sku.stock:
            return JsonResponse({'res':4, 'errmsg':'商品库存不足'})
        kt = time.time()
        print('up库存查询耗时', kt-vtime)
        # 更新
        conn.hset(cart_key, sku_id, count)

        # 计算用户购物车中商品的总件数 {'1':5, '2':3}
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)

        # 返回应答
        print('update返回应答')
        print('up 总耗时',time.time()-start)
        return JsonResponse({'res':5, 'total_count': total_count, 'message':'更新成功'})


# 删除购物车记录
# 采用ajax post请求
# 前端需要传递的参数:商品的id(sku_id)
# /cart_fd/delete
class CartDeleteView(View):
    '''购物车记录删除'''
    def post(self, request):
        '''购物车记录删除'''

        print('收到购物车记录删除POST')
        user = request.user
        if not user.is_authenticated:
            # 用户未登录
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        # 接收参数
        sku_id = request.POST.get('sku_id')

        # 数据的校验
        if not sku_id:
            return JsonResponse({'res': 1, 'errmsg': '无效的商品id%d'% sku_id})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res':2, 'errmsg':'商品不存在'})

        # 业务处理:删除购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id

        # 删除 hdel
        conn.hdel(cart_key, sku_id)

        # 计算用户购物车中商品的总件数 {'1':5, '2':3}
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)

        # 返回应答
        print("Delete返回应答")
        return JsonResponse({'res':3, 'total_count':total_count, 'message':'删除成功'})














