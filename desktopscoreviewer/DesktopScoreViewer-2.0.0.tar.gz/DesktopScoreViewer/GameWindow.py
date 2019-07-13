import wx
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class GameWindow(wx.Frame):
    def __init__(self, parent, text, button):
        self.parent = parent
        self.but = button
        self.dc = None

        # adds option to open browser in background
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(
            executable_path='/Users/josephjung/PycharmProjects/DesktopScoreViewer/geckodriver',
            options=options)

        #set up webscraping
        self.gameurl = "https://www.espn.com" + str(button.link.get('href'))
        self.driver.get(self.gameurl)
        self.page = self.driver.page_source
        soup = BeautifulSoup(self.page, 'lxml')

        # get game status
        gamestatus = soup.find('div', class_='mlbGamecast__pitchCount')
        balls = gamestatus.find('div', class_='pitchCount__item pitchCount__item--balls')
        strikes = gamestatus.find('div', class_='pitchCount__item pitchCount__item--strikes')
        outs = gamestatus.find('div', class_='pitchCount__item pitchCount__item--outs')

        self.ballcount = 0;
        self.strikecount = 0;
        self.outcount = 0;

        ball = balls.findAll('span')
        for b in ball:
            if (len(b.attrs['class']) > 1):
                self.ballcount += 1

        strike = strikes.findAll('span')
        for s in strike:
            if (len(s.attrs['class']) > 1):
                self.strikecount += 1

        out = outs.findAll('span')
        for o in out:
            if (len(o.attrs['class']) > 1):
                self.outcount += 1

        wx.Frame.__init__(self, parent, title=text, size=(400, 207),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.gamepanel = wx.Panel(self)
        self.gamewindowsizer = wx.BoxSizer(wx.VERTICAL)

        self.homeboxsizer = wx.BoxSizer(wx.VERTICAL)
        self.inningboxsizer = wx.BoxSizer(wx.VERTICAL)
        self.awayboxsizer = wx.BoxSizer(wx.VERTICAL)
        self.gamewindowgridsizer = wx.GridSizer(3, gap=(0,0))

        self.hometextdivider = wx.StaticBox(self.gamepanel)
        self.awaytextdivider = wx.StaticBox(self.gamepanel)
        self.inningtextdivider = wx.StaticBox(self.gamepanel)
        self.hometextsizer = wx.StaticBoxSizer(self.hometextdivider, wx.VERTICAL)
        self.awaytextsizer = wx.StaticBoxSizer(self.awaytextdivider, wx.VERTICAL)
        self.inningtextsizer = wx.StaticBoxSizer(self.inningtextdivider, wx.VERTICAL)

        self.hometext = wx.StaticText(self.gamepanel, label="HOME",
                                      style=wx.ALIGN_CENTER, size=(115, 0))
        self.awaytext = wx.StaticText(self.gamepanel, label="AWAY",
                                      style=wx.ALIGN_CENTER, size=(115, 0))
        self.inningtext = wx.StaticText(self.gamepanel, label="INNING",
                                        style=wx.ALIGN_CENTER, size=(115, 0))
        topfont = wx.Font(16, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.hometext.SetFont(topfont)
        self.awaytext.SetFont(topfont)

        inningtextfont = wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)
        self.inningtext.SetFont(inningtextfont)

        self.hometextsizer.Add(self.hometext, 1, wx.CENTER, 1, wx.Size(115,20))
        self.inningtextsizer.Add(self.inningtext, 1, wx.CENTER, 1, wx.Size(115,20))
        self.awaytextsizer.Add(self.awaytext, 1, wx.CENTER, 1, wx.Size(115,20))

        teamfont = wx.Font(16, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_NORMAL)
        teamsplaying = self.but.gameinfo.findAll('span', class_="sb-team-abbrev")

        self.hometeam = wx.StaticText(self.gamepanel, label=teamsplaying[1].text,
                                      style=wx.ALIGN_CENTER, size=(115,20))
        self.awayteam = wx.StaticText(self.gamepanel, label=teamsplaying[0].text,
                                      style=wx.ALIGN_CENTER, size=(115, 20))

        self.hometeam.SetFont(teamfont)
        self.awayteam.SetFont(teamfont)

        self.hometextsizer.Add(self.hometeam, 1, wx.CENTER, 1, wx.Size(115,20))
        self.awaytextsizer.Add(self.awayteam, 1, wx.CENTER, 1, wx.Size(115, 20))

        teamscores = soup.findAll('div', class_='score-container')
        gameinning = soup.find('span', class_='status-detail').text

        self.gametime = gameinning.split(' ')
        if(len(self.gametime) > 2):
            self.topbot = self.gametime[-2]
            self.inningno = self.gametime[-1]
        else:
            self.topbot = self.gametime[0]
            self.inningno = self.gametime[1]

        if (self.topbot == "Bottom"):
            self.hometextdivider.SetBackgroundColour("lime green")
            self.awaytextdivider.SetBackgroundColour("red")
        elif (self.topbot == "Top"):
            self.hometextdivider.SetBackgroundColour("red")
            self.awaytextdivider.SetBackgroundColour("lime green")
        else:
            self.hometextdivider.SetBackgroundColour("sky blue")
            self.awaytextdivider.SetBackgroundColour("sky blue")

        self.homescore = wx.StaticText(self.gamepanel, label=teamscores[0].text, size=(115,40), style=wx.ALIGN_CENTER)
        self.awayscore = wx.StaticText(self.gamepanel, label=teamscores[1].text, size=(115,40), style=wx.ALIGN_CENTER)
        self.inning = wx.StaticText(self.gamepanel, label="".join(self.inningno[:-2]), size=(115,40), style=wx.ALIGN_CENTER)

        scorefont = wx.Font(34, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.homescore.SetFont(scorefont)
        self.awayscore.SetFont(scorefont)
        self.inning.SetFont(scorefont)

        self.homescoredivider = wx.StaticBox(self.gamepanel)
        self.inningdivider = wx.StaticBox(self.gamepanel)
        self.awayscoredivider = wx.StaticBox(self.gamepanel)

        self.homescoresizer = wx.StaticBoxSizer(self.homescoredivider, wx.VERTICAL)
        self.inningsizer = wx.StaticBoxSizer(self.inningdivider, wx.VERTICAL)
        self.awayscoresizer = wx.StaticBoxSizer(self.awayscoredivider, wx.VERTICAL)

        self.homescoresizer.Add(self.homescore, 1, wx.CENTER, 1, wx.Size(115,40))
        self.inningsizer.Add(self.inning, 1, wx.CENTER, 1, wx.Size(115,20))
        self.awayscoresizer.Add(self.awayscore, 1, wx.CENTER, 1, wx.Size(115,40))

        self.balldivider = wx.StaticBox(self.gamepanel)
        self.strikedivider = wx.StaticBox(self.gamepanel)
        self.outdivider = wx.StaticBox(self.gamepanel)
        self.ballsizer = wx.StaticBoxSizer(self.balldivider, wx.VERTICAL)
        self.strikesizer = wx.StaticBoxSizer(self.strikedivider, wx.VERTICAL)
        self.outsizer = wx.StaticBoxSizer(self.outdivider, wx.VERTICAL)

        self.balltext = wx.StaticText(self.gamepanel, label="Balls", size=(115,20), style=wx.ALIGN_CENTER)
        self.striketext = wx.StaticText(self.gamepanel, label="Strikes", size=(115, 20), style=wx.ALIGN_CENTER)
        self.outtext = wx.StaticText(self.gamepanel, label="Outs", size=(115, 20), style=wx.ALIGN_CENTER)

        self.ballsizer.Add(self.balltext, 1, wx.CENTER, 1, wx.Size(115, 20))
        self.strikesizer.Add(self.striketext, 1, wx.CENTER, 1, wx.Size(115, 20))
        self.outsizer.Add(self.outtext, 1, wx.CENTER, 1, wx.Size(115, 20))

        self.homeboxsizer.AddMany([(self.hometextsizer, wx.CENTER),
                                   (self.homescoresizer, wx.CENTER),
                                   (self.ballsizer, wx.CENTER)])
        self.awayboxsizer.AddMany([(self.awaytextsizer, wx.CENTER),
                                   (self.awayscoresizer, wx.CENTER),
                                   (self.outsizer, wx.CENTER)])
        self.inningboxsizer.AddMany([(self.inningtextsizer, wx.CENTER),
                                     (self.inningsizer, wx.CENTER),
                                     (self.strikesizer, wx.CENTER)])

        self.gamewindowgridsizer.Add(self.homeboxsizer)
        self.gamewindowgridsizer.Add(self.inningboxsizer)
        self.gamewindowgridsizer.Add(self.awayboxsizer)
        self.gamewindowsizer.Add(self.gamewindowgridsizer)

        self.gamepanel.SetSizerAndFit(self.gamewindowsizer)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        #sets timer for every 15 seconds
        self.timer.Start(milliseconds=15000, oneShot=wx.TIMER_CONTINUOUS)

    def OnClose(self, event):
        if(self.dc):
            self.dc.Destroy()
        self.driver.close()
        self.parent.Show()
        self.Destroy()

    def OnPaint(self, event):
        self.dc = wx.PaintDC(self)

        self.DrawBalls()
        self.DrawStrikes()
        self.DrawOuts()

        # draw top and bottom triangles
        self.DrawTop()
        self.DrawBot()

    #draw and fill in ball circles
    def DrawBalls(self):
        ballbrush = wx.Brush("yellow", style=wx.BRUSHSTYLE_SOLID)
        self.dc.SetBrush(ballbrush)

        if self.ballcount == 0:
            ballbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            self.dc.SetBrush(ballbrush)
        self.dc.DrawCircle(25, 165, 6)
        if self.ballcount == 1:
            ballbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            self.dc.SetBrush(ballbrush)
        self.dc.DrawCircle(55, 165, 6)
        if self.ballcount == 2:
            ballbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            self.dc.SetBrush(ballbrush)
        self.dc.DrawCircle(85, 165, 6)
        if self.ballcount == 3:
            ballbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            self.dc.SetBrush(ballbrush)
        self.dc.DrawCircle(115, 165, 6)

    #draw and fill in strike circles
    def DrawStrikes(self):
        strikebrush = wx.Brush("red", style=wx.BRUSHSTYLE_SOLID)
        self.dc.SetBrush(strikebrush)

        if self.strikecount == 0:
            strikebrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            self.dc.SetBrush(strikebrush)
        self.dc.DrawCircle(165, 165, 6)
        if self.strikecount == 1:
            strikebrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            self.dc.SetBrush(strikebrush)
        self.dc.DrawCircle(200, 165, 6)
        if self.strikecount == 2:
            strikebrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            self.dc.SetBrush(strikebrush)
        self.dc.DrawCircle(235, 165, 6)

    #draw and fill in out circles
    def DrawOuts(self):
        outbrush = wx.Brush("red", style=wx.BRUSHSTYLE_SOLID)
        self.dc.SetBrush(outbrush)

        if self.outcount == 0:
            outbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            self.dc.SetBrush(outbrush)
        self.dc.DrawCircle(295, 165, 6)
        if self.outcount == 1:
            outbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            self.dc.SetBrush(outbrush)
        self.dc.DrawCircle(330, 165, 6)
        if self.outcount == 2:
            outbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            self.dc.SetBrush(outbrush)
        self.dc.DrawCircle(365, 165, 6)

    #draw top arrow
    def DrawTop(self):

        if(self.topbot == "Top"):
            topbrush = wx.Brush('sky blue', style=wx.BRUSHSTYLE_SOLID)
        else:
            topbrush = wx.Brush('sky blue', style=wx.BRUSHSTYLE_TRANSPARENT)
        self.dc.SetBrush(topbrush)

        topside1 = wx.Point(160, 85)
        topside2 = wx.Point(150, 105)
        topside3 = wx.Point(170, 105)
        toparrow = [topside1, topside2, topside3]
        self.dc.DrawPolygon(toparrow)

    #draw bot arrow
    def DrawBot(self):
        if (self.topbot == "Bottom"):
            botbrush = wx.Brush('sky blue', style=wx.BRUSHSTYLE_SOLID)
        else:
            botbrush = wx.Brush('sky blue', style=wx.BRUSHSTYLE_TRANSPARENT)
        self.dc.SetBrush(botbrush)

        botside1 = wx.Point(240, 105)
        botside2 = wx.Point(230, 85)
        botside3 = wx.Point(250, 85)
        botarrow = [botside1, botside2, botside3]
        self.dc.DrawPolygon(botarrow)

    #refresh GUI components
    def OnTimer(self, event):
        self.driver.get(self.gameurl)
        newpage = self.driver.page_source
        soup = BeautifulSoup(newpage, 'lxml')

        # get game status
        gamestatus = soup.find('div', class_='mlbGamecast__pitchCount')
        balls = gamestatus.find('div', class_='pitchCount__item pitchCount__item--balls')
        strikes = gamestatus.find('div', class_='pitchCount__item pitchCount__item--strikes')
        outs = gamestatus.find('div', class_='pitchCount__item pitchCount__item--outs')

        teamscores = soup.findAll('div', class_='score-container')
        gameinning = soup.find('span', class_='status-detail').text
        self.gametime = gameinning.split(' ')
        if (len(self.gametime) > 2):
            self.topbot = self.gametime[-2]
            self.inningno = self.gametime[-1]
        else:
            self.topbot = self.gametime[0]
            self.inningno = self.gametime[1]

        if(self.topbot == "Bottom"):
            self.hometextdivider.SetBackgroundColour("lime green")
            self.awaytextdivider.SetBackgroundColour("red")
        elif(self.topbot == "Top"):
            self.hometextdivider.SetBackgroundColour("red")
            self.awaytextdivider.SetBackgroundColour("lime green")
        else:
            self.hometextdivider.SetBackgroundColour("sky blue")
            self.awaytextdivider.SetBackgroundColour("sky blue")

        self.homescore.SetLabel(teamscores[0].text)
        self.awayscore.SetLabel(teamscores[1].text)
        self.inning.SetLabel("".join(self.inningno[:-2]))

        self.ballcount = 0;
        self.strikecount = 0;
        self.outcount = 0;

        ball = balls.findAll('span')
        for b in ball:
            if (len(b.attrs['class']) > 1):
                self.ballcount += 1

        strike = strikes.findAll('span')
        for s in strike:
            if (len(s.attrs['class']) > 1):
                self.strikecount += 1

        out = outs.findAll('span')
        for o in out:
            if (len(o.attrs['class']) > 1):
                self.outcount += 1

        self.gamepanel.Refresh()

        self.DrawBalls()
        self.DrawStrikes()
        self.DrawOuts()

        # draw top and bottom triangles
        self.DrawTop()
        self.DrawBot()

        self.Bind(wx.EVT_CLOSE, self.OnClose)