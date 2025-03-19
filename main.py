from config import database, user, password, subd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import create_tables, import_data, get_shops
import json



if __name__ == '__main__':

    DNS = f'{subd}://{user}:{password}@localhost:5432/{database}'
    engine = create_engine(DNS)

    create_tables(engine)




    Session = sessionmaker(bind=engine)
    session = Session()

    with open('fixture/tests_data.json') as f:
        data = json.load(f)

    import_data(session, data)

    id_name = input('Введите Имя или id искомого автора: ')


    get_shops(session, id_name)

    session.close()








