from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


from .models import UserFav
from .serializers import UserFavSerializer, UserFavDetailSerializer
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.

class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    用户收藏
    """
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return UserFavDetailSerializer
    #
    #     elif self.action == "create":
    #         return UserFavSerializer
    #     return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


