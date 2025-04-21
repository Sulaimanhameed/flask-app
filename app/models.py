from app import db
from datetime import datetime
from sqlalchemy import Numeric

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(30))
    price = db.Column(Numeric(10, 2))
    description = db.Column(db.Text, default='No description')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Car('{self.make}', '{self.model}', {self.year})"
