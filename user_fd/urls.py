from django.urls import path, re_path, include
from django.contrib.auth.decorators import login_required
# 如果用户没有登录，会重定向到 settings.LOGIN_URL ，
# 并传递绝对路径到查询字符串中。例如： /accounts/login/?next=/polls/3/ 。如果用户已经登录，则正常执行视图。
from . import views
app_name = 'user'
# 登陆验证,视图继承LoginRequiredMixin
urlpatterns = [

    path('', views.UserInfoView.as_view(), name='info'),
    path('order/<str:page>/', views.UserOrderView.as_view(), name='order'),
    path('address/', views.UserAddressView.as_view(), name='address'),
    path('register/', views.Register.as_view(), name='register'),
    path('active/<str:token>/', views.ActiveView.as_view(), name='active'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout')

]


 # 使用login_required装饰器
# urlpatterns = [
#
#     path('', login_required(views.UserInfoView.as_view()), name='info'),
#     path('order/', login_required(views.UserOrderView.as_view()), name='order'),
#     path('address/', login_required(views.UserAddressView.as_view()), name='address'),
#     path('register/', views.Register.as_view(), name='register'),
#     path('active/<str:token>/', views.ActiveView.as_view(), name='active'),
#     path('login/', views.LoginView.as_view(), name='login'),
#
# ]
