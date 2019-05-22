
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Plant(Base):
    __tablename__ = 'plant'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    category = Column(String(50))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category
        }


engine = create_engine('sqlite:///plants.db')
Base.metadata.create_all(engine)
