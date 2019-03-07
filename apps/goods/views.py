import rest_framework.views
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer, CategorySerializer
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    page_size = 12   #返回的商品个数
    page_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页
    继承mixins.ListModelMixin可以不用写get函数
    """
    queryset = Goods.objects.all().order_by("id")
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    # 设置filter的类为我们自定义的类
    # 过滤
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name','goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:商品分类列表数据
    继承mixins.RetrieveModelMixin之后可以获取某个商品的详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


