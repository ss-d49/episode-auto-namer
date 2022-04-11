from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from .schema import Title, Episode, base

def create_connection():
	engine = create_engine(
	    "mariadb+pymysql://root:root@localhost:3306/media2")
	metadata = MetaData(engine)
	Session = sessionmaker()
	Session.configure(bind=engine)
	session = Session()
	base.metadata.create_all(engine)
	return session
