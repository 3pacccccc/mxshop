# -*- coding: utf-8 -*-
__author__ = 'ma'

from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from .models import UserFav
from goods.serializers import GoodsSerializer

class UserFavDetailSerializer(serializers.ModelSerializer):
    """用户收藏详情"""
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                # message的信息可以自定义
                message="已经收藏"
            )
        ]
        model = UserFav
        fields = ("user", "goods", "id")