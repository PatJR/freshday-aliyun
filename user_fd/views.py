from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from user_fd.models import User, Address
from django.views.generic import View  # 使用视图类
from goods_fd.models import GoodsSKU  # UserInfoView
from order_fd.models import OrderGoods, OrderInfor
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # 加密身份令牌
from itsdangerous import SignatureExpired  # 加密失效异常
from freshday.settings import SECRET_KEY  # 使用django中setting.py 中的SECRET_KEY作为密钥
from user_fd.tasks import send_register_active_email
from django.contrib.auth import authenticate  # 用户认证
from django.contrib.auth import login  # 用户登陆
from django.contrib.auth import logout  # 用户退出
from django.contrib.auth.mixins import LoginRequiredMixin
from django_redis import get_redis_connection  # 获得可重用的连接字符串.即django-redis在settings中的配置
from django.core.paginator import Paginator
import re
import os
from django.core.mail import send_mail  # 发送邮件
from django.conf import settings
from django.contrib.auth.decorators import login_required
# """ 如果用户没有登录，会重定向到 settings.LOGIN_URL ，
# # 并传递绝对路径到查询字符串中。例如： /accounts/login/?next=/polls/3/ 。如果用户已经登录，则正常执行视图。"""

import time

# from django.conf import settings   # 同上导入setting.SECRET_KEY
# Create your views here.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freshday.settings')
# django.setup()
"""
用户管理可参见https://docs.djangoproject.com/en/2.1/topics/auth/default/
"""


def register(request):
    """显示注册页面"""
    # register_handle(request)
    return render(request, 'register.html')


def register_handle(request):
    print('excute++++++++++++++')

    # 进行注册处理
    # 接受数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    print(allow)
    # 进行数据校验
    # all()
    # 函数用于判断给定的可迭代参数iterable中的所有元素是否都为TRUE，
    # 如果是返回True，否则返回False。元素除了是0、空、None、False外都算True
    if not all([username, password, email]):
        # 数据不完整
        print('数据不完整')
        return render(request, 'register.html', {'errmsg': '数据不完整'})
    # 校验邮箱
    if not re.match(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+$", email):
        print('邮箱格式不正确')
        return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
    # 是否同意协议  ps : HTML check属性无指定的valu时 返回 on 或off
    if allow != 'on':
        print('请同意协议')
        return render(request, 'register.html', {'errmsg': '请同意协议'})
    # 校验用户名是否重复
    try:
        # 通过get()查询数据库中username
        print('通过get()查询数据库中')
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # 用户名不存在
        print('用户名不存在')
        user = None
    if user:
        # 用户名已经存在
        print('用户名已经存在')
        return render(request, 'register.html', {'errmsg': '用户名已存在'})
    # 进行业务处理, 进行用户注册
    # 模型类继承的AbstractUser的Manage的实例objects有创建用户方法返回模型实例对象
    user = User.objects.create_user(username=username, email=email, password=password)
    user.is_active = 0  # 0表示未激活,需要用过邮箱激活
    user.save()

    # 返回应答,跳转首页
    # 使用重定向函数redirect重定向页面
    print('重定向页面')
    return redirect(reverse('goods:index'))


class Register(View):

    def get(self, request):
        """显示注册页面"""
        # register_handle(request)
        return render(request, 'register.html')

    def post(self, request):
        print('excute++++++++++++++')

        # 进行注册处理
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        print(username, password, email, allow)
        # 进行数据校验
        # all()
        # 函数用于判断给定的可迭代参数iterable中的所有元素是否都为TRUE，
        # 如果是返回True，否则返回False。元素除了是0、空、None、False外都算True
        if not all([username, password, email]):
            # 数据不完整
            print('数据不完整')
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+$", email):
            print('邮箱格式不正确')
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        # 是否同意协议  ps : HTML check属性无指定的valu时 返回 on 或off
        if allow != 'on':
            print('请同意协议')
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        # 校验用户名是否重复
        try:
            # 通过get()查询数据库中username
            print('通过get()查询数据库中')
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            print('用户名不存在')
            user = None
        if user:
            # 用户名已经存在
            print('用户名已经存在')
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        # 进行业务处理, 进行用户注册
        # 模型类继承的AbstractUser的Manage的实例objects有创建用户方法返回模型实例对象
        print('save user information -------')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = 0  # 0表示未激活,需要用过邮箱激活
        user.save()
        print('save succed ------------')
        # 发送激活邮件，包含激活链接
        # 激活链接中需要包含用户的身份信息，并且要将身份信息进行加密
        # 加密用户的身份信息生成激活token
        # TimedJSONWebSignatureSerializer('密钥', 过期时间)
        # TimedJSONWebSignatureSerializer('secrkey', 3600)  密钥'secrkey'  过期时间3600秒也可以为None
        print('ready secret key========')
        serializer = Serializer(SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # dump()加密 ，返回byte类型数据
        print('token类型', type(token))
        token = token.decode()  # decode() 转换成字符串编码  byte类型数据前的b"" 会转为 b'不能作为URL参数
        print('secret key complete==========')
        # 发送邮件
        # ——————————————————————————————————————
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freshday.settings")
        reciver = [email, ]  # 收件人列表
        send_register_active_email.delay(reciver, username, token)  # celery task
        print('email send excute -----1111111111111111111----------')
        # ————————————————————————————————————————
        # 返回应答,跳转首页
        # 使用重定向函数redirect重定向页面
        print('重定向页面')
        return redirect(reverse('goods:index'))


class ActiveView(View):
    """用户激活"""

    def get(self, requset, token):
        """进行用户激活"""
        print('激活')
        # 进行解密，获取要激活的用户组信息
        serializer = Serializer(SECRET_KEY, 3600)
        try:
            print(type(token))
            print('前', token)
            # token = token.encode()  # 接收的是字符串，需要转成byte类型
            print('后', token)
            info = serializer.loads(token)  # 解密
            # 获取激活用户的ID
            user_id = info['confirm']
            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 转到登陆页面
            return redirect(reverse('user:login'))
        except SignatureExpired:
            return HttpResponse('激活链接已经过期')


class LoginView(View):

    def get(self, request):
        """显示登陆页面"""
        print('recive request GET')
        # 判断是否记住用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'  # 此为HTML <input> 的checked属性值为checked 规定此 input 元素首次加载时应当被选中。
        else:
            username = ''
            checked = ''
        # 使用模板
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        print('recive request POST')
        # 接受数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        print(username, password)
        # 校验数据
        # 使用内置函数all()判断可迭代参数中所有元素都为True,元素除了0，fals,none,空外都算TRUE
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})
        # 业务处理登陆校验
        user = authenticate(username=username,
                            password=password)  # 使用django内置用户认证，返回用户对象， django.contrib.auth.   AbstrickUser
        print(user)
        if user is not None:
            # 用户名密码正确
            print("用户名密码正确")
            if user.is_active:
                """用户已激活
                    记录用户登录状态
                    在请求中保存用户id和后端。这样用户就不会
                    必须对每个请求重新进行身份验证。请注意期间的数据集
                    用户登录时将保留匿名会话。保留到session
                """
                print('用户已激活')
                login(request, user)  # django.contrib.auth.
                # 获取登陆后所需要跳转的地址
                # 默认跳转到首页
                """Querydict 继承字典类型，同样继承get方法,dict.get(key, default=None)
                     key -- 字典中要查找的键。
                    default -- 如果指定键的值不存在时，返回该默认值值。
                    get不到next 返回 由reverse反向解析的url /goods/index/
                    注： 使用字典
                """
                # next 是 login_required装饰器， 如果用户没有登录，会重定向到 settings.LOGIN_URL ，
                # # 并传递绝对路径到查询字符串中。例如： /accounts/login/?next=/polls/3/ 。
                """如果next 为none 则使用默认值"""
                next_url = request.GET.get('next', default=reverse('goods:index'))

                # 跳转到next_url
                "redirect,会放回一个对象，该对象的父类继承于HttpResponse类所以可以调用该实例的方法和属性"
                response = redirect(next_url)
                # 判断是否记住用户名
                remenber = request.POST.get('remenber')

                if remenber == 'on':
                    # 记住用户名 max_age应该是一个秒数，或者为None(默认值) 如果cookie只持续到客户机浏览器会话的时间。
                    # 如果expires(有效期)未指定，则计算过期。
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response
            else:
                return render(request, 'login.html', {'errmsg': '账户未激活'})

        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


# /user/logout


class LogoutView(View):
    """退出登陆"""

    def get(self, request):
        """清除用户的session信息"""
        logout(request)  # 清除request.user 在session的数据

        # 跳转到首页
        return redirect(reverse('goods:index'))


class UserInfoView(LoginRequiredMixin, View):  # /user/
    """ 用户信息：
    LoginRequiredMxin 使用说明：
    使用基于类的视图时，可以使用 LoginRequiredMixin
    实现和 login_required# 相同的行为。"""

    def get(self, request):
        # 获取用户的个人信息
        user = request.user  # user 对象
        address = Address.objects.get_default_adress(user)  # 返回address对象
        # 获取用户的历史浏览记录   使用redis  list存储用户的历史纪录
        # -------------------------------------------------------------------------------
        import redis  # redis 的python原生包使用
        """实现Redis协议。这个抽象类为所有Redis命令提供了一个Python接口，并实现了Redis协议。
        连接和管道由此派生，实现如何将命令发送和接收到Redis服务器分配给:StrictRedis"""
        r = redis.Redis(host='localhost', port=6379, db=1)
        # ————————————————————————————————————————————————
        # 使用django-redis进行链接
        connect = get_redis_connection('default')  # 获取在settings.CACHE中的“default”的值
        history_key = 'history_%d' % user.id
        print(history_key)
        # 获取用户的最近浏览的5个商品的id
        # llrang key start stop   stop=-1 是list的末位
        sku_id = connect.lrange(history_key, 0, 4)  # sku_id  type:list [b'3', b'1']byte类型
        print("是", sku_id)
        # 从数据库中查询用户浏览的商品的具体信息
        """方法一"""
        # goods_li = GoodsSKU.objects.filter(id__in=sku_id)   # goods_li type : Queryset[ object1, object2 , ..]
        # # 其顺序与sku_id中顺序不一致
        # goods_res = []
        # # 依照sku_id的顺序对 对goods_li 中的对象列表重新排序
        # for a_id in sku_id:
        #     for goods in goods_li:
        #         if a_id == goods.id:
        #             goods_res.append(goods)
        """方法二"""
        goods_li = []
        for id in sku_id:
            print('ID是：', id)
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)
        # 组织上下文
        # print(goods_li)
        context = {'page': 'user',  # page=user  返回一个值 用于css样式在目录列表中显示
                   'user': user,
                   'address': address,
                   'goods_li': goods_li}
        return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin, View):  # /user/order/

    def get(self, request, page):
        # 获取用户的订单信息
        user = request.user
        orders = OrderInfor.objects.filter(user=user).order_by('-create_time')
        # 遍历获取订单信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_goods = OrderGoods.objects.filter(order=order)
            for order_good in order_goods:
                # 计算小计
                amount = order_good.count * order_good.price
                # 给order_good对象增加属性
                order_good.amount = amount
            # 给order增加订单状态名称
            order.status_name = OrderInfor.ORDER_STATUS[order.order_status]
            # 增加属性保存商品信息
            order.order_goods = order_goods

        # 分页
        paginator = Paginator(orders, 1)
        # 获取page页内容
        try:
            page = int(page)
        except Exception as e:
            print(e)
            page = 1

        if page > paginator.num_pages:  # 请求页面值大于总页数
            page = 1

        order_page = paginator.page(page)

        # todo:进行页码控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示最后5页
        # 4.其他情况，显示当前页的前2页，和后两页
        num_pages = paginator.num_pages  # 获取总页数
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page < 3:
            pages = range(1, 6)
        elif (num_pages - page) <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 组织上下文
        context = {
            'order_page': order_page,
            'pages': pages,
            'page': 'order',  # page=order  返回一个值 用于css样式在目录列表中显示
        }

        # request.user.is_authenticated  ,user是HttpRquest实例对象request的一个属性，其值是User的实例对象
        # 实例request的属性也会被传递至模板文件中例如 request.user
        return render(request, 'user_center_order.html', context)


class UserAddressView(LoginRequiredMixin, View):  # /user/address/
    def get(self, request):
        # 获取用户地址
        user = request.user
        # 调用封装在manage实例对象objects的自定义方法获取默认地址  无返回None
        address_default = Address.objects.get_default_adress(user)

        # page=address  返回一个值 用于css样式在目录列表中显示
        return render(request, 'user_center_address.html', {'page': 'address', 'address': address_default})

    def post(self, request):
        print('receive post')
        receiver = request.POST.get('receiver')
        postcode = request.POST.get('postcode')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        print(receiver)
        # 校验数据
        if not all([receiver, postcode, address, phone]):  # all()遍历可迭代变量，所有元素存在返回true 有一个为none 返回none
            # 数据不完整
            print('数据不完整')
            return render(request, 'user_center_address.html', {"errmsg": '数据不完整'})
        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            print('手机号码格式不正确')
            return render(request, 'user_center_address.html', {"errmsg": '手机格式不正确'})
        # 业务处理：地址添加
        # 如果用户已存在默认收货地址，添加的地址不作为默认收货地址，否则作为默认收货地址
        # 获取登录用户对应的user对象,request的user属性是User的实例对象
        user = request.user
        # 调用封装在manage实例对象objects的自定义方法获取默认地址  无返回None
        address_default = Address.objects.get_default_adress(user)

        if address_default:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user,  # user必须是User的实例对象
                               receiver=receiver,  # 收件人
                               address=address,  # 收货地址
                               postcode=postcode,  # 邮编
                               phone=phone,  # 手机号码
                               is_default=is_default,  # 是否默认
                               )
        # 返回应答，刷新地址页面
        return redirect(reverse('user:address'))
