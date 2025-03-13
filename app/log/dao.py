from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.log.model import Log
from sqlalchemy import and_, or_


class LogDAO:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def save_log(self, created_at: datetime, log_level: str, log_data: str) -> Log:
        new_log = Log(created_at=created_at, log_level=log_level, log_data=log_data)
        self.db.session.add(new_log)
        self.db.session.commit()
        return new_log

    def get_all_logs(self) -> list[Log]:
        return self.db.session.query(Log).all()

    def get_logs_by_time(self, start_time: datetime, end_time: datetime):
        return self.db.session.query(Log).filter(and_(Log.created_at > start_time, Log.created_at < end_time)).all()

    def get_logs_by_fragment(self, fragment: str):
        return self.db.session.query(Log).filter(or_(Log.log_data.like(f"%{fragment}%"),
                                                     Log.log_level.like(f"%{fragment}%"))).all()

    def get_logs_by_fragment_and_by_time(self, fragment: str, start_time: datetime, end_time: datetime):
        return self.db.session.query(Log).filter(and_(Log.created_at > start_time,
                                                      Log.created_at < end_time,
                                                      or_(Log.log_data.like(f"%{fragment}%"),
                                                          Log.log_level.like(f"%{fragment}%")))).all()
