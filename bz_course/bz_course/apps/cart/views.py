import logging

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated

from bz_course.settings.constanst import IMAGE_SRC
from course.models import Course, CourseExpire

logger = logging.getLogger("django")


class CartViewSet(ViewSet):
    """购物车相关的业务"""

    # 只允许已登录且认证成功的用户访问
    permission_classes = [IsAuthenticated]

    def add_cart(self, request):
        """
        将用户提交的课程添加进购物车
        :param request: 用户id  课程id  勾选状态  有效期
        :return:
        """
        course_id = request.data.get("course_id")
        user_id = request.user.id
        print(user_id,'1user_id')
        # 是否勾选
        select = True
        # y有效期
        expire = 0

        # 校验前端传递的参数
        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，课程不存在"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 将商品的信息储存至redis
            redis_connection = get_redis_connection("cart")
            # redis的管道
            pipeline = redis_connection.pipeline()
            # 开启管道
            pipeline.multi()
            # 商品的信息以及对应的有效期   cart_1    1   0
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            # 被勾选的商品
            pipeline.sadd("select_%s" % user_id, course_id)
            # 执行
            pipeline.execute()

            # 获取购物车商品数量
            cart_length = redis_connection.hlen("cart_%s" % user_id)

        except:
            logger.error("购物车数据储存失败")
            return Response({"message": "参数有误，添加购物车失败"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "添加购物车成功", "cart_length": cart_length}, status=status.HTTP_200_OK)

    def list_cart(self, request):
        """展示购物车"""
        user_id = request.user.id
        # print(user_id)
        redis_connection = get_redis_connection('cart')
        cart_list_bytes = redis_connection.hgetall("cart_%s" % user_id)
        select_list_bytes = redis_connection.smembers("select_%s" % user_id)
        # print(select_list_bytes)

        # 循环从mysql中查询出商品的信息
        data = []
        for course_id_byte, expire_id_byte in cart_list_bytes.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            print(expire_id,"expire_id")

            try:
                # 获取购物车中所有的商品信息
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                # print(type(course))
            except Course.DoesNotExist:
                continue
            print(course.expire_real_price(expire_id))
            data.append({
                "course_img": IMAGE_SRC + course.course_img.url,
                "name": course.name,
                "expire_id": expire_id,
                "id":course.id,
                "price":course.expire_real_price(expire_id),
                "selected": True if course_id_byte in select_list_bytes else False,
                # 课程对应的有效期选项
                "expire_list": course.expire_list,
            })
        # print(data)
        return Response(data)
    def del_cart(self,request):
        """从购物车中删除某个课程"""
        user_id = request.user.id
        id = request.query_params.get('id')
        print(id)

        try:
            Course.objects.get(is_show=True, is_delete=False, pk=id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，当前商品已下架"}, status=status.HTTP_400_BAD_REQUEST)

        redis_connection = get_redis_connection('cart')
        pipe = redis_connection.pipeline()
        pipe.multi()
        pipe.hdel("cart_%s" % user_id, id)
        pipe.srem("select_%s" % user_id, id)
        pipe.execute()

        return Response({"message": "删除商品成功"})

    def change_select(self, request):
        """切换购物车商品的状态"""
        user_id = request.user.id
        selected = request.data.get("selected")
        course_id = request.data.get("course_id")
        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误！当前商品不存在"}, status=status.HTTP_400_BAD_REQUEST)

        redis_connection = get_redis_connection("cart")
        if selected:
            # 将商品添加至 set中  代表选中
            redis_connection.sadd("select_%s" % user_id, course_id)
        else:
            redis_connection.srem("select_%s" % user_id, course_id)

        return Response({"message": "状态切换成功~~~~~"})

    def change_expire(self, request):
        """改变redis的课程有效期"""
        user_id = request.user.id
        course_id = request.data.get("course_id")
        expire_id = request.data.get("expire_id")
        # print(expire_id, "expire_id")

        try:
            course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)

            # 如果前端传递的有效期选项不是0  则修改对应的有效
            if expire_id > 0:
                expire_item = CourseExpire.objects.filter(is_delete=False, is_show=True, pk=expire_id)
                if not expire_item:
                    raise CourseExpire.DoesNotExist()
        except Course.DoesNotExist:
            return Response({"message": "操作的课程不存在"}, status=status.HTTP_400_BAD_REQUEST)

        redis_connection = get_redis_connection("cart")
        redis_connection.hset("cart_%s" % user_id, course_id, expire_id)
        # print(course.expire_real_price(expire_id))
        # TODO  重新计算修改有效期的课程的价格

        return Response({"message": "切换有效期成功", "price": course.expire_real_price(expire_id)})

    def get_select_course(self, request):
        """获取所有被选中的课程"""
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")

        # 获取当前登录用户的购物车的所有商品
        cart_list = redis_connection.hgetall("cart_%s" % user_id)
        select_list = redis_connection.smembers("select_%s" % user_id)

        total_price = 0  # 已勾选的商品总价
        data = []

        for course_id_byte, expire_id_byte in cart_list.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            if course_id_byte in select_list:

                try:
                    # 获取购物车中所有的商品信息
                    course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                except Course.DoesNotExist:
                    continue

                # 如果有效期的id大于0 则需要计算商品的价格 id不大于0则代表永久 需要默认值
                origin_price = course.price
                expire_text = "永久有效"

                if expire_id > 0:
                    try:
                        course_expire = CourseExpire.objects.get(pk=expire_id)

                        # 有效期对应的价格
                        origin_price = course_expire.price
                        expire_text = course_expire.expire_text

                    except CourseExpire.DoesNotExist:
                        pass

                # 根据已勾选的商品的对应有效期的价格计算最终勾选商品的价格
                real_expire_price = course.expire_real_price(expire_id)

                data.append({
                    'id': course.id,
                    # 'price': course.real_price(),
                    "course_img": IMAGE_SRC + course.course_img.url,
                    "name": course.name,
                    # 课程对应的有效期文本
                    "expire_text": expire_text,
                    # 获取有效期真实价格
                    "real_price": "%.2f" % float(real_expire_price),
                    # 原价
                    "price": origin_price,
                })

                # 商品所有的总价
                total_price += float(real_expire_price)

        total_price = "%.2f" % float(total_price)

        return Response({"course_list": data, "total_price": total_price, "message": "获取成功"})


