# coding=utf8
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

# 通过这个程序实现发送邮件的功能。本来想和

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr))

def let_send():
    from_addr = 'zangchangan@163.com'
    password = 'a215381460'
    to_addr = 'changan@theping.cn'
    smtp_server = 'smtp.163.com'

    msg = MIMEText('现在ip地址少于4个，请注意', 'plain', 'utf-8')
    msg['From'] = _format_addr(u'Python爱好者 <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    msg['Subject'] = Header(u'来自SMTP的问候……', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


