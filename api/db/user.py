from sqlalchemy import delete

from db import Base, Session, db
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    
    email: Mapped[str]
    name: Mapped[str]
  
    
    @staticmethod
    def write(user):
        with Session() as session:
            session.execute(delete(User)) #deletes all rows in the table 
            session.add(user)
            session.commit()
            
    @staticmethod
    def read():
        with Session() as session:
            return session.query(User).one() #used one() so that it returns a User object

    @staticmethod
    def read_all():
        with Session() as session:
            return session.query(User).all() #returns a list containing one element
    def __repr__(self):
        return f"User(email={self.email}, name={self.name})"

target_tables = [Base.metadata.tables['user']]
Base.metadata.create_all(db, tables=target_tables)

