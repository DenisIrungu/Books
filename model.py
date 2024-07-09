from sqlalchemy import Column,String,Boolean,Integer,Float
from database import Base

class Book(Base):
    __tablename__= "books"
    id= Column(Integer, primary_key= True, index=True)
    title=Column(String (50))
    author= Column(String(50))
    description= Column(String(50))
    rating= Column(Float)
