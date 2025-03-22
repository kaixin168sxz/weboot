import wechat
import ollama

wait = 3
wechat.listen(['test', ])
ollama.create(model='kaixin', from_='llama3.1', system="你是一个名叫开心的人类，我会向你发送微信朋友向你发送的内容，格式为：“发送者: “内容””。你回答的字符数要控制在100字以内，不要太多，只要返回你想要回复的内容，在返回结果外不需要添加双引号。我会使用“<context>...<context>”来包裹上下文；在“context”中，“Self”代表你，我会以如下格式记录上下文:“发送者: “内容””，在回答时，你需要联系上下文来回答。注意：只要返回你想要回复给微信朋友的内容！只要返回你想要回复给微信朋友的内容！只要返回你想要回复给微信朋友的内容！使用中文回答！使用中文回答！使用中文回答！“<context>...<context>”中的是历史上下文！“<context>...<context>”中的是历史上下文！“<context>...<context>”中的是历史上下文！")
context = []

while True:
    messages = wechat.scan()
    if messages and messages[0] != '/bye':
        print(messages)
        msg = messages[1]
        sender = messages[0]

        question = sender+': “'+msg+'”'
        content = '<context>\n'+'\n'.join(context)+'<context>\n'+question
        # content=question
        print('USER:')
        print(content)
        res = ollama.chat(
            model='kaixin',
            messages=[{'role': 'user', 'content': content}],
            stream=False,
        )
        print('RETURN:')
        print(res.message.content)
        context.append(question)
        context.append('Self: “'+res.message.content+'”')
        if len(context) > 50:
            context = context[-48:]
        wechat.send(['test', ], res.message.content)