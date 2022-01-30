
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(80), nullable=True)
