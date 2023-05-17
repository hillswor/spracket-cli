from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import ipdb

Base = declarative_base()
engine = create_engine("sqlite:///db.sqlite3")
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    address = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name,
            self.first_name,
            self.last_name,
            self.email,
            self.address,
        )


class Bike(Base):
    __tablename__ = "bikes"

    id = Column(Integer, primary_key=True)
    manufacturer = Column(String)
    model = Column(String)
    year = Column(Integer)

    def __repr__(self):
        return "<Bike(manufacturer='%s', model='%s')>" % (
            self.manaufacturer,
            self.model,
        )
