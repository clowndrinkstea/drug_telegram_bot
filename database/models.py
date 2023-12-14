from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column("id", Integer, primary_key=True)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class User(BaseModel):
    __tablename__ = 'users'

    telegram_id = Column("telegram_id", Integer, nullable=True)
    chat_id = Column("chat_id", Integer, nullable=False)
    meta = Column('meta', String(255), nullable=False)


class Notification(BaseModel):
    __tablename__ = 'notifications'

    start_date = Column('start_date', DateTime, nullable=False)
    notification_hour = Column('notification_hour', Integer, nullable=False)
    notification_minute = Column('notification_minute', Integer, nullable=False)
    drug_name = Column('drug_name', String(255), nullable=False)
    drug_type = Column('drug_type', String(255), nullable=False, default='')
    amount = Column('amount', Integer, nullable=False)
    end_date = Column('end_date', DateTime, nullable=False)
    period = Column('period', Integer, nullable=True, default=-1)

    user_id = Column(Integer, ForeignKey('users.id'))
