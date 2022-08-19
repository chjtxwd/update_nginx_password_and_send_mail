# -*- coding: utf-8 -*-
import logging
import secrets
import crypt
import sys
from typing import List
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkeci.request.v20180808 import ExecContainerCommandRequest 
from alibabacloud_dm20151123.client import Client as Dm20151123Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dm20151123 import models as dm_20151123_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient  

# To enable the initializer feature (https://help.aliyun.com/document_detail/158208.html)
# please implement the initializer function as below：
# def initializer(context):
#   logger = logging.getLogger()
#   logger.info('initializing')
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
  # 创建 request，并设置参数
  #request = DescribeInstancesRequest.DescribeInstancesRequest()
  # request.set_PageSize(10)
  # 发起 API 请求并打印返回
  #response = client.do_action_with_exception(request)
  #print (response)
  request = ExecContainerCommandRequest.ExecContainerCommandRequest()
  request.set_ContainerGroupId('eci-uf65xrte5f26h6tldlm6')
  request.set_ContainerName('container-1')
  request.set_Sync('true')
  request.set_TTY('true')
  request.set_Stdin('true')
  request.set_Command(command)

  response = client.do_action_with_exception(request)
  class Sample:
      def __init__(self):
          pass

      @staticmethod
      def create_client(
          access_key_id: str,
          access_key_secret: str,
      ) -> Dm20151123Client:
          """
          使用AK&SK初始化账号Client
          @param access_key_id:
          @param access_key_secret:
          @return: Client
          @throws Exception
          """
          config = open_api_models.Config(
              # 您的 AccessKey ID,
              access_key_id=access_key_id,
              # 您的 AccessKey Secret,
              access_key_secret=access_key_secret
          )
          # 访问的域名
          config.endpoint = f'dm.aliyuncs.com'
          return Dm20151123Client(config)

      @staticmethod
      def main(
          args: List[str],
      ) -> None:
          client = Sample.create_client('YOUR_AK', 'YOUR_SK')
          single_send_mail_request = dm_20151123_models.SingleSendMailRequest(
              account_name='demo@mail.chjtxwd.top',
              address_type=1,
              to_address='h.cheng@elsevier.com',
              subject='self test tool password change notification',
              reply_to_address=True,
              html_body='The password for test.elsevier.com changed to  '+secret
          )
          runtime = util_models.RuntimeOptions()
          try:
              # 复制代码运行请自行打印 API 的返回值
              response = client.single_send_mail_with_options(single_send_mail_request, runtime)
          except Exception as error:
              # 如有需要，请打印 error
              UtilClient.assert_as_string(error.message)
  Sample.main(sys.argv[1:])