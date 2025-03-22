import re
import win32com.client
import win32gui
import wechat
from ollama import chat

def _window_enum_callback(hwnd, wildcard):
    """
    Pass to win32gui.EnumWindows() to check all the opened windows
    把想要置顶的窗口放到最前面，并最大化
    """
    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
        win32gui.BringWindowToTop(hwnd)
        # 先发送一个alt事件，否则会报错导致后面的设置无效：pywintypes.error: (0, 'SetForegroundWindow', 'No error message is available')
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        # 设置为当前活动窗口
        win32gui.SetForegroundWindow(hwnd)

wait = 3
wechat.listen(['文件传输助手', ])

while True:
    messages = wechat.scan()
    if messages and messages[0] != '/bye':
        print(messages)
        msg = messages[1]
        sender = messages[0]
        win32gui.EnumWindows(_window_enum_callback, '.*?Windows PowerShell.*?')
        res = chat(
            model='deepseek-r1:1.5b',
            messages=[{'role': 'user', 'content': msg}],
            stream=False,
        )
        wechat.send([sender, ], res)