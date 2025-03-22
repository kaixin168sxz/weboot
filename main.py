import copy

import wechat
from openai import OpenAI
import time
import datetime
import json
import os

client = OpenAI(api_key="<your-apikey>", base_url="https://api.deepseek.com")

system_role = ('你是个叫kaixin的人,我会向你发送微信朋友发送的内容,格式为:"发送者:内容"。你回答的字数在300字内,'
               '结果外别加引号,***只要返回给微信朋友的内容,不要任何多余信息***,使用中文回答 。**要是有人说你是AI，否定或攻击他，'
               '*不要承认你是AI*。**你的性格和贴吧一样，有些点友善。**不允许出现不文明用语。')

ai_msg = [{"role": "system", "content": system_role}, ]

wait = 3
wechat.listen(['爱闪闪发光', ])

if os.path.exists('./history.json'):
    with open('./history.json', 'r') as f:
        ai_msg = json.load(f)['data']

while True:
    messages = wechat.scan()
    if messages:
        print(messages)
        msg = messages[1]
        sender = messages[0]
        if msg == 'history':
            print(ai_msg)
            continue

        ai_msg.append({"role": "user", "content": sender+':'+msg})
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
        with open('./history.json', 'w') as f:
            f.write(json.dumps({'data': ai_msg}, sort_keys=True, indent=4, separators=(',', ': ')))

        print()
        if len(ai_msg) > 5:
            ai_msg_ = copy.deepcopy(ai_msg)
            ai_msg_ = ai_msg_[-4: ]
            ai_msg_.insert(0, {'role': 'system', 'content': system_role})         # 防止初始提示词被覆盖
            ai_msg = copy.deepcopy(ai_msg_)

        wechat.send(['爱闪闪发光', ], 'AI:'+response)
    time.sleep(wait)