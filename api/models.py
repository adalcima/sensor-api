import time

from api import db


class Reading(db.Model):
    __tablename__ = 'readings'

    id = db.Column(db.Integer, primary_key=True)
    device_uuid = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Integer, default=0)
    date_created = db.Column(db.Integer, default=int(time.time()))
