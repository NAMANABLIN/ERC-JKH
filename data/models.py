from sqlalchemy import Column, Integer, \
    String, ForeignKey, Boolean, orm
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select

from data.database import Base, async_db_session


class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        async_db_session.add(cls(**kwargs))
        await async_db_session.commit()

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result


class User(Base, ModelAdmin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    address = Column(String)
    is_operator = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    HD_of_the_tenant = Column(String)
    waiting_for_operator = Column(Boolean, default=False)
    operator = Column(Integer, default=0)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"address={self.address}, "
            f"is_operator={self.is_operator}, "
            f"is_admin={self.is_admin}, "
            f"HD_of_the_tenant={self.HD_of_the_tenant}"
            f")>"
        )


class Operator(Base, ModelAdmin):
    __tablename__ = "operators"

    id = Column(Integer,  ForeignKey('users.id'), primary_key=True)
    HD_of_the_operator = Column(String)

    user = orm.relationship('User')

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"HD_of_the_operator={self.HD_of_the_operator}"
            f")>"
        )

