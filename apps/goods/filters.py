# -*- coding: utf-8 -*-
__author__ = 'ma'

import django_filters
from django.db.models import Q

from .models import Goods

class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品过滤类
    """
    pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr="gte")
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr="lte")
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        # 查找第一类别下面的所有商品
        # return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot']
