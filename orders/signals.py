from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def check_robot_availability(sender, instance, **kwargs):
    orders = Order.objects.filter(robot_serial=instance.serial, notification_sent=False)
    if orders:
        for order in orders:
            order.notification_sent = True
            order.save()
            subject = "Робот доступен в наличии"
            message = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.model}," \
                      f" версии {instance.version}." \
                      f" Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
            from_email = "robot@example.com"
            recipient_list = [order.customer.email]
            send_mail(subject, message, from_email, recipient_list)