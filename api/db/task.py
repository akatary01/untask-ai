from enum import Enum
from datetime import datetime
from db import Base, Session, db
from sqlalchemy.orm import Mapped, mapped_column

class TaskType(Enum):
    JOB_FINDER = "job-finder"
    
class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    
    prompt: Mapped[str]
    frequency: Mapped[int]
    start_at: Mapped[datetime]
    task_type: Mapped[TaskType]
    
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

if __name__ == "__main__":
    Task.write(Task(prompt = 'find me nursing jobs at 1pm everyday for 2 weeks', start_at = datetime(2026, 7, 9, 13), frequency = 14, task_type = TaskType.JOB_FINDER))
    print(Task.read())