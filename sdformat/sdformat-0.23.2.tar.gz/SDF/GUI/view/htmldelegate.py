from PyQt5 import QtCore
from PyQt5.QtWidgets import (QTextDocument, QStyledItemDelegate,
                             QAbstractTextDocumentLayout)
                             


class HTMLDelegate(QStyledItemDelegate):
    """
    The following class was copied and slightly adapted from posts by
    stackoverflow.com users Giorgio Gelardi and Kalbe Pederson 
    in this thread: 
    http://stackoverflow.com/questions/2959850/how-to-make-item-view-render-rich-html-text-in-pyqt
    """
    def paint(self, painter, option, index):
        model = index.model()
        record = model.data(index)
        doc = QTextDocument(self)
        # doc.setHtml(get_html_box(record))
        doc.setHtml(record)
        doc.setTextWidth(option.rect.width())
        ctx = QAbstractTextDocumentLayout.PaintContext()

        painter.save()
        painter.translate(option.rect.topLeft())
        painter.setClipRect(option.rect.translated(-option.rect.topLeft()))
        dl = doc.documentLayout()
        dl.draw(painter, ctx)
        painter.restore()
    
    def sizeHint(self, option, index):
        model = index.model()
        record = model.data(index)
        doc = QTextDocument(self)
        # doc.setHtml(get_html_box(record))
        doc.setHtml(record)
        doc.setTextWidth(option.rect.width())
        return QtCore.QSize(doc.idealWidth(), doc.size().height())
