import sys
import os.path
# #import PyQt5
import json
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication
from .window import Ui_MainWindow


standart_note_path = os.path.join(Path().home(), "Notes", "note_files")
standart_file_path = os.path.join(Path().home(), "Notes")
main_script_path = os.path.split(os.path.abspath(__file__))[0]


def check_path(path):
    if not os.path.exists(path):
        levels = path.split(os.path.sep)
        if not levels[0]:
            p = '/'
        elif levels[0].endswith(":"):
            p = levels[0] + os.path.sep
        else:
            p = levels[0]
        for l in levels[1:]:
            p = os.path.join(p, l)
            if not os.path.exists(p):
                os.mkdir(p)
                print(p)
            print(os.path.exists(p))


class Note(QtWidgets.QListWidgetItem):
    def __init__(self, text="", name="Новая заметка", path=False):
        super().__init__(name)
        self.name = name
        self.text = text
        if not path:
            path = os.path.join(standart_note_path, name)
        if not os.path.exists(standart_note_path):
            os.mkdir(standart_note_path)
        '''if os.path.exists(path):
            i = 1
            while os.path.exists(path):
                path = os.path.join(standart_note_path, self.name + str(i))
                i += 1'''
        self.name = self.name  # #+ str(i)
        self.path = path


class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.note = False
        self.notes = []
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self, self.save_note)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+N"), self, self.new_note)
        self.notes_list.itemClicked.connect(self.set_current_note)
        self.new_button.clicked.connect(self.new_note)
        self.del_button.clicked.connect(self.del_note)
        self.italicButton.clicked.connect(lambda: self.setTextStyle("Italic"))
        self.boldButton.clicked.connect(lambda: self.setTextStyle("Bold"))
        self.underButton.clicked.connect(lambda: self.setTextStyle("Under"))
        self.fontsizeSpinBox.valueChanged.connect(lambda x: self.setTextStyle({"size": x}))
        self.fontSelector.currentFontChanged.connect(lambda x: self.setTextStyle({"family": x}))
        self.textEdit.currentCharFormatChanged.connect(self.change_styles)
        #self.textEdit.cursorPositionChanged.connect(self.change_styles)
        self.markedList.clicked.connect(lambda: self.addList(-1))
        self.numList.clicked.connect(lambda: self.addList(-4))
        self.alignLeftButton.clicked.connect(lambda: self.setAligment('l'))
        self.alignCenterButton.clicked.connect(lambda: self.setAligment('c'))
        self.alignRightButton.clicked.connect(lambda: self.setAligment('r'))
        self.textEdit.cursorPositionChanged.connect(self.check_aligment)
        self.get_notes()

    def check_aligment(self):
        cursor = self.textEdit.textCursor()
        fmt = cursor.blockFormat()
        alignment = fmt.alignment()
        if alignment == QtCore.Qt.AlignLeft:
            self.alignLeftButton.setChecked(True)
            self.alignRightButton.setChecked(False)
            self.alignCenterButton.setChecked(False)
        elif alignment == QtCore.Qt.AlignRight:
            self.alignLeftButton.setChecked(False)
            self.alignRightButton.setChecked(True)
            self.alignCenterButton.setChecked(False)
        elif alignment == QtCore.Qt.AlignCenter:
            self.alignLeftButton.setChecked(False)
            self.alignRightButton.setChecked(False)
            self.alignCenterButton.setChecked(True)


    def setAligment(self,aligment):
        cursor = self.textEdit.textCursor()
        block_format = QtGui.QTextBlockFormat()
        if aligment == 'l':
            block_format.setAlignment(QtCore.Qt.AlignLeft)
        elif aligment == 'c':
            block_format.setAlignment(QtCore.Qt.AlignCenter)
        elif aligment == 'r':
            block_format.setAlignment(QtCore.Qt.AlignRight)
        block = cursor.setBlockFormat(block_format)
        self.check_aligment()

    def change_styles(self, data):
        #data = self.textEdit.textCursor().blockCharFormat()
        self.italicButton.setChecked(data.fontItalic())
        self.fontsizeSpinBox.setValue(data.fontPointSize())
        self.underButton.setChecked(data.fontUnderline())
        print(data.fontWeight())
        self.boldButton.setChecked(1 if data.fontWeight() > 50 else 0)
        self.fontSelector.setCurrentFont(QtGui.QFont(data.fontFamily()))

    def del_note(self, b):
        for item in self.notes_list.selectedItems():
            name = self.notes_list.takeItem(self.notes_list.row(item)).text()
            # #print(dir(name))
            path = os.path.join(standart_note_path, name)
            # #print(path)
            os.remove(path)

    def set_current_note(self, item):
        #self.save_note()
        p = os.path.join(standart_note_path, item.text())
        self.load_note(p)
        self.show_note(self.note)

    def get_notes(self):
        for note_name in os.listdir(standart_note_path):
            self.notes.append(Note(text="",
                                   name=note_name,
                                   path=os.path.join(standart_note_path, note_name)))
            self.notes_list.addItem(QtWidgets.QListWidgetItem(note_name))
        #self.load_note(self.notes[0].path)

    def save_note(self):
        if not self.note:
            name, ok = QtWidgets.QInputDialog.getText(self, "Введите название заметки", "Название:")
            path = os.path.join(standart_note_path, name)
            self.note = Note("", name, path)
            self.notes.append(self.note)
            self.notes_list.addItem(QtWidgets.QListWidgetItem(self.note.name))
        with open(self.note.path, 'w') as file:
            text = self.textEdit.toHtml()
            print(text)
            file.write(text)

    def show_note(self, note):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontFamily("Arial")
        fmt.setFontPointSize(12)
        self.textEdit.setCurrentCharFormat(fmt)
        self.textEdit.setHtml(note.text)
        # #print(self.textEdit.toHtml())

    def load_note(self, path):
        name = os.path.basename(path)
        with open(path) as file:
            text = file.read()
        # #print(type(Note()))
        self.note = Note(text, name, path)
        # #self.show_note(self.note)

    def new_note(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Введите название заметки", "Название:")
        path = os.path.join(standart_note_path, name)
        if ok:
            open(path, 'w').close()
            '''self.notes.append(Note(text="",
                                   name=name,
                                   path=path))'''
            self.notes_list.addItem(QtWidgets.QListWidgetItem(name))
            self.load_note(path)

    def setTextStyle(self, style):
        cursor = self.textEdit.textCursor()
        cursor.setKeepPositionOnInsert(False)
        char_format = cursor.charFormat()
        if cursor.hasSelection():
            if style == "Italic":
                char_format.setFontItalic(not char_format.fontItalic())
            elif style == "Bold":
                char_format.setFontWeight(50 if char_format.fontWeight() >= 99 else 99)
            elif style == "Under":
                char_format.setFontUnderline(not char_format.fontUnderline())
            elif style.get("size"):
                char_format.setFontPointSize(style["size"])
            elif style.get("family"):
                char_format.setFontFamily(style["family"].family())
            cursor.setCharFormat(char_format)
        '''else:
            span = "<span style=\"{}\">1</span>"
            if style == "Italic":
                span = span.format("")
            elif style == "Bold":
                span = span.format("")
            elif style == "Under":
                span = span.format("text-decoration: underline;")
            elif style.get("size"):
                span = span.format("")
            elif style.get("family"):
                span = span.format("")
            cursor.insertHtml(span)'''

    def addList(self, style):
        cursor = self.textEdit.textCursor()
        qlist = QtGui.QTextListFormat()
        qlist.setStyle(style)
        cursor.createList(qlist)

    def setIcons(self):
        pathes = [
            "center-alignment.png",
            "right-alignment.png",
            "left-alignment.png",
            "plus.png",
            "minus.png"
        ]
        buttons = [
            self.alignCenterButton,
            self.alignRightButton,
            self.alignLeftButton,
            self.new_button,
            self.del_button
        ]
        for p, b in zip(pathes, buttons):
            print(os.path.join(main_script_path, p))
            full_path = os.path.join(main_script_path.split()[0], "imgs", p)
            b.setIcon(QtGui.QIcon(full_path))


def make_usercfg(cfg_path):
    with open(cfg_path, "w") as cfg_file:
        cfg = {
            "note_path": standart_note_path,
            "file_path": standart_file_path
        }
        json.dump(cfg, cfg_file)


def main():
    global standart_note_path
    global standart_file_path

    cfg_path = os.path.join(standart_file_path, "user.cfg")
    check_path(standart_file_path)
    check_path(standart_note_path)
    if not os.path.exists(os.path.join(standart_file_path, "user.cfg")):
        make_usercfg(cfg_path)
    with open(cfg_path) as cfg_file:
        cfg = json.load(cfg_file)
    standart_note_path = cfg["note_path"]
    standart_file_path = cfg["file_path"]

    app = QApplication(sys.argv)
    window = Window()
    window.setIcons()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
