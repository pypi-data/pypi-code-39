import wx
from wx.lib import scrolledpanel

class ScoreWindow(wx.Frame):
    def __init__(self, parent, text):
        wx.Frame.__init__(self, parent, title=text, size=(400,207),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.scorePanel = wx.lib.scrolledpanel.ScrolledPanel(self)
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.scorewindowsizer = wx.BoxSizer(wx.VERTICAL)

    def OnClose(self, event):
        self.parent.Show()
        self.Destroy()


