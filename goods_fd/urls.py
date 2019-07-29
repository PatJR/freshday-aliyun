from django.urls import path, re_path, include
from . import views
app_name = 'goods'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('goods/<str:goods_id>/', views.DetailView.as_view(), name='detail'),
    path('list/<str:type_id>/<str:page>/', views.ListView.as_view(), name='list'),
    path('page/<int:p>', views.pagedex, name='page'),
]