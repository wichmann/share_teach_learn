
import enum 

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class CategoryType(enum.Enum):
    contentTypes = 1
    schoolTypes = 2
    classes = 3
    subjects = 4

FileCategory = db.Table('FileCategory',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('fileId', db.Integer, db.ForeignKey('File.id')),
    db.Column('categoryId', db.Integer, db.ForeignKey('Category.id')))

class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Enum(CategoryType))
    files = db.relationship('File', secondary=FileCategory, viewonly=True)#, backref='Category'

class File(db.Model):
    __tablename__ = 'File'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    categories = db.relationship('Category', secondary=FileCategory, viewonly=True)#, backref='File'

def initializeCategories():
    db.session.add(Category(name='Arbeitsblätter', type=CategoryType.contentTypes))
    db.session.add(Category(name='Info-Texte', type=CategoryType.contentTypes))
    db.session.add(Category(name='Ergebnissicherung', type=CategoryType.contentTypes))
    db.session.add(Category(name='Grundschule', type=CategoryType.schoolTypes))
    db.session.add(Category(name='Realschule', type=CategoryType.schoolTypes))
    db.session.add(Category(name='Hauptschule', type=CategoryType.schoolTypes))
    db.session.add(Category(name='Berufsschule', type=CategoryType.schoolTypes))
    db.session.add(Category(name='Politik', type=CategoryType.subjects))
    db.session.add(Category(name='Deutsch', type=CategoryType.subjects))
    db.session.add(Category(name='Informatik', type=CategoryType.subjects))
    db.session.add(Category(name='Englisch', type=CategoryType.subjects))
    # 'classes': ['Klasse 1', 'Klasse 2', 'Klasse 3', 'Klasse 4']
    db.session.commit()
