from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, \
    LeavingMessageSerializer, AddressSerializer
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    list:
        获取收藏列表
    retrieve:
        判断是否收藏商品
    create:
        收藏商品
    delete:
        删除收藏
    """
    queryset = UserFav.objects.all()
    # serializer_class = UserFavSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer

        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):

    """
    list:
        获取用户留言
    create:
        添加用户留言
    delete:
        删除用户留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)



class AddressViewset(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    update:
        更新收货地址
    create:
        创建收货地址
    delete:
        删除收货地址
    """
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
