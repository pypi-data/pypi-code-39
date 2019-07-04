"""Document represents rendered instance of template."""
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship


class Document:
    id = Column(Integer, primary_key=True)
    document_text = Column(Text, required=True)
    template_id = Column(Integer, ForeignKey("template.id", ondelete="CASCADE"))
    template = relationship('Template')

