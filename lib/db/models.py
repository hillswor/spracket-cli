from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import ipdb

Base = declarative_base()
# engine = create_engine("sqlite:///db.sqlite3")
# Session = sessionmaker(bind=engine)
# session = Session()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)

    __table_args__ = (
        UniqueConstraint("username", name="uq_username"),
        UniqueConstraint("email", name="uq_email"),
    )

    def __repr__(self):
        return "<User(username='%s', email='%s')>" % (self.username, self.email)


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
