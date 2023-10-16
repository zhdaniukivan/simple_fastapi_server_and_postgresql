from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    id_questions = Column(Integer)
    question_text = Column(String, index=True)
    answer_text = Column(String)
    create_date = Column(DateTime, default=datetime.utcnow)