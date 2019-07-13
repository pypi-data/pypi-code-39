import wx
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from DesktopScoreViewer.ScoreWindow import ScoreWindow
from DesktopScoreViewer.GameWindow import GameWindow

def alignToTopRight(win):
    dw, dh = wx.DisplaySize()
    w, h = win.GetSize()
    x = dw - w
    win.SetPosition((x,25))

class MenuWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Desktop Score Viewer', size=(400,207),
                         style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        nba_button = wx.Button(self.panel, label='NBA (Currently not available)')
        nfl_button = wx.Button(self.panel, label='NFL Currently not available)')
        mlb_button = wx.Button(self.panel, label='MLB')

        mlb_button.Bind(wx.EVT_BUTTON, self.on_click_mlb)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.sizer.Add(nba_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(nfl_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(mlb_button, 0, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(self.sizer)

        self.driver = None

        self.Show()


    def on_click_mlb(self, event):
        #list to store scraped basic game data
        statictextlist = []

        #load page
        url = "https://www.espn.com/mlb/scoreboard"
        #adds option to open browser in background
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(executable_path='/Users/josephjung/PycharmProjects/DesktopScoreViewer/geckodriver',
                                        options=options)
        self.driver.get(url)
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'lxml')

        #get current date and create display window to show game data
        today = soup.find('span', id="sbpDate")
        self.display = ScoreWindow(self, "MLB " + today.text)

        #get all current ongoing games and for each game, get teams and score
        games = soup.findAll('article', class_="scoreboard baseball live js-show")
        for game in games:
            #get each inning
            inning = game.find('th', class_="date-time")

            #get each game info
            scores = game.findAll('td', class_="total")
            competingteamnames = game.findAll('span', class_="sb-team-short")
            competingteamabbrev = game.findAll('span', class_="sb-team-abbrev")

            #pair up scraped teams according to each game
            for i in range(len(competingteamnames)):
                score = scores[i].text
                if i%2 == 0:
                    away = competingteamabbrev[i].text + " " + competingteamnames[i].text
                    text = str(inning.text + "\nAway: " + away + " - " + score)
                else:
                    home = competingteamabbrev[i].text + " " + competingteamnames[i].text
                    text = str("Home: " + home + " - " + score)

                #add team name, abbreviation and score to display window
                textdisplay = wx.StaticText(self.display.scorePanel, label=text)
                statictextlist.append(textdisplay)

        # get links
        links = soup.findAll('a', class_="button-alt sm", href=re.compile("/mlb/game*"))

        gamenumber = 1
        for count in range(len(statictextlist)):
            if count%2 == 1:
                gamedivider = wx.StaticBox(self.display.scorePanel, -1, "Game {0}".format(gamenumber))
                gamedividersizer = wx.StaticBoxSizer(gamedivider, wx.VERTICAL)

                #add statictext to staticboxsizer
                gamedividersizer.Add(statictextlist[count-1], 0, wx.ALIGN_CENTER, 10)
                gamedividersizer.Add(statictextlist[count], 0, wx.ALIGN_CENTER, 10)

                #add staticboxsizer to display sizer
                self.display.scorewindowsizer.Add(gamedividersizer, 1, wx.EXPAND | wx.ALL, 10)

                #create a button to follow a specific game in more detail
                followbutton = wx.Button(self.display.scorePanel, label="Follow Game {0}".format(gamenumber))
                followbutton.link = links[gamenumber-1]
                followbutton.gameno = gamenumber
                followbutton.gameinfo = games[gamenumber-1]
                self.display.scorewindowsizer.Add(followbutton, 0, wx.ALL | wx.ALIGN_CENTER, 10)
                followbutton.Bind(wx.EVT_BUTTON, self.follow_game)

                gamenumber += 1

        #add boxsizer that contains all game data and show display window while hiding main menu window
        self.display.scorePanel.SetSizer(self.display.scorewindowsizer)
        self.display.scorePanel.SetupScrolling()
        alignToTopRight(self.display)
        self.display.Show()
        self.Hide()

    def follow_game(self, event):
        but = event.GetEventObject()

        teams = but.gameinfo.findAll('span', class_="sb-team-abbrev")
        gamewindowtitle = str("MLB - " + teams[0].text + " VS " + teams[1].text)

        self.display.game = GameWindow(self.display, gamewindowtitle, but)
        alignToTopRight(self.display.game)
        self.display.Hide()
        self.display.game.Show()

    #cleanly closes itself and firefox driver
    def OnClose(self, event):
        self.Destroy()
        if(self.driver):
            self.driver.close()





