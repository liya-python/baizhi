import datetime

from my_task.main import app
from order.models import Order


@app.task(name="check_order")
def check_order():
    order_all =Order.objects.all()
    for order in order_all:
        if order.order_status == 0:
            create_time = order.create_time
            offent = datetime.timedelta(minutes=0.5)
            end_time = (create_time + offent).timestamp()
            if datetime.datetime.now().timestamp()>=end_time:
                order.order_status = 3
                order.save()
                print('超时取消')
    return 'order'