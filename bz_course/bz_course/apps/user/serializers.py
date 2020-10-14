import re
from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from bz_course.settings import constanst
from user.models import UserInfo
from user.utils import get_user_by_account


class UserModelSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text="用户token")
    code = serializers.CharField(max_length=8,write_only=True)
    '''用户序列化器'''
    class Meta:
        model = UserInfo
        fields = ('id','username','password','phone','token','code')
        extra_kwargs = {
            'id':{
                'read_only':True,
            },
            'username':{
                'read_only':True,
            },
            'password':{
                'write_only':True,
            },
            'phone':{
                'write_only':True,
            },
        }
    def validate(self, attrs):
        # print(attrs)
        '''验证手机号'''
        phone = attrs.get('phone')
        password = attrs.get('password')
        code = attrs.get('code')
        # print(code,'code',type(code))
        # 密码
        if not re.match(r'^\w{3,18}$',password):
            raise serializers.ValidationError('密码格式不正确')
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$',phone):

            raise serializers.ValidationError('手机号格式不正确')
            # 验证手机号是否被注册
        try:
            user =get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user = None
        if user:
            raise serializers.ValidationError("当前手机号已经被注册")

        # TODO  验证前端发送短信雁阵是否正确  是否一致  是否在有效期内
        redis_connection = get_redis_connection("sms")
        re_code = redis_connection.get("mobile_%s" % phone)
        # print(re_code,'re_code')
        if not re_code:
            raise  serializers.ValidationError('验证码失效')
        else:
            re_code = re_code.decode('utf-8')
            if code == re_code:
                # TODO 为了防止暴力破解 需要控制验证码的验证次数
                # redis_connection = get_redis_connection("sms")
                # num = redis_connection.incr('num')
                # print(num)
                # if num>10:
                #     return serializers.ValidationError('验证码发送次数达到上限')
                redis_connection.setex("mobile_%s" % phone,5,'')
            else:
                raise serializers.ValidationError('验证码错误')




        # 验证成功后将验证码删除
        return attrs

    def create(self, validated_data):
        # print('1111')
        """
        用户信息设置
        用户名  token  密码加密
        """
        # 对密码进行加密处理
        password = validated_data.get("password")
        hash_password = make_password(password)
        code = validated_data.get('code')
        # print(code)

        # 为用户名设置默认值  随机字符串  手机号
        username = validated_data.get("phone")

        # 添加数据
        user = UserInfo.objects.create(phone=username, username=username, password=hash_password,email='2793955734@qq.com' )
        from my_task.sms.tasks import send_sms
        send_sms.delay(username, code)
        # send_email.delay(user.email)
        # 为注册成功的用户生成token
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        # print(user)

        return user
