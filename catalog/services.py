from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER

DEFAULT_EMAIL_TO = 'ILIDANUM@yandex.ru'


def send_email(blog_info, email_to=DEFAULT_EMAIL_TO):
    subject = f"Поздравляем с достижением!"
    message = f"Ваша статья {blog_info.title} достигла 100 просмотров "
    send_mail(subject, message, EMAIL_HOST_USER, [email_to])