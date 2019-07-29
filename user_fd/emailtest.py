from django.core.mail import send_mail
import os
from smtplib import SMTPRecipientsRefused


class SendEmai():
    """

    """
    def __init__(self, subject, sender,reciver_list, message=None, html_messqge=None, fail_silently=False):
        self.subject = subject
        self.message = message
        self.sender = sender
        self.fail_silently = fail_silently
        self.html_messqge = html_messqge
        if not type(reciver_list) == type(list()):
            print('Type Erro for your reciver_list')
            # return 'Type Erro for your reciver_list'
        self.reciver_list = reciver_list

    def simplify_send_email(self, message=None, html_messqge=None, fail_silently=False):
        """ 该方法只能实现简单邮件发送，对多发无法识别邮件报错机制
            可以尝试并发执行
        """
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freshday.settings")
        # django.setup()  无用
        erro = {}
        try:
            # subject = 'OFFER'  # 邮件主题
            # message = ''  # 邮件正文
            # # sender = 'pat201978@163.com'  #发件人
            # sender = '995010997@qq.com'
            # reciver = ['924304012@qq.com', ]
            send_mail(self.subject, message, self.sender, self.reciver_list, fail_silently=fail_silently,
                      html_message=html_messqge)
        except SMTPRecipientsRefused as SMTP_ERRO:
            erro = {'erro': '邮箱不存在或者邮件被拒绝'}
            print(erro,SMTP_ERRO)
        except Exception:
            print(Exception)


if __name__ == '__main__':
    # subject = 'OFFER'  # 邮件主题
    # # message = '实例化 邮件对象测试数据'  # 邮件正文
    # # sender = 'pat201978@163.com'  #发件人
    # sender = '995010997@qq.com'
    # reciver = ['924304012@qq.com']
    # html = "<h1>亲爱的 ，你已成为我们的优选会员，点击'www.baidu.com'激活你的账户</h1>"
    # s = SendEmai(subject, sender, reciver)
    # s.simplify_send_email(html)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freshday.settings")
    subject = 'OFFER'  # 邮件主题
    message = ''  # 邮件正文
    sender = '995010997@qq.com'  #发件人
    reciver = ['924304012@qq.com', ]
    html_message = "<a href = 'https://www.baidu.com/'> 1</a>"
    send_mail(subject, message,sender,reciver,False,html_message=html_message)