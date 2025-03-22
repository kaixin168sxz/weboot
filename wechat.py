from wxauto import WeChat
import pyautogui
import pyperclip

wx = WeChat()
def send(who: list[str], msg: str):  # 查询发送对象
    # 获取会话列表
    wx.GetSessionList()
    pyperclip.copy(msg)
    for w in who:
        wx.ChatWith(w)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

def listen(listen_list: list[str]):
    for i in listen_list:
        wx.AddListenChat(who=i)

def scan():
    # 然后调用`AddListenChat`方法添加监听对象，其中可选参数`savepic`为是否保存新消息图片
    msgs = wx.GetListenMessage()
    for chat in msgs:
        one_msgs = msgs.get(chat)  # 获取消息内容

        # 回复收到
        for msg in one_msgs:
            if msg.type == 'sys':
                print(f'【系统消息】{msg.content}')

            elif msg.type == 'friend':
                sender = msg.sender  # 这里可以将msg.sender改为msg.sender_remark，获取备注名
                print(f'<{sender.center(10, "-")}>：{msg.content}')

                return msg.sender, msg.content

            elif msg.type == 'self':
                print(f'<{msg.sender.center(10, "-")}>：{msg.content}')
                return msg.sender.replace('Self', '文件传输助手'), msg.content

            elif msg.type == 'time':
                print(f'\n【时间消息】{msg.time}')

            elif msg.type == 'recall':
                print(f'【撤回消息】{msg.content}')
