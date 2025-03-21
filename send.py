from wxauto import WeChat


def wechat(who: list[str], msg: str):  # 查询发送对象
    wx = WeChat()
    # 获取会话列表
    wx.GetSessionList()
    for w in who:
        wx.ChatWith(w)
        wx.SendMsg(msg)
