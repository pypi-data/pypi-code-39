"""Document represents rendered instance of template."""
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
import pdfkit
from themis_doc.pdf_storage import PDFStorage


class Document:
    id = Column(Integer, primary_key=True)
    document_text = Column(Text, nullable=False)
    template_id = Column(Integer, ForeignKey("template.id", ondelete="CASCADE"))
    template = relationship('Template')

    def render_to_pdf(self):
        return pdfkit.from_string(self.document_text, False)

    def store(self):
        raise NotImplemented()