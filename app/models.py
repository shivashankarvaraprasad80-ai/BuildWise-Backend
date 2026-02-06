from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    analysis_result = Column(Text, nullable=True)
