from django.urls import path, re_path, include
from . import views
app_name = 'cart'
urlpatterns = [
    path('add/', views.CartAddView.as_view(), name='add'),
    path('', views.CartInfoView.as_view(), name='info'),
    path('delete/', views.CartDeleteView.as_view(), name='delete'),
    path('update/', views.CartUpdateView.as_view(), name='update'),
]