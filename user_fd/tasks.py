from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freshday.settings')
    subject = '天天生鲜欢迎您'
    message = ''
    sender = settings.EMAIL_HOST_USER  # 发件人
    reciver = to_email
    html_message = "<h1>%s 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href='http://127.0.0.1:8000/user/active/%s'>激活</a>" % (
        username, token)
    send_mail(subject, message, sender, reciver, html_message=html_message, fail_silently=False)


if __name__ == '__main__':
    send_register_active_email()
