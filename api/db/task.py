from db import Base, Session, db
from sqlalchemy.orm import Mapped, mapped_column

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    
    prompt: Mapped[str]
    start_at: Mapped[str]
    frequency: Mapped[int]
    task_type: Mapped[str]
    
    @staticmethod
    def write(task):
        with Session() as session:
            session.add(task)
            session.commit()
            
    @staticmethod
    def read():
        with Session() as session:
            return session.query(Task).all()

    def __repr__(self):
        return f"Task(prompt={self.prompt}, start_at={self.start_at}, frequency={self.frequency}, task_type={self.task_type})"
target_tables = [Base.metadata.tables['tasks']]
Base.metadata.create_all(db, tables=target_tables)
