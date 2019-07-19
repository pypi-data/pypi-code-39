from sqlalchemy import (
    Column,
    DateTime,
    Float,
    # ForeignKey,
    Integer,
    Unicode,
)
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# create an instance of the declarative base class, to be used across all models
Base = declarative_base()


# ------------------------------------------------------------------------------
class Detection(Base):
    """
    Mapped class for object detection events.
    """

    __tablename__ = "detections"

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # attributes
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())
    category = Column(Unicode(255))
    probability = Column(Float)
    start_x = Column(Integer)
    start_y = Column(Integer)
    end_x = Column(Integer)
    end_y = Column(Integer)

    # # many-to-one relationship (i.e. we may have
    # # multiple detections per video frame image)
    # detection_image_id = Column(Integer, ForeignKey("detection_images.id"))
    # detection_image = relationship("DetectionImage",
    #                                foreign_keys=[detection_image_id])

    # simple representation
    def __repr__(self):
        return f"<Detection(id={self.id}, " + \
               f"created={self.created}, updated={self.updated}, " + \
               f"category={self.category}, probability={self.probability}, " + \
               f"bounding box=(x0={self.start_x}, y0={self.start_y}, " + \
               f"x1={self.end_x}, y1={self.end_y}))>"
