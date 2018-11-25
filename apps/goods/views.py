from django.shortcuts import render
from django.views.generic import View
from rest_framework.pagination import PageNumberPagination

from goods.models import Goods, GoodsCategory
from django.http import HttpResponse, JsonResponse
import json
from django.core.serializers import serialize
from rest_framework.views import APIView
from goods.serializers import GoodsSerializer, CategorySerializer3, CategorySerializer2, CategorySerializer
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets, filters
from .filters import GoodsFilter
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


# class GoodsListView(View):
#     def get(self, request):
#         goods = Goods.objects.all()
#         json_data = serialize('json', goods)
#         json_data = json.loads(json_data)
#         return JsonResponse(json_data, safe=False)

#
# class GoodsListView(APIView):
#     def get(self, request, format=None):
#         goods = Goods.objects.all()
#         goods_serializer = GoodsSerializer(goods, many=True)
#         return Response(goods_serializer.data)

class GoodsPagination(PageNumberPagination):
    '''
    商品列表自定义分页
    '''
    # 默认每页显示的个数
    page_size = 12
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 100


class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = GoodsPagination
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filter_class = GoodsFilter
    # 对商品实现搜索功能， =name表示精确搜索
    search_fields = ('=name', 'goods_brief')
    ordering_fields = ('sold_num', 'add_time')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer