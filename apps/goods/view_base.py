import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics

from .models import Goods
from .serializers import GoodsSerializer1, GoodsSerializer



class GoodsListView1(View):
    """
    最简单的一种返回json方式。
    优点：操作简单快捷
    缺点：在字段多的时候复杂，并且功能十分的有限
    """
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()
        for good in goods:
            json_dict = {}
            json_dict['name'] = good.name
            json_dict['category'] = good.category.name
            json_dict['market_price'] = good.market_price

            json_list.append(json_dict)

        return HttpResponse(json.dumps(json_list), content_type='application/json')


class GoodsListView2(View):
    """
    优点：可以一键直接序列化所有的数据
    缺点：对于有些字段如ImageField以及DatetimeField无法序列化
    """
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()
        for good in goods:
            json_dict = model_to_dict(good)
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list), content_type="application/json")


class GoodsListView3(View):
    """
    优点：可以一键序列化所有数据
    缺点：字段序列化定死的，要想重组的话非常麻烦
         images保存的是一个相对路径，我们还需要补全路径，而这些drf都可以帮助我们做到
    """
    def get(self, request):
        goods = Goods.objects.all()
        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)


class GoodsListView4(APIView):
    """
    通过drf的serializer和 APIView使得序列化变得更加简单
    """

    def get(self, request):
        goods = Goods.objects.all()
        goods_serializer = GoodsSerializer1(goods, many=True)
        return Response(goods_serializer.data)

    """
    验证传入数据的逻辑例子
    """
    def post(self, request, format=None):
        serializer = GoodsSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()   #sava会调用GoodsSerializer里面的create方法
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodsListView5(APIView):
    """
    功能还不够强大
    """
    def get(self, request):
        goods = Goods.objects.all()
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)


class GoodsListView6(mixins.ListModelMixin, generics.GenericAPIView):
    """
    商品列表页
    generic.py源码里面有很多类可以继承，功能很丰富
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StandardReslutsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'p'


class GoodsListView7(generics.ListAPIView):
    """
    商品列表页
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = StandardReslutsSetPagination