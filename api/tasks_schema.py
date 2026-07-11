import sqlalchemy as sa
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, sessionmaker

db = sa.create_engine("sqlite:///:memory:") #:memory: instead of tasks.db for testing purposes
Session = sessionmaker(bind=db)
Base = declarative_base()
class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    
    prompt: Mapped[str]
    start_at: Mapped[str]
    frequency: Mapped[int]
    task_type: Mapped[str]

    def __repr__(self):
        return f"Task(prompt={self.prompt}, start_at={self.start_at}, frequency={self.frequency}, task_type={self.task_type})"
    
def write_task(task):
    Base.metadata.create_all(db)

    with Session() as session:
        session.add(task)
        session.commit()

def read_tasks():
    Base.metadata.create_all(db)
    with Session() as session:
        return session.query(Task).all()
    
# task = Task(prompt = 'find me nursing jobs at 1pm everyday for 2 weeks', start_at = '09/07/2026 13:00:00', frequency = '14', task_type = 'job_finder')
# write_task(task)
# print(read_tasks())