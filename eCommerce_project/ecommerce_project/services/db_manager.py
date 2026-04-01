from services.models import Base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from config import config
from config import config

class DBManager:
    def __init__(self):
        database_url = config.SQLALCHEMY_DATABASE_URI
        self.engine = create_engine(database_url, echo=False)  
        self.metadata = MetaData()
        self.create_all_tables()
        self.Session = sessionmaker(self.engine)
        

    def create_all_tables(self):
        Base.metadata.create_all(self.engine)