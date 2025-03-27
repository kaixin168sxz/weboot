import copy
import wechat
from openai import OpenAI
import time
import json
import os

client = OpenAI(api_key="<your-apikey>", base_url="https://api.deepseek.com")

with open("./Weboot提示词.txt", "r", encoding="UTF-8") as f:
    system_role = f.read()

ai_msg = [{"role": "system", "content": system_role}, ]

wait = 3
wechat.listen(['上海哥哥', ])

if os.path.exists('./history.json'):
    with open('./history.json', 'r') as f:
        ai_msg = json.load(f)['data']

while True:
    messages = wechat.scan()
    if messages and messages[0] != '[动画表情]':
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
        )
        response = res.choices[0].message.content
        print('AI> ', end='')
        # print(res.choices[0].message.reasoning_content)
        print(response)
        ai_msg.append({"role": "assistant", "content": response})
        with open('./history.json', 'w') as f:
            f.write(json.dumps({'data': ai_msg}, sort_keys=True, indent=4, separators=(',', ': ')))

        print()
        if len(ai_msg) > 5:
            ai_msg_ = copy.deepcopy(ai_msg)
            ai_msg_ = ai_msg_[-4: ]
            ai_msg_.insert(0, {'role': 'system', 'content': system_role})         # 防止初始提示词被覆盖
            ai_msg = copy.deepcopy(ai_msg_)

        wechat.send(['上海哥哥', ], 'AI:'+response)
    time.sleep(wait)