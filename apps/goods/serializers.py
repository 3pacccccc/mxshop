# -*- coding: utf-8 -*- 
__author__ = 'ma'

from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsImage


class GoodsSerializer1(serializers.Serializer):
    """
    缺点：需要自己一个一个添加字段
    注意：ImageField会自动补全路径，但是需要在setting中设置好MEDIA_URL = '/media/'
    """
    name = serializers.CharField(required=True, max_length=100)
    click_num = serializers.IntegerField(default=0)
    goods_front_image = serializers.ImageField()

    def create(self, validated_data):
        return Goods.objects.create(**validated_data)


class CategorySerializer3(serializers.ModelSerializer):
    """
    三级类目序列化
    """
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    """
    二级类目序列化
    """
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    一级类目序列化
    """
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image", )


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    #images 跟model里面的relate_name保持一致
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"






