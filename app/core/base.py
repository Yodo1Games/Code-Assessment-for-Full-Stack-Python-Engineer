from sqlalchemy import Integer, Column
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Column(Integer, primary_key=True, autoincrement=True)
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self):
        """returns a dictionary representation of the object"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
