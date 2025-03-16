from itertools import count

import sqlalchemy as sq
from sqlalchemy import or_
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref='books')


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)    


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    sq.CheckConstraint(count >= 0, name='count_check')

    books = relationship(Book, backref='stock_book')
    shops = relationship(Shop, backref='stock_shop')

    def __str__(self):
        return f'{self.count}'


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stocks = relationship(Stock, backref='sales')



def create_tables(engine):
    Base.metadata.drop_all(engine)   
    Base.metadata.create_all(engine)


def import_data(session, data):
    creator1 = Creator
    for row in data:
        column = row['fields']
        if row['model'] == 'publisher':
            creator1.create_publisher(session=session, name=column['name'])
        if row['model'] == 'book':
            creator1.create_book(session=session, title=column['title'], id_publisher=column['id_publisher'])
        if row['model'] == 'shop':
            creator1.create_shop(session=session, name=column['name'])
        if row['model'] == 'stock':
            creator1.create_stock(session=session, id_shop=column['id_shop'], id_book=column['id_book'],
                                  count=column['count'])
        if row['model'] == 'sale':
            creator1.create_sale(session=session, price=column['price'], date_sale=column['date_sale'],
                                 count=column['count'], id_stock=column['id_stock'])


class Creator:

    def __init__(self):
        pass


    @staticmethod
    def create_publisher(session, name):
        session.add(Publisher(name=name))
        session.commit()


    @staticmethod
    def create_book(session, title, id_publisher):
        session.add(Book(title=title, id_publisher=id_publisher))
        session.commit()


    @staticmethod
    def create_shop(session, name):
        session.add(Shop(name=name))
        session.commit()


    @staticmethod
    def create_stock(session, id_shop, id_book, count):
        session.add(Stock(id_shop=id_shop, id_book=id_book, count=count))
        session.commit()


    @staticmethod
    def create_sale(session, price, date_sale, count, id_stock):
        stock_count = session.query(Stock).filter(Stock.id == id_stock).all()[0].count
        if stock_count - count >= 0:
            session.add(Sale(price=price, date_sale=date_sale, count=count, id_stock=id_stock))
            session.commit()
        # else:
        #     print(f'Not enough books in this shop {count}')


def find_sales(session, id_name='%'):
    book_list = []
    stock_id_list = []
    result = ''

    if id_name.isdigit():
        id_ = id_name
        name = ''
    else:
        id_ = 0
        name = id_name

    for c in session.query(Book).join(Publisher.books).filter(or_(Publisher.id == id_, Publisher.name == name)).all():
        book_list.append(c.id)

    for c in session.query(Stock).filter(Stock.id_book.in_(book_list)).all():
        stock_id_list.append(c.id)

    for c in session.query(Book.title,
                           Shop.name,
                           Sale.price,
                           Sale.date_sale
                           ).join(Stock.sales).join(Stock.books).join(Stock.shops).filter(Stock.id.in_(stock_id_list)).all():
        result += "{:^20} | {:^10} | {:^7} | {:%d-%m-%Y}".format(c.title, c.name, c.price, c.date_sale) + '\n'

    return result