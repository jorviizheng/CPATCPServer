#encoding:utf-8
import ConfigParser
import httplib
import json
import time
from urlparse import urlparse
from AliRocketMQ.sample.Util import parseURL,calSignature

from thinkutils.log.log import *
from thinkutils.common_utils.object2json import *
"""
消息订阅者
"""
class HttpConsumer(object):
    def __init__(self):
        """签名字段"""
        self.signature = "Signature"
        """Consumer ID"""
        self.consumerid = "ConsumerID"
        """消费主题"""
        self.topic = "Topic"
        """访问码"""
        self.ak = "AccessKey"
        """配置文件解析器"""
        self.cf = ConfigParser.ConfigParser()
    """
    订阅消息流程
    """
    def process(self):
        """开始读取配置文件"""
        self.cf.read("app.properties")
        """读取主题"""
        topic = self.cf.get("ali_mq", "Topic")
        """存储消息的URL路径"""
        url = self.cf.get("ali_mq", "URL")
        """访问码"""
        ak = self.cf.get("ali_mq", "Ak")
        """密钥"""
        sk = self.cf.get("ali_mq", "Sk")
        """Consumer ID"""
        cid = "CID_ZHUOLINK_SDK1"#self.cf.get("property", "ConsumerID")
        newline = "\n"
        """获取URL主机域名地址"""
        urlname = urlparse(url).hostname
        """连接存储消息的服务器"""
        conn = httplib.HTTPConnection(parseURL(urlname))
        while True:
            try:
                """时间戳"""
                date = repr(int(time.time() * 1000))[0:13]
                """构造签名字符串"""
                signString = topic + newline + cid + newline + date
                """计算签名值"""
                sign = calSignature(signString,sk)
                """请求消息HTTP头部"""
                headers = {
                    self.signature : sign,
                    self.ak : ak,
                    self.consumerid : cid
                }
                """开始发送获取消息的HTTP请求"""

                conn.request(method="GET",url=url+"/message/?topic="+topic+"&time="+date+"&num=32",headers=headers)
                """获取HTTP应答消息"""
                response = conn.getresponse()
                """验证应答消息状态值"""
                if response.status != 200:
                    continue

                """从应答消息中读取实际的消息内容"""
                msg = response.read()
                """将实际的消费消息进行解码"""
                messages = json.loads(msg)
                if len(messages) == 0:
                    time.sleep(0.1)
                    continue
                else:
                    g_logger.info(msg)

                """依次获取每条消费消息"""
                for message in messages:
                    """计算时间戳"""
                    date = repr(int(time.time() * 1000))[0:13]
                    """构建删除消费消息URL路径"""
                    delUrl = url + "/message/?msgHandle="+message['msgHandle'] + "&topic="+topic+"&time="+date
                    """构造签名字符串"""
                    signString = topic + newline + cid + newline + message['msgHandle'] + newline + date
                    """进行签名"""
                    sign = calSignature(signString,sk)
                    """构造删除消费消息HTTP头部"""
                    delheaders = {
                        self.signature : sign,
                        self.ak : ak,
                        self.consumerid : cid,
                    }
                    """发送删除消息请求"""
                    conn.request(method="DELETE", url=delUrl, headers=delheaders)
                    """获取请求应答"""
                    response = conn.getresponse()
                    """读取应答内容"""
                    msg = response.read()
                    g_logger.info("delete msg: %s" % (msg, ))
            except Exception,e:
                print e
        conn.close()
"""启动入口"""
if __name__ == '__main__':
    """构造消息订阅者"""
    consumer = HttpConsumer()
    """开始启动消息订阅者"""
    consumer.process()