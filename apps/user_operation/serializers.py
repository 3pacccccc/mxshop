# -*- coding: utf-8 -*-
__author__ = 'ma'

import re

from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer
from MxShop.settings import REGEX_MOBILE


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


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')  #设置之后可以返回add_time并且在提交留言的时候不需要填写
    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", 'id', 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    #第二次做的时候记得验证fields里面字段的合法性
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')  # 设置之后可以返回add_time并且在提交留言的时候不需要填写

    province = serializers.CharField(required=True, label="省份", help_text="省份",
                                     error_messages={
                                         "blank":"省份不能为空",
                                     })

    city = serializers.CharField(required=True, label="城市", help_text="城市",
                                     error_messages={
                                         "blank":"城市不能为空",
                                     })

    district = serializers.CharField(required=True, label="区域", help_text="区域",
                                     error_messages={
                                         "blank":"区域不能为空",
                                     })

    address = serializers.CharField(required=True, label="地址", help_text="地址",
                                    error_messages={
                                        "blank": "地址不能为空",
                                    })

    signer_name = serializers.CharField(required=True, label="收货人", help_text="收货人",
                                    error_messages={
                                        "blank": "收货人不能为空",
                                    })

    signer_mobile = serializers.CharField(required=True, label="联系电话", help_text="联系电话",
                                        error_messages={
                                            "blank": "联系电话不能为空",
                                        }, max_length=11, min_length=11)

    def validate_signer_mobile(self, signer_mobile):
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError("手机号码非法， 请确认后重新输入")
        return signer_mobile

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", 'address',
                  'signer_name', 'add_time', 'signer_mobile')
