from sqlalchemy import Column, BigInteger, String, sql
from utils.db_api.database_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))

    query: sql.Select
