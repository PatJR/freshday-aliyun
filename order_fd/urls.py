from django.urls import path, re_path, include
from . import views
app_name = 'order'
urlpatterns = [
    # path('infor/', views.info, name='infor'),
    path('infor/', views.OrderPlaceView.as_view(),name='infor'),
    path('commit/', views.OrderCommitView.as_view(), name='commit'),
    path('pay/', views.OrderPayView.as_view(), name='pay'),
    path('check/', views.CheckPayView.as_view(), name='check'),
    path('comment/<str:order_id>', views.CommentView.as_view(), name='comment')
]