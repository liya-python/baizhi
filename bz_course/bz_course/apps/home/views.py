# Create your views here.
from rest_framework.generics import ListAPIView

from bz_course.settings.constanst import BANNER_LENGTH
from home.models import Banner, Nav
from home.serializers import BannerModelSerializer, NavModelSerializer


class BannerListAPIView(ListAPIView):
    '''
    轮播图
    '''
    queryset = Banner.objects.filter(is_delete=False,is_show=True).order_by('-id')[:BANNER_LENGTH]
    serializer_class = BannerModelSerializer

class NavListAPIView(ListAPIView):
    '''
    导航栏
    '''
    queryset = Nav.objects.filter(is_delete=False, is_show=True).order_by('-id')
    serializer_class = NavModelSerializer