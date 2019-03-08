"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.db import router
from django.urls import path, re_path
from django.urls import include
from django.conf.urls import url
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from MxShop.settings import MEDIA_ROOT
from goods.view_base import GoodsListView1, GoodsListView2, GoodsListView3, GoodsListView4
from goods.views import GoodsListViewSet, CategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewset, AddressViewset

# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })

router = DefaultRouter()

router.register(r'goods', GoodsListViewSet, base_name="goods")

router.register(r'categorys', CategoryViewSet, base_name="categorys")

router.register(r'codes', SmsCodeViewSet, base_name="codes")

router.register(r'users', UserViewSet, base_name="users")

router.register(r'userfavs', UserFavViewSet, base_name="userfavs") #收藏

router.register(r'messages', LeavingMessageViewset, base_name="messages") #留言

router.register(r'address', AddressViewset, base_name="address") #收货地址


urlpatterns = [
    path('docs/', include_docs_urls(title="小马杂货店API")),  # 自动生成文档
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('api-auth/', include('rest_framework.urls')),  #drf的登录url，配置之后会在drf的页面右上角出现登录的按钮
    re_path('^', include(router.urls)),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    path('api-token-auth/', views.obtain_auth_token),   # drf自带的token认证模式
    path('login/', obtain_jwt_token ),                  # jwt的认证借口
]