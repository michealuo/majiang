#!/usr/bin/env python
from twilio.rest import Client
# Your Account SID from twilio.com/console
account_sid = "AC46caa3141eefe2a510e792f657931762"
# Your Auth Token from twilio.com/console
auth_token  = "6403538376fa6a10339a488a130fafa9"
client = Client(account_sid, auth_token)
message = client.messages.create(
    # 这里中国的号码前面需要加86
    to="+8613732169662",
    from_="+19382228294",
    body="尊敬的用户您好,你的验证码为2054,如非本人操作,请忽视此条短信")
print(message.sid)