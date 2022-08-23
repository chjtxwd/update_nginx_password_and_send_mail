# -*- coding: utf-8 -*-
import logging
import secrets
import crypt
from aliyunsdkcore.client import AcsClient
from aliyunsdkeci.request.v20180808 import ExecContainerCommandRequest 
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr 

def handler(event, context):
  logger = logging.getLogger()
  # generate nginx basic auth random password
  secret = secrets.token_hex(4)
  print(secret)
  c = crypt.crypt(secret)
  print(c)
  a = r'["/bin/sh", "-c", "echo '
  command = '\'user:'
  b = r'\'> /etc/nginx/conf/htpasswd"]'
  command = a+command+c+b
  # 创建 AcsClient 实例
  client = AcsClient(
    "YOUR_AK",
    "YOUR_SK",
    "cn-shanghai"
  );
  request = ExecContainerCommandRequest.ExecContainerCommandRequest()
  request.set_ContainerGroupId('eci-uf65xrte5f26h6tldlm6')
  request.set_ContainerName('container-1')
  request.set_Sync('true')
  request.set_TTY('true')
  request.set_Stdin('true')
  request.set_Command(command)

  response = client.do_action_with_exception(request)
  #set SMTP
  # username，通过控制台创建的发信地址
  username = 'usernam'
  # password，通过控制台创建的SMTP密码
  password = 'password'
  # 自定义的回信地址，与控制台设置的无关。邮件推送发信地址不收信，收信人回信时会自动跳转到设置好的回信地址。
  replyto = 'no-reply_self-diag-tool@elsevier.cn'
  # 显示的To收信地址
  rcptto = ['mail']
  receivers = rcptto 
  
  # 构建alternative结构
  msg = MIMEMultipart('alternative')
  msg['Subject'] = Header('self test tool password change notification')
  msg['From'] = formataddr(["no-reply_self-diag-tool", username])  # 昵称+发信地址(或代发)
  # list转为字符串
  msg['To'] = ",".join(rcptto)
  msg['Reply-to'] = replyto
  msg['Message-id'] = email.utils.make_msgid()
  msg['Date'] = email.utils.formatdate()
  html_body='The password for test.elsevier.com changed to  '+secret
  # 构建alternative的text/html部分
  texthtml = MIMEText(html_body, _subtype='html', _charset='UTF-8')
  msg.attach(texthtml)
  # 发送邮件
  try:
      # 若需要加密使用SSL，可以这样创建client
      client = smtplib.SMTP_SSL('smtpdm.aliyun.com', 465)
      # SMTP普通端口为25或80
      # client = smtplib.SMTP('smtpdm.aliyun.com', 80)
      # 开启DEBUG模式
      client.set_debuglevel(0)
      # 发件人和认证地址必须一致
      client.login(username, password)
      # 备注：若想取到DATA命令返回值,可参考smtplib的sendmail封装方法:
      # 使用SMTP.mail/SMTP.rcpt/SMTP.data方法
      # print(receivers)
      client.sendmail(username, receivers, msg.as_string())  # 支持多个收件人，最多60个
      client.quit()
      print('邮件发送成功！')
  except smtplib.SMTPConnectError as e:
      print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
  except smtplib.SMTPAuthenticationError as e:
      print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
  except smtplib.SMTPSenderRefused as e:
      print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
  except smtplib.SMTPRecipientsRefused as e:
      print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
  except smtplib.SMTPDataError as e:
      print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
  except smtplib.SMTPException as e:
      print('邮件发送失败, ', str(e))
  except Exception as e:
      print('邮件发送异常, ', str(e))