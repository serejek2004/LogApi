from datetime import datetime
from app.database import db


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    log_level = db.Column(db.String(10), nullable=False)
    log_data = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"[{self.created_at}] {self.log_level}: {self.message}"

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "log_level": self.log_level,
            "log_data": self.log_data,
        }
