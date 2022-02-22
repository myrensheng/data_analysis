import requests
import time
import hmac
import hashlib
import base64
import urllib.parse


def judge_msg(key_msg_list, msg):
    for km in key_msg_list:
        if km in msg:
            return True
    return False


def make_sign(secret=None):
    timestamp = str(round(time.time() * 1000))
    if secret is None:
        return None
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # print(timestamp)
    # print(sign)
    return timestamp, sign


def dingding_robot(msg=None, key_msg_list=None, safe_set=None, send_type=None, secret=None, webhook=None,
                   at_mobiles=None, at_all=False, title="财联社"):
    """
    钉钉机器人
    :param title: 在消息显示的时候的简短信息
    :param secret: 密钥
    :param key_msg_list: 自定义的关键词列表
    :param msg: 发送的信息
    :param safe_set:安全设置，自定义关键词，加签
    :param send_type: 发送内容的类型：text，markdown(md)
    :param webhook: 申请的webhook
    :param at_mobiles: 默认为None，指定@某人，传入列表
    :param at_all: @所有人，传入True或者False
    :return: 发送是否成功标志
    """
    if webhook is None:
        return None
    if at_mobiles is None:
        at_mobiles = []
    if send_type not in ["text", "md", "markdown"]:
        print("send_type必须为['text', 'md', 'markdown']其中一个")
        return None
    if safe_set in ['自定义关键词', '加签']:
        header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
        send_content = {"at": {"atMobiles": at_mobiles, "isAtAll": at_all}}
        if send_type == "text":
            send_content["msgtype"] = "text"
            send_content["text"] = {"content": msg}
        elif send_type in ["md", "markdown"]:
            send_content["msgtype"] = "markdown"
            send_content["markdown"] = {"title": title, "text": msg}
        if safe_set == "自定义关键词":
            if not isinstance(key_msg_list, list) and not judge_msg(key_msg_list, msg):
                print("key_msg_list传入自定义的关键词列表，msg中必须包含其中一个关键词")
                return None
            res = requests.post(url=webhook, json=send_content, headers=header)
            return res.text
        elif safe_set == "加签":
            if secret:
                timestamp, sign = make_sign(secret)
                webhook = webhook + "&timestamp=" + timestamp + "&sign=" + sign
                res = requests.post(url=webhook, json=send_content, headers=header)
                return res.text
            else:
                print("secret为密钥，加签方式必须传入;")
                return None
    else:
        print("safe_set参数为['自定义关键词', '加签']其中一个")
        return None