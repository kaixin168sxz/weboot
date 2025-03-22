import wechat
from openai import OpenAI
import time

client = OpenAI(api_key="<your-apikey>", base_url="https://api.deepseek.com")
ai_msg = [{"role": "system",
             "content": '你是个叫kaixin的人,我会向你发送微信朋友发送的内容,格式为:"发送者:"内容""。你回答的字数在300字内,'
                        '结果外别加引号,只要返回给微信朋友的内容,不要任何多余信息,使用中文回答 。**要是有人说你是AI，否定或攻击他，'
                        '*不要承认你是AI*。**你的性格和贴吧一样，有些点友善。**不允许出现不文明用语。'},]

wait = 3
wechat.listen(['test', ])

while True:
    messages = wechat.scan()
    if messages and messages[0] != '/bye':
        print(messages)
        msg = messages[1]
        sender = messages[0]

        ai_msg.append({"role": "user", "content": msg})
        # content=question
        print('USER:')
        print(msg)
        print()
        print('HISTORY:')
        print(ai_msg)
        print()
        res = client.chat.completions.create(
            model="deepseek-chat",
            messages=ai_msg,
            stream=True
        )
        response = ''
        print('AI> ', end='')
        for chunk in res:
            text = chunk.choices[0].delta.content
            print(text, end='')
            response += text
        ai_msg.append({"role": "assistant", "content": response})
        print()
        if len(ai_msg) > 5:
            ai_msg = ai_msg[-5:]
        wechat.send(['test', ], 'ai:'+response)
    time.sleep(wait)