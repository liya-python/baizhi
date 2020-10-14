# 任务队列的链接地址
from my_task.main import app

# 任务队列的链接地址
broker_url = "redis://127.0.0.1:6379/6"
# 结果队列的链接地址
result_backend = "redis://127.0.0.1:6379/7"

# 定时任务的调度
app.conf.beat_schedule = {
    'check_order_out_time': {
        # 本次定时任务要调度的任务
        'task': 'check_order',
        # 定时任务调度的周期
        'schedule': 30.0,
        # 'args': (16, 16)    # 是一个函数  有参数可以通过此函数传递  没参数无需传递
    },
}
