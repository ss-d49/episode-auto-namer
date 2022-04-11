from sqlalchemy import Column, Date, ForeignKey, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()

class Title(base):
    """Title Table Definition"""
    __tablename__ = 'title'
    titleId = Column(Integer, primary_key=True, nullable=False)
    titleIMDBId = Column(Integer)
    title = Column(Text, unique=True, nullable=False)
    originalTitle = Column(Text, unique=True)
    episodes = relationship("Episode")
    titleSynopsis = Column(Text)
    titleOriginalSynopsis = Column(Text)
    network = Column(Text)


class Episode(base):
    """Episode Table Definition"""
    __tablename__ = 'episode'
    titleId = Column(Integer, ForeignKey('title.titleId'), nullable=False)
    episodeId = Column(Integer, primary_key=True, nullable=False)
    episodeIMDBId = Column(Integer)
    seasonNumber = Column(Integer)
    episodeNumber = Column(Integer)
    episodeTitle = Column(Text, nullable=False)
    episodeOriginalTitle = Column(Text, unique=True)
    episodeSynopsis = Column(Text)
    episodeOriginalSynopsis = Column(Text)
    episodeAired = Column(Date)
