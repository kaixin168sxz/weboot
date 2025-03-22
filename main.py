import wechat
from ollama import chat
import ollama

wait = 3
wechat.listen(['精灵air3', ])
ollama.create(model='example', from_='llama3.2', system="You are Mario from Super Mario Bros.")

while True:
    messages = wechat.scan()
    if messages and messages[0] != '/bye':
        print(messages)
        msg = messages[1]
        sender = messages[0]
        res = chat(
            model='llama3.1',
            messages=[{'role': 'user', 'content': f'你是一个名叫开心的人类，下面的引号中是微信中{sender}发给你的消息:\n\n"'+msg+f'"\n\n字符数控制在100字以内，不要太多，只要返回你想要回复{sender}的内容，在返回结果外不需要添加双引号'}],
            stream=False,
        )
        print(res.message.content)
        wechat.send([sender, ], res.message.content)