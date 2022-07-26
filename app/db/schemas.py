from ast import For
from unittest.util import _MAX_LENGTH
from db.conn import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())


    def all_columns(self):
        return [c for c in self.__table__.columns]

    def __hash__(self):
        return hash(self.id)

    def create(self, session: Session, auto_commit=False, **kwargs):
        """
        테이블 데이터 적재 전용 함수
        :param session:
        :param auto_commit: 자동 커밋 여부
        :param kwargs: 적재 할 데이터
        :return:
        """
        for col in self.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(self, col_name, kwargs.get(col_name))
        session.add(self)
        session.flush()
        if auto_commit:
            session.commit()
        return self


class Users(Base, BaseMixin):
    __tablename__ = "users"

    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(2000))

    record = relationship("Records", back_populates="user")
    wod = relationship("Wods", back_populates="user")
    wod_time_record = relationship("WodTimeRecords", back_populates="user")
    wod_amrap_record = relationship("WodAmrapRecords", back_populates="user")
    comment = relationship("Comments", back_populates="user")


class Records(Base, BaseMixin):
    __tablename__ = "records"

    exercise_name = Column(String(500), index=True)
    weight = Column(Integer)
    unit = Column(String(200))
    date = Column(DateTime)
    repetition_maximum = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("Users", back_populates="record")


class WodTypes(Base, BaseMixin):
    __tablename__ = "wod_types"

    wod_type_name = Column(String(100))

    wod = relationship("Wods", back_populates="wod_type")
    wod_time_record = relationship("WodTimeRecords", back_populates="wod_type")
    wod_amrap_record = relationship("WodAmrapRecords", back_populates="wod_type")


class Wods(Base, BaseMixin):
    __tablename__ = "wods"

    title = Column(String(100), nullable=False)
    text = Column(String(1000), nullable=False)
    like = Column(Integer())
    view_counts = Column(Integer())
    user_id = Column(Integer, ForeignKey(Users.id))
    wod_type_id = Column(Integer, ForeignKey(WodTypes.id))

    user = relationship("Users", back_populates="wod")
    wod_type = relationship("WodTypes", back_populates="wod")
    wod_time_record = relationship("WodTimeRecords", back_populates="wod")
    wod_amrap_record = relationship("WodAmrapRecords", back_populates="wod")
    comment = relationship("Comments", back_populates="wod")


class WodTimeRecords(Base, BaseMixin):
    __tablename__ = "wod_time_records"
    
    time_record = Column(Integer)
    user_id = Column(Integer, ForeignKey(Users.id))
    wod_id = Column(Integer, ForeignKey(Wods.id))
    wod_type_id = Column(Integer, ForeignKey(WodTypes.id))

    user = relationship("Users", back_populates="wod_time_record")
    wod = relationship("Wods", back_populates="wod_time_record")
    wod_type = relationship("WodTypes", back_populates="wod_time_record")

class WodAmrapRecords(Base, BaseMixin):
    __tablename__ = "wod_amrap_records"

    round_record = Column(Integer)
    reps_record = Column(Integer)
    user_id = Column(Integer, ForeignKey(Users.id))
    wod_id = Column(Integer, ForeignKey(Wods.id))
    wod_type_id = Column(Integer, ForeignKey(WodTypes.id))

    user = relationship("Users", back_populates="wod_amrap_record")
    wod = relationship("Wods", back_populates="wod_amrap_record")
    wod_type = relationship("WodTypes", back_populates="wod_amrap_record")
    

class Comments(Base, BaseMixin):
    __tablename__ = "comments"

    comment = Column(String(500))
    user_id = Column(Integer, ForeignKey(Users.id))
    wod_id = Column(Integer, ForeignKey(Wods.id))

    user = relationship("Users", back_populates="comment")
    wod = relationship("Wods", back_populates="comment")

