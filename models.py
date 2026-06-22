from sqlalchemy import Column, Integer, String, Text, Boolean
from database import Base

#Blog Table 
class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True,index=True)
    title = Column(String(100))
    content = Column(Text)
    is_active = Column(Boolean, default=True)