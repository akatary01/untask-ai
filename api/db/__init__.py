import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, mapped_column, sessionmaker

db = sa.create_engine("sqlite:///tasks.db") #:memory: instead of tasks.db for testing purposes
Session = sessionmaker(bind=db)
Base = declarative_base()