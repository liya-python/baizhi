from django.db import models

# Create your models here.
from home.baseModel import BaseModel


class Banner(BaseModel):
    """轮播图模型"""
    title = models.CharField(max_length=200, verbose_name="标题")
    img = models.ImageField(upload_to='banner', max_length=255, verbose_name="轮播图图片")
    class Meta:
        db_table = "bz_banner"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Nav(BaseModel):
    POSITION_OPTION = (
        (1, "顶部导航"),
        (2, "底部导航"),
    )
    title = models.CharField(max_length=200, verbose_name="标题")
    position = models.IntegerField(choices=POSITION_OPTION, default=1)
    is_site = models.BooleanField(default=False, verbose_name="是否是外部网址")

    class Meta:
        db_table = "bz_nzv"
        verbose_name = "导航栏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title