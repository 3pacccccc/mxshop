# -*- coding: utf-8 -*-
__author__ = 'ma'

import re
from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode


User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        #验证手机是否注册
        if User.objects.filter(mobile=mobile).count() > 0:
            raise serializers.ValidationError("该用户已经存在")

        #验证手机号是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法，请确认后再输入")

        #验证发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile):
            raise serializers.ValidationError("请求过于频繁，请稍后再试")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    #help_text使得code在前端的显示名称的验证码
    code = serializers.CharField(required=True, max_length=4, min_length=4, help_text="验证码",
                                 error_messages={
                                     "required": "请输入验证码",
                                     "max_lenth": "您输入的验证码过长，请确认后输入！",
                                     "min_lenth": "您输入的验证码过短，请确认后输入！",
                                     "blank": "验证码不能为空"
                                 }, label="验证码", write_only=True)
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")],
                                     label="账号")

    password = serializers.CharField(
        style={"input_type": "password"}, label="密码",
        write_only=True
    )

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)

            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")


    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']

        return attrs

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user


    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = ('name', 'gender', 'birthday', 'email', 'mobile')

