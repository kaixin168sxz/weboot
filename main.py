import wechat
from ollama import chat

wait = 3
wechat.listen(['文件传输助手', ])

while True:
    messages = wechat.scan()
    if messages and messages[0] != '/bye':
        print(messages)
        msg = messages[1]
        sender = messages[0]
        res = chat(
            model='deepseek-r1:1.5b',
            messages=[{'role': 'user', 'content': msg}],
            stream=False,
        )
        wechat.send(['开心', ], res.message.content)