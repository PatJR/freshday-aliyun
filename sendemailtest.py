import smtplib
from email.mime.text import MIMEText

#第三方SMTP服务
mail_host = "smtp.qq.com"
mail_user = "995010997@qq.com"
mail_pass = "xmmafvuvvboybecj"

sender = "995010997@qq.com"
receiver = "924304012@qq.com"

message = MIMEText("你好，世界！")
message["From"] = sender
message["To"] = receiver
message["Subject"] = "一起嗨吧！"

def send_email():
    try:
        server = smtplib.SMTP()
        server.connect(mail_host, port=25)
        server.login(mail_user,mail_pass)
        server.sendmail(sender,receiver,message.as_string())
        server.close()
        print("邮件发送成功!")
    except Exception as e:
        print("邮件发送失败!",e)

if __name__ == '__main__':
    send_email()