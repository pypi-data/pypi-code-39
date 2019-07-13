
import wx
from DesktopScoreViewer.MenuWindow import MenuWindow
from DesktopScoreViewer.MenuWindow import alignToTopRight

def main():
    app = wx.App()
    frame = MenuWindow()
    alignToTopRight(frame)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
