from sqlalchemy import create_engine, Column, String, Integer, DATETIME, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()
engine = create_engine("sqlite:///./todo.db", echo=True)
session = sessionmaker(bind=engine)



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    todos = relationship("Todos", back_populates="user")




class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    time = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    username = Column(String, ForeignKey('users.username'), nullable=False)


    user = relationship('User', back_populates="todos")



Base.metadata.create_all(engine)



