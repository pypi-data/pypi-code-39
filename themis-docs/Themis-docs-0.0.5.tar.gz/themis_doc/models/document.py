"""Document represents rendered instance of template."""
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import pdfkit


class Document:
    id = Column(Integer, primary_key=True)
    document_text = Column(Text, nullable=False)
    template_id = Column(Integer, ForeignKey("template.id", ondelete="CASCADE"))
    template = relationship('Template')
    variables = Column(JSONB)

    def render_to_pdf(self):
        return pdfkit.from_string(self.document_text, False)

    def store_as_pdf(self):
        raise NotImplemented()
