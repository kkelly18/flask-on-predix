from datetime import datetime
from . import db


class DataPoint(db.Model):
    __tablename__ = 'time_series'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    value = db.Column(db.String(64))

    def to_json(self):
        json_data_point = {
            'name': self.name,
            'timestamp': self.timestamp,
            'value': self.value
        }
        return json_data_point

    def __repr__(self):
        return self.to_json()
