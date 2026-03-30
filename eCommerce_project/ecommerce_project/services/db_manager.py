from services.models import Base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    def __init__(self):
        database_url = os.getenv('DATABASE_URL')
        self.engine = create_engine(database_url, echo=False)  
        self.metadata = MetaData()
        self.create_all_tables()
        self.Session = sessionmaker(self.engine)

    def create_all_tables(self):
        Base.metadata.create_all(self.engine)

