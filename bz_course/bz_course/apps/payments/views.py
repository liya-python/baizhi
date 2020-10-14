import datetime
from django.shortcuts import render
# Create your views here.
# from datetime import datetime
import os
from alipay import AliPay
from django.conf import settings
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from bz_course.settings.constanst import IMAGE_SRC
from bz_course.settings.develop import BASE_DIR
from course.models import CourseExpire
from order.models import Order
from payments.models import UserCourse


class AliPayAPIView(APIView):

    def get(self, request):
        """生成支付链接"""

        order_number = request.query_params.get("order_number")

        # 获取应用的私钥
        # app_private_key_string = open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read(),
        # # 获取支付宝的公钥
        # alipay_public_key_string = open(os.path.join(BASE_DIR, "apps/payments/keys/alipay_public_key.pem")).read(),
        # print(alipay_public_key_string)

        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return Response({"message": "对不起，当前订单不存在"})

        # 支付的初始化参数
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG['appid'],  # 沙箱支付的应用id
            app_notify_url=settings.ALIAPY_CONFIG['app_notify_url'],  # 默认回调url
            # app_private_key_string=app_private_key_string,  # 应用私钥
            # # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # alipay_public_key_string=alipay_public_key_string,
            app_private_key_string=settings.ALIAPY_CONFIG['app_private_key_path'],  # 应用私钥
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=settings.ALIAPY_CONFIG['alipay_public_key_path'],
            sign_type=settings.ALIAPY_CONFIG['sign_type'],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG['debug'],  # 默认False
        )

        # 生成支付宝的支付链接
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_number,
            total_amount=float(order.real_price),
            subject=order.order_title,
            return_url=settings.ALIAPY_CONFIG['return_url'],
            notify_url=settings.ALIAPY_CONFIG['notify_url']  # 可选, 不填则使用默认notify url
        )

        # 生成支付的链接地址  需要将order_string与网关拼接进行拼接
        url = settings.ALIAPY_CONFIG['gateway_url'] + order_string

        return Response(url)


class AiliPayResultAPIView(APIView):
    """
    处理支付成功后的业务：验证支付情况
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # print('初始化')
        # print(request.user.id)
        # 支付的初始化参数
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG['appid'],  # 沙箱支付的应用id
            app_notify_url=settings.ALIAPY_CONFIG['app_notify_url'],  # 默认回调url
            # app_private_key_string=app_private_key_string,  # 应用私钥
            # # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # alipay_public_key_string=alipay_public_key_string,
            app_private_key_string=settings.ALIAPY_CONFIG['app_private_key_path'],  # 应用私钥
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=settings.ALIAPY_CONFIG['alipay_public_key_path'],
            sign_type=settings.ALIAPY_CONFIG['sign_type'],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG['debug'],  # 默认False
        )

        # 验证alipay的异步通知，
        data = request.query_params.dict()
        signature = data.pop("sign")
        success = alipay.verify(data, signature)
        # print(success)

        if success:
            # 验证支付结果成功后 开始处理订单相关的业务
            return self.order_result_pay(data)

        return Response({"message": "对不起，当前订单支付失败"})

    def order_result_pay(self, data):
        """
        修改订单
        生成用户购买记录
        展示购买的订单信息
        :return:
        """

        # 先查看订单是否成功
        order_number = data.get('out_trade_no')
        # print(order_number)

        try:
            order = Order.objects.get(order_number=order_number, order_status=0)
            # print(order)
        except Order.DoesNotExist:
            return Response({"message": "对不起，当前订单支付出现异常了"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 更新订单信息
            order.pay_time = datetime.datetime.now()
            # print(order.pay_time)
            order.order_status = 1
            order.save()

            # 根据订单获取对应的用户
            user = order.user
            # print(user)
            # 获取购买订单的所有课程
            order_courses_all = order.order_courses.all()
            # print(order_courses_all)
            # 订单结算页所需的课程信息
            course_list = []

            for course_detail in order_courses_all:
                """遍历本次订单中所有的商品"""
                # 课程购买人数的增长
                course = course_detail.course
                course.students += 1
                # print(course.students)
                course.save()
                # print(course,"course")

                # 判断用户购买的课程是永久有效 如果不是永久有效则记录到期时间
                pay_time = order.pay_time
                # print(pay_time)
                # print(course_detail.expire)

                # 不是永久课程
                if course_detail.expire > 0:
                    # 处理到期时间  最终到期时间= 购买时间+有效期
                    pass
                    expire_item = CourseExpire.objects.filter(is_delete=False, is_show=True, pk=course_detail.expire)[0]
                    expire_time = expire_item.expire_time
                    expire_text = expire_item.expire_text
                    origin_price = float(expire_item.price)
                    # print(origin_price)
                    # print(expire_time)
                    end_timestamp = datetime.timedelta(days=expire_time)
                    end_time = ( pay_time + end_timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    # print(end_time)
                else:
                    # 永久购买
                    expire_time='永久有效'
                    expire_text="永久有效"
                    origin_price= course.price
                    end_time = '2099-12-13'
                    print(end_time)

                #  为用户生成购买记录
                trade_no = data.get('trade_no')
                usercourse = UserCourse.objects.create(user=user,course=course,trade_no=trade_no,buy_type=1,pay_time=order.pay_time,out_time=end_time)
                # print(usercourse)

                #  为前端返回所需的信息
                course_list.append(
                                {
                                    "order_number": order_number,
                                    "pay_time":order.pay_time,
                                    "id" :course.id,
                                    "name":course.name,
                                    "course_img":IMAGE_SRC + course.course_img.url,
                                    "brief":course.brief,
                                    "discount_name":course.discount_name,
                                    "real_price":course.expire_real_price(expire_id=course_detail.expire),
                                    "origin_price":origin_price,
                                    "expire_time":expire_time,
                                    "expire_text":expire_text,
                                    "end_time":end_time,
                                }
                            )

        except Order.DoesNotExist:
            return Response({"message": "订单信息更新失败"})

        return Response({"message": "支付成功",
                         "success": "success",
                         "course_list":course_list,
                         "total_price": data.get("total_amount"),
                         "pay_time":order.pay_time})

# class CoursePayAPIView(ViewSet):
#     def pay_list(self,request):

