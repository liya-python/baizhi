from bz_course.settings import constanst
from bz_course.utils.send_msg import Message
from my_task.main import app


# celery的任务必须写在tasks文件中  别的文件不识别
@app.task(name="send_sms")  # name 可以指定当前的任务名称，如果不写，则使用默认的函数名作为任务名
def send_sms(phone, code):
    message = Message(constanst.API_KEY1)
    print(message)
    res = message.send_message(phone, code)
    print(res, 'res2')
    print("注册成功")

    return "hello"
@app.task(name="send_mail")
def send_email(email):
    from django.core.mail import send_mail
    send_mail('注册用户', '注册成功', '2793955734@qq.com',
              ['email'], fail_silently=False)
    print('邮件发送成功')
    return 'mail'