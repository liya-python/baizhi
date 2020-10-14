from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from order.serializers import OrderModelSerializer


class OrderAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    """生成订单的视图"""
    queryset = Order.objects.filter(is_delete=False, is_show=True)
    serializer_class = OrderModelSerializer