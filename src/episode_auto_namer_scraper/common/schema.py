from sqlalchemy import Column, Date, ForeignKey, Integer, Text, String
from sqlalchemy.orm import relationship
from episode_auto_namer_scraper.common.Database import Base

class Title(Base):
    """Title Table Definition"""
    __tablename__ = 'title'
    titleId = Column(Integer, primary_key=True, nullable=False)
    titleIMDBId = Column(Integer)
    title = Column(String(64), unique=True, nullable=False)
    originalTitle = Column(String(64), unique=True)
    episodes = relationship("Episode")
    titleSynopsis = Column(Text)
    titleOriginalSynopsis = Column(Text)
    network = Column(Text)


class Episode(Base):
    """Episode Table Definition"""
    __tablename__ = 'episode'
    titleId = Column(Integer, ForeignKey('title.titleId'), nullable=False)
    episodeId = Column(Integer, primary_key=True, nullable=False)
    episodeIMDBId = Column(Integer)
    seasonNumber = Column(Integer)
    episodeNumber = Column(Integer)
    episodeTitle = Column(Text, nullable=False)
    episodeOriginalTitle = Column(String(64), unique=True)
    episodeSynopsis = Column(Text)
    episodeOriginalSynopsis = Column(Text)
    episodeAired = Column(Date)
