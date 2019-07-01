#!/usr/bin/env python3
#
# This file is part of Memoria.
#
# Copyright (C) 2019 - Thomas Dähnrich <develop@tdaehnrich.de>
#
# Memoria is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# Memoria is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Memoria. If not, see <http://www.gnu.org/licenses/>.

import gi
import os
import random
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Pango

from settings import PIXMAPS_DIR, SOUNDS_DIR, UI_DIR, VERSION
from settings import get_settings, setup_language


# get settings and setup language

get_settings()
_ = setup_language()


# create vocable cards and players

class Card(object):

    def __init__(self, vocable, button, turned, found):

        self.vocable = vocable
        self.button = button
        self.turned = turned
        self.found = found


class Player(object):

    def __init__(self, number, active, chkbtn, colbtn, ent, lblName, lblScore):

        self.number = number
        self.active = active
        self.chkbtn = chkbtn
        self.colbtn = colbtn
        self.ent = ent
        self.lblName = lblName
        self.lblScore = lblScore

        color_rgba = Gtk.ColorChooser.get_rgba(self.colbtn)
        self.color = '#{:02x}{:02x}{:02x}'.format(round(color_rgba.red*255),
            round(color_rgba.green*255), round(color_rgba.blue*255))

        self.name = self.ent.get_text()
        markup = self.get_label_markup(self.color, self.name)
        self.lblName.set_markup(markup)

        self.score = 0
        self.lblScore.set_text(str(self.score))


    def get_label_markup(self, color, text):

        if self.color[1] in "bcdef" or self.color[3] in "bcdef" or self.color[5] in "bcdef":
            markup = "<span background='{}' foreground='#000000'>{}</span>".format(self.color, text)
        else:
            markup = "<span background='{}' foreground='#ffffff'>{}</span>".format(self.color, text)

        return markup


# main functions of game

def setup_headerbar(self):

    decoration = Gtk.Settings.get_default().get_property("gtk-decoration-layout")
    if "close" in decoration.split(":")[0]:
        self.headGame.remove(self.menbtnGame)
        self.headGame.remove(self.btnNewGame)
        self.headGame.pack_start(self.menbtnGame)
        self.headGame.pack_end(self.btnNewGame)


def show_game_options(self):

    from list import get_vocabulary, get_vocabulary_error
    from settings import default_file, default_player_number
    global voc_unit

    # set default number of players when the window is shown for the first time
    if not len(self.listUnits) and not self.lblPlayer1.get_text():
        if default_player_number == 2:
            self.chkbtnPlayer2.set_active(True)
        if default_player_number == 3:
            self.chkbtnPlayer2.set_active(True)
            self.chkbtnPlayer3.set_active(True)
        if default_player_number == 4:
            self.chkbtnPlayer2.set_active(True)
            self.chkbtnPlayer3.set_active(True)
            self.chkbtnPlayer4.set_active(True)

    # load default vocabulary list, if one is set
    if os.path.exists(default_file):
        secondary_text, voc_unit = get_vocabulary(self.listUnits, default_file)
        if secondary_text:
            get_vocabulary_error(default_file, self.winGame, secondary_text)

    if not Gtk.check_version(3,22,0):
        self.popOptions.popup()
    else:
        self.popOptions.show_all()


def setup_game(self):

    global cards_number, pairs_found, players_number, tries_counter
    global player1, player2, player3, player4

    player1 = Player(1, True, self.chkbtnPlayer1, self.colbtnPlayer1, self.entPlayer1,
        self.lblPlayer1, self.lblScore1)
    player2 = Player(2, False, self.chkbtnPlayer2, self.colbtnPlayer2, self.entPlayer2,
        self.lblPlayer2, self.lblScore2)
    player3 = Player(3, False, self.chkbtnPlayer3, self.colbtnPlayer3, self.entPlayer3,
        self.lblPlayer3, self.lblScore3)
    player4 = Player(4, False, self.chkbtnPlayer4, self.colbtnPlayer4, self.entPlayer4,
        self.lblPlayer4, self.lblScore4)

    players_number = 1
    for player in (player2, player3, player4):
        if player.chkbtn.get_active():
            player.lblName.show()
            player.lblScore.show()
            players_number += 1
        else:
            player.ent.set_text("")
            player.lblName.hide()
            player.lblScore.hide()

    if self.cmbCardsNr.get_active() == 0:
        cards_number = 12
    if self.cmbCardsNr.get_active() == 1:
        cards_number = 16
    if self.cmbCardsNr.get_active() == 2:
        cards_number = 20
    if self.cmbCardsNr.get_active() == 3:
        cards_number = 24

    pairs_found = 0
    tries_counter = 0
    self.lblPairsCounter.set_text("0 / " + str(int(cards_number/2)))
    self.lblTriesCounter.set_text("0")


def build_cards(self):

    global cards, voc_active

    cards = []
    vocables = []

    # set dimensions for size of grid
    if cards_number == 12:
        x_range = 3
        y_range = 4
    elif cards_number == 16:
        x_range = 4
        y_range = 4
    elif cards_number == 20:
        x_range = 4
        y_range = 5
    elif cards_number == 24:
        x_range = 4
        y_range = 6

    # reduce number of active vocables to number of vocable cards
    while len(voc_active) > cards_number/2:
        voc_active.pop(random.randint(0, len(voc_active)-1))
    for i in range(len(voc_active)):
        vocables.append(voc_active[i][0])
        vocables.append(voc_active[i][1])

    # create vocable cards
    for y in range(y_range):
        for x in range(x_range):
            index = random.randint(0, len(vocables)-1)
            vocable = vocables[index]
            vocables.pop(index)
            btnCard = Gtk.Button.new_with_label(vocable)
            btnCard.set_property("visible", True)
            btnCard.set_property("hexpand", True)
            btnCard.set_property("vexpand", True)
            btnCard.set_property("height-request", 100)
            btnCard.set_property("width-request", 300)
            btnCard.set_property("margin", 10)
            btnCard.get_style_context().add_class("buttonCard")
            btnCard.get_child().get_style_context().add_class("buttonCard-label")
            btnCard.get_child().hide()
            btnCard.connect("clicked", self.on_btnCard_clicked)
            cards.append(Card(vocable, btnCard, False, False))
            self.gridPairs.attach(btnCard, x, y, 1, 1)


def get_turned_cards():

    cards_turned = ()

    for card in cards:
        if card.turned:
            cards_turned += (card.vocable,)

    return cards_turned


def pair_found(self):

    from settings import sound
    global cards, pairs_found, player1, player2, player3, player4

    # increase score and set css_data for active player
    for player in (player1, player2, player3, player4):
        if player.active:
            player.score += 1
            player.lblScore.set_text(str(player.score))
            css_data = ".color{}".format(str(player.number)) + "{\n" + \
                "  background: {};\n".format(player.color) + "}"
            break

    # set cards to found and color them with color of active player
    for card in cards:
        if card.turned:
            card.turned = False
            card.found = True
            card.button.get_style_context().add_class("color{}".format(str(player.number)))
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(css_data.encode())
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
        css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    # update statistical data
    pairs_found += 1
    text = str(pairs_found) + " / " + str(int(cards_number/2))
    self.lblPairsCounter.set_text(text)

    # check if game is finished
    if pairs_found*2 == cards_number:
        game_finished(self)
        if sound:
            play_sound(self, 'finish.wav')
    elif sound:
        play_sound(self, 'found.wav')


def pair_not_found(self):

    from settings import timer_length

    for card in cards:
        card.button.set_sensitive(False)
    if players_number > 1:
        self.lblTitel.set_text(_("Next player ({})").format(str(timer_length)))
    else:
        self.lblTitel.set_text(_("Next try ({})").format(str(timer_length)))
    GObject.timeout_add(1000, change_player, self)


def change_player(self):

    count = int(self.lblTitel.get_text()[-2])
    count -= 1
    if players_number > 1:
        self.lblTitel.set_text(_("Next player ({})").format(str(count)))
    else:
        self.lblTitel.set_text(_("Next try ({})").format(str(count)))

    if count == 0:
        # turn vocable cards that were not found
        for card in cards:
            if not card.found:
                card.button.set_sensitive(True)
                card.button.get_child().hide()
                card.turned = False
        # change active player and show colored name on header bar
        player = get_next_active_player()
        text = player.name
        markup = player.get_label_markup(player.color, text)
        self.lblTitel.set_markup(markup)
        return False
    return True


def get_next_active_player():

    global player1, player2, player3, player4

    if player1.active:
        if players_number < 2:
            return player1
        else:
            player1.active = False
            player2.active = True
            return player2
    if player2.active:
        player2.active = False
        if players_number < 3:
            player1.active = True
            return player1
        else:
            player3.active = True
            return player3
    if player3.active:
        player3.active = False
        if players_number < 4:
            player1.active = True
            return player1
        else:
            player4.active = True
            return player4
    if player4.active:
        player4.active = False
        player1.active = True
        return player1


def game_finished(self):

    if player1.score > player2.score and player1.score > player3.score and player1.score > player4.score:
        text = _("{} has won!").format(player1.name)
        markup = player1.get_label_markup(player1.color, text)
    elif player2.score > player1.score and player2.score > player3.score and player2.score > player4.score:
        text = _("{} has won!").format(player2.name)
        markup = player2.get_label_markup(player2.color, text)
    elif player3.score > player1.score and player3.score > player2.score and player3.score > player4.score:
        text = _("{} has won!").format(player3.name)
        markup = player3.get_label_markup(player3.color, text)
    elif player4.score > player1.score and player4.score > player2.score and player4.score > player3.score:
        text = _("{} has won!").format(player4.name)
        markup = player4.get_label_markup(player4.color, text)
    else:
        markup = _("The game ended in a draw!")
    if players_number == 1:
        markup = _("The game is finished!")
    self.lblTitel.set_markup(markup)
    self.btnNewGame.show()


def reset_game(self):

    # delete all child elements in grid
    widgets = self.gridPairs.get_children()
    for widget in widgets:
        self.gridPairs.remove(widget)

    self.lblTitel.set_text("Memoria")
    self.btnNewGame.show()
    self.gridPlayers.hide()
    self.winGame.resize(1,1)


def play_sound(self, file_name):

    from simpleaudio.simpleaudio import WaveObject

    sound_file = os.path.join(SOUNDS_DIR, file_name)
    WaveObject.from_wave_file(sound_file).play()


# initialize main window and manage widgets

class Game(Gtk.Application):

    def __init__(self):

        Gtk.Application.__init__(self)

        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(UI_DIR, 'game.ui'))
        self.builder.connect_signals(self)

        for obj in self.builder.get_objects():
            if issubclass(type(obj), Gtk.Buildable):
                name = Gtk.Buildable.get_name(obj)
                setattr(self, name, obj)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(os.path.join(UI_DIR, 'memoria.css'))
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


    def do_startup(self):

        Gtk.Application.do_startup(self)

        setup_headerbar(self)
        self.abtdlg.set_version(VERSION)


    def do_activate(self):

        self.add_window(self.winGame)
        self.winGame.present()


    # menus and new game button

    def on_menuNew_clicked(self, widget):

        if self.btnNewGame.get_visible():
            reset_game(self)
            show_game_options(self)
        else:
            message_text = _("Do you want to abort the current game?")
            dialog = Gtk.MessageDialog(self.winGame, 0,
                Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, message_text)
            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                reset_game(self)
                show_game_options(self)
            dialog.destroy()


    def on_menuSettings_clicked(self, widget):

        from settings import Settings

        Settings(self.winGame)


    def on_menuEditor_clicked(self, widget):

        from editor import Editor

        Editor(self.winGame)


    def on_menuHelp_clicked(self, widget):

        import webbrowser

        webbrowser.open_new_tab("https://memoria-romaaeterna.readthedocs.io/en/latest/")


    def on_menuAbout_clicked(self, widget):

        self.abtdlg.run()
        self.abtdlg.hide()


    def on_menuQuit_clicked(self, widget):

        if self.btnNewGame.get_visible():
            self.quit()
        else:
            message_text = _("Do you want to quit the application?")
            dialog = Gtk.MessageDialog(self.winGame, 0,
                Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, message_text)
            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                self.quit()
            dialog.destroy()


    def on_btnNewGame_clicked(self, widget):

        reset_game(self)
        show_game_options(self)


    # option popover window

    def on_btnVocabulary_clicked(self, widget):

        from list import load_vocabulary_list, get_vocabulary, get_vocabulary_error
        global voc_unit

        dialog = load_vocabulary_list(self.winGame)

        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            voc_file_path = dialog.get_filename()
            dialog.destroy()
            secondary_text, voc_unit = get_vocabulary(self.listUnits, voc_file_path)
            if secondary_text:
                get_vocabulary_error(voc_file_path, self.winGame, secondary_text)
        else:
            dialog.destroy()


    def on_treeUnits_row_activated(self, widget, path, column):

        self.listUnits[path][0] = not self.listUnits[path][0]


    def on_chkbtnPlayer_toggled(self, widget):

        name = widget.get_property("name")
        if name == "chkbtnPlayer1":
           widget.set_active(True)
        if name == "chkbtnPlayer2":
            if widget.get_active():
                self.colbtnPlayer2.set_sensitive(True)
                self.entPlayer2.set_sensitive(True)
                self.chkbtnPlayer3.set_sensitive(True)
            else:
                self.colbtnPlayer2.set_sensitive(False)
                self.entPlayer2.set_sensitive(False)
                self.chkbtnPlayer3.set_active(False)
                self.chkbtnPlayer3.set_sensitive(False)
                self.colbtnPlayer3.set_sensitive(False)
                self.entPlayer3.set_sensitive(False)
                self.chkbtnPlayer4.set_active(False)
                self.chkbtnPlayer4.set_sensitive(False)
                self.colbtnPlayer4.set_sensitive(False)
                self.entPlayer4.set_sensitive(False)
        if name == "chkbtnPlayer3":
            if widget.get_active():
                self.colbtnPlayer3.set_sensitive(True)
                self.entPlayer3.set_sensitive(True)
                self.chkbtnPlayer4.set_sensitive(True)
            else:
                self.colbtnPlayer3.set_sensitive(False)
                self.entPlayer3.set_sensitive(False)
                self.chkbtnPlayer4.set_active(False)
                self.chkbtnPlayer4.set_sensitive(False)
                self.colbtnPlayer4.set_sensitive(False)
                self.entPlayer4.set_sensitive(False)
        if name == "chkbtnPlayer4":
            if widget.get_active():
                self.colbtnPlayer4.set_sensitive(True)
                self.entPlayer4.set_sensitive(True)
            else:
                self.colbtnPlayer4.set_sensitive(False)
                self.entPlayer4.set_sensitive(False)


    def on_entPlayer_icon_press(self, widget, GTK_ENTRY_ICON_SECONDARY, event):

        widget.set_text("")


    def on_btnOptionsApply_clicked(self, widget):

        from settings import sound
        global voc_active

        setup_game(self)

        number = 0
        if self.chkbtnPlayer4.get_active() and not self.entPlayer4.get_text():
            number = 4
        if self.chkbtnPlayer3.get_active() and not self.entPlayer3.get_text():
            number = 3
        if self.chkbtnPlayer2.get_active() and not self.entPlayer2.get_text():
            number = 2
        if not self.entPlayer1.get_text():
            number = 1
        if number:
            message_text = _("Please type in a name for Player {}!").format(str(number))
            dialog = Gtk.MessageDialog(self.winGame, 0,
                Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, message_text)
            dialog.run()
            dialog.destroy()
            return

        message_text = ""
        unit_chosen = False
        for i in range(len(self.listUnits)):
            if self.listUnits[i][0]:
                unit_chosen = True
                break
        if not unit_chosen:
            message_text = _("You have to choose one unit at least.")
            dialog = Gtk.MessageDialog(self.winGame, 0,
                Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, message_text)
            dialog.run()
            dialog.destroy()
            return

        voc_active = []
        for i in range(len(self.listUnits)):
            if self.listUnits[i][0]:
                for n in range(1,100):
                    if n == self.listUnits[i][2]:
                        voc_active.extend(voc_unit[n])
        if len(voc_active)*2 < cards_number:
            message_text = _("The number of vocables is too small.") + "\n" + \
                _("Please select more units or decrease the number of cards.")
            dialog = Gtk.MessageDialog(self.winGame, 0,
                Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, message_text)
            dialog.run()
            dialog.destroy()
            return

        if sound:
            play_sound(self, 'start.wav')

        headerbar_height = self.headGame.get_preferred_height()
        self.headGame.set_property("height-request", headerbar_height[0])
        self.btnNewGame.hide()
        markup = player1.get_label_markup(player1.color, player1.name)
        self.lblTitel.set_markup(markup)

        build_cards(self)
        self.gridPlayers.show()

        if not Gtk.check_version(3,22,0):
            self.popOptions.popdown()
        else:
            self.popOptions.hide()


    def on_btnOptionsCancel_clicked(self, widget):

        if not Gtk.check_version(3,22,0):
            self.popOptions.popdown()
        else:
            self.popOptions.hide()


    # vocable cards

    def on_btnCard_clicked(self, widget):

        global cards, tries_counter

        # turn vocable card and set active
        widget.set_sensitive(False)
        widget.get_child().show()
        for card in cards:
            if card.button == widget:
                card.turned = True
                break

        # get turned card(s) and check how to go on
        cards_turned = get_turned_cards()
        if len(cards_turned) > 1:
            # update statistical data
            tries_counter += 1
            self.lblTriesCounter.set_text(str(tries_counter))
            # check if pair was found
            if cards_turned in voc_active or cards_turned[::-1] in voc_active:
                pair_found(self)
            else:
                pair_not_found(self)


    # quit game

    def on_winGame_delete_event(self, widget, event):

        if self.btnNewGame.get_visible():
            return False
        else:
            message_text = _("Do you want to quit the application?")
            dialog = Gtk.MessageDialog(self.winGame, 0,
                Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, message_text)
            response = dialog.run()
            dialog.destroy()
            if response == Gtk.ResponseType.YES:
                return False
            else:
                return True


    def on_winGame_destroy(self, game):

        self.quit()
