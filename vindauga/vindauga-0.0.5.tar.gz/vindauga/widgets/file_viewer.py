# -*- coding: utf-8 -*-
import itertools
import logging
import textwrap

from vindauga.types.collections.collection import Collection
from vindauga.constants.message_flags import mfError, mfOKButton
from vindauga.constants.grow_flags import gfGrowHiX, gfGrowHiY
from vindauga.constants.state_flags import sfExposed
from vindauga.dialogs.message_box import messageBox
from vindauga.types.draw_buffer import DrawBuffer

from .scroller import Scroller

logger = logging.getLogger('vindauga.widgets.file_viewer')


class FileViewer(Scroller):
    name = 'FileViewer'

    def __init__(self, bounds, hScrollBar, vScrollBar, fileName, wrap=True):
        super().__init__(bounds, hScrollBar, vScrollBar)
        self.growMode = gfGrowHiX | gfGrowHiY
        self.fileLines = None
        self.isValid = True
        self.fileName = fileName
        self.wrap = wrap
        self.readFile(fileName)

    def draw(self):
        c = self.getColor(0x0301)
        for i in range(self.size.y):
            b = DrawBuffer()
            b.moveChar(0, ' ', c, self.size.x)
            if self.delta.y + i < len(self.fileLines):
                p = self.fileLines[self.delta.y + i]
                if (not p) or len(p) < self.delta.x:
                    s = ''
                else:
                    s = p[self.delta.x: self.delta.x + self.size.x].rstrip()
                b.moveStr(0, s, c)
            self.writeBuf(0, i, self.size.x, 1, b)

    def scrollDraw(self):
        super().scrollDraw()
        self.draw()

    def readFile(self, fName):
        self._limit.x = 0
        self.fileName = fName
        self.fileLines = Collection()

        try:
            fileToView = open(fName, 'rt', encoding='utf-8')
        except OSError:
            messageBox(_('Invalid drive or directory'), 1, mfError | mfOKButton)
            self.isValid = False
            return

        lines = fileToView.readlines()
        if self.wrap:
            wrapped = (textwrap.wrap(l + '\n', self.size.x - 1, expand_tabs=True, tabsize=4) for l in lines)
            lines = itertools.chain(*wrapped)

        self.fileLines.extend(lines)
        self._limit.y = len(self.fileLines)
        if self.fileLines:
            self._limit.x = max(len(l) for l in self.fileLines)

    def setState(self, state, enable):
        super().setState(state, enable)
        if enable and (state & sfExposed):
            self.setLimit(self._limit.x, self._limit.y)

    def valid(self, command):
        return self.isValid
