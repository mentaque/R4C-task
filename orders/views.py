import json

from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from customers.models import Customer
from orders.models import Order
from robots.models import Robot


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        robot_serial = data.get('robot_serial')
        customer_id = data.get('customer_id')

        customer = Customer.objects.get(id=customer_id)
        #Если модель робота есть
        robot = Robot.objects.filter(serial=robot_serial).first()
        if robot:
            Order.objects.create(customer_id=customer_id, robot_serial=robot_serial, notification_sent=True)
            subject = "Заказ успешно оформлен"
            message = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {robot.model}," \
                      f" версии {robot.version}." \
                      f" Этот робот есть в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
            from_email = "robot@example.com"
            recipient_list = [customer.email]
            send_mail(subject, message, from_email, recipient_list)
        #Если модели робота нет
        else:
            robot_info = robot_serial.split('-')
            Order.objects.create(customer_id=customer_id, robot_serial=robot_serial)
            subject = "Заказ успешно создан, ожидайте"
            message = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {robot_info[0]}," \
                      f" версии {robot_info[1]}." \
                      f" Пока что этого робота нет в наличии." \
                      f" Когда он появится мы обязательно вас оповестим."
            from_email = "robot@example.com"
            recipient_list = [customer.email]
            send_mail(subject, message, from_email, recipient_list)

        return HttpResponse("Заказ создан успешно, проверьте почту")
