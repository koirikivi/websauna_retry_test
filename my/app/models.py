"""Kaboom models.

Place your SQLAlchemy models in this file.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from websauna.system.model.meta import Base


class MyModel(Base):
    __tablename__ = 'mymodel'
    id = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(Text, default="")
