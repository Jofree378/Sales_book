from config import database, user, password, subd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import create_tables
import json

dns = f'{subd}://{user}:{password}@localhost:5432/{database}'
engine = create_engine(dns)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixture/tests_data.json') as f:
    data = json.load(f)
    



session.close()







