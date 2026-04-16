from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:7777@localhost/n75fastdb', echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

