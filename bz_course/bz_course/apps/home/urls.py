from django.urls import path

from home import views

urlpatterns = [
    path('banners/',views.BannerListAPIView.as_view()),
    path('nav/',views.NavListAPIView.as_view())
]