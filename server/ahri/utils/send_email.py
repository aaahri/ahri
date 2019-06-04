# -*- coding:utf-8 -*-
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.header import Header


class SendEmail:

    def send(self, address, op, code):
        username = "ahri@aaahri.cn"
        password = "MXTF1997jtxm0318"
        # 自定义的回复地址
        replyto = "myfsnow@gmail.com"
        rcptto = address
        msg = MIMEMultipart("alternative")
        msg["Subject"] = Header("Sign Up - AHRI").encode()
        msg["From"] = "%s <%s>" % (Header("AHRI").encode(), username)
        msg["To"] = rcptto
        msg["Reply-to"] = replyto
        msg["Message-id"] = email.utils.make_msgid()
        msg["Date"] = email.utils.formatdate()
        # textplain = MIMEText("验证码：0000", _subtype="plain", _charset="UTF-8")
        # msg.attach(textplain)
        if op == 1:
            html = '''
            <div style="width: 100%">
        <div style="width: 100%;
            height: 80px;
            background: #3399cc;
            line-height: 80px;
            text-align: left;
            color:#fff;
            font-size: 24px;
            padding-left: 30px;
            box-sizing: border-box;">
            <span style="font-size: 60px;color:#333;font-weight:700">C</span>&nbsp;&nbsp;&nbsp;&nbsp;
            AHRI&nbsp;&nbsp;验证码
        </div>
        <div style="font-size: 22px;padding: 25px;">欢迎注册,您的验证码是: ''' + code + ''''</div>
    </div>'''
        else:
            html = '''
                        <div style="width: 100%">
                    <div style="width: 100%;
                        height: 80px;
                        background: #3399cc;
                        line-height: 80px;
                        text-align: left;
                        color:#fff;
                        font-size: 24px;
                        padding-left: 30px;
                        box-sizing: border-box;">
                        <span style="font-size: 60px;color:#333;font-weight:700">C</span>&nbsp;&nbsp;&nbsp;&nbsp;
                        AHRI&nbsp;&nbsp;验证码
                    </div>
                    <div style="font-size: 22px;padding: 25px;">您正在找回密码,您的验证码是: ''' + code + ''''</div>
                </div>'''
        texthtml = MIMEText(html, _subtype="html", _charset="UTF-8")
        msg.attach(texthtml)
        # 发送邮件
        try:
            client = smtplib.SMTP()
            # client = smtplib.SMTP_SSL()
            # python 2.7以上版本，若需要使用SSL，可以这样创建client
            # client = smtplib.SMTP_SSL()
            # SMTP普通端口为25或80
            client.connect("smtpdm.aliyun.com", 25)
            # 开启DEBUG模式
            client.set_debuglevel(0)
            client.login(username, password)
            # 发件人和认证地址必须一致
            # 备注：若想取到DATA命令返回值,可参考smtplib的sendmaili封装方法:
            #      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
            client.sendmail(username, rcptto, msg.as_string())
            client.quit()
            print("邮件发送成功！")
        except smtplib.SMTPConnectErro as e:
            print("邮件发送失败，连接失败:", e.smtp_code, e.smtp_error)
        except smtplib.SMTPAuthenticationError as e:
            print("邮件发送失败，认证错误:", e.smtp_code, e.smtp_error)
        except smtplib.SMTPSenderRefused as e:
            print("邮件发送失败，发件人被拒绝:", e.smtp_code, e.smtp_error)
        except smtplib.SMTPRecipientsRefused as e:
            print("邮件发送失败，收件人被拒绝:", e.smtp_code, e.smtp_error)
        except smtplib.SMTPDataError as e:
            print("邮件发送失败，数据接收拒绝:", e.smtp_code, e.smtp_error)
        except smtplib.SMTPException as e:
            print("邮件发送失败, ", e.message)
        except Exception as e:
            print("邮件发送异常, ", str(e))
