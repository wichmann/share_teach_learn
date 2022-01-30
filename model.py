
import uuid
import enum

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class CategoryType(enum.Enum):
    contentTypes = 1
    schoolTypes = 2
    classes = 3
    subjects = 4


class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Enum(CategoryType))
    files = db.relationship('File', secondary='FileCategory', back_populates='categories') #, back_populates='Category.')#, backref='Category'


class File(db.Model):
    __tablename__ = 'File'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    uuid = db.Column(db.String(40), unique=True)
    categories = db.relationship('Category', secondary='FileCategory', back_populates='files') #, lazy='subquery', backref=db.backref('files', lazy=True))


FileCategory = db.Table('FileCategory',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('fileId', db.Integer, db.ForeignKey('File.id')),
    db.Column('categoryId', db.Integer, db.ForeignKey('Category.id')))


def initializeCategories():
    c1 = Category(name='Arbeitsblätter', type=CategoryType.contentTypes)
    db.session.add(c1)
    c2 = Category(name='Info-Texte', type=CategoryType.contentTypes)
    db.session.add(c2)
    c3 = Category(name='Ergebnissicherung', type=CategoryType.contentTypes)
    db.session.add(c3)
    c4 = Category(name='Grundschule', type=CategoryType.schoolTypes)
    db.session.add(c4)
    c5 = Category(name='Realschule', type=CategoryType.schoolTypes)
    db.session.add(c5)
    c6 = Category(name='Hauptschule', type=CategoryType.schoolTypes)
    db.session.add(c6)
    c7 = Category(name='Berufsschule', type=CategoryType.schoolTypes)
    db.session.add(c7)
    c8 = Category(name='Politik', type=CategoryType.subjects)
    db.session.add(c8)
    c9 = Category(name='Deutsch', type=CategoryType.subjects)
    db.session.add(c9)
    c10 = Category(name='Informatik', type=CategoryType.subjects)
    db.session.add(c10)
    c11 = Category(name='Englisch', type=CategoryType.subjects)
    db.session.add(c11)
    # 'classes': ['Klasse 1', 'Klasse 2', 'Klasse 3', 'Klasse 4']
    #
    new_uuid = uuid.uuid4()
    db.session.add(File(filename='datei1.jpg', uuid=new_uuid.hex, description='Ein Bild eines kleinen Hundes.',categories=[c1, c4]))
    new_uuid = uuid.uuid4()
    db.session.add(File(filename='datei2.pdf', uuid=new_uuid.hex, description='Ein Dokument mit einer Katze. Ein Dokument mit einer Katze. Ein Dokument mit einer Katze. Ein Dokument mit einer Katze.',categories=[c2, c5]))
    new_uuid = uuid.uuid4()
    db.session.add(File(filename='ein_langer_dateiname_vom_benutzer.odt', uuid=new_uuid.hex, description='Eine lange Datei.', categories=[c1, c7]))
    new_uuid = uuid.uuid4()
    db.session.add(File(filename='ein_benutzer.odt', uuid=new_uuid.hex, description='Eine llkdfjg lsfdgjklsfjd klgjslfdk glksfd klgjlksdfg kldsfklange Datei.',categories=[c2, c4]))
    new_uuid = uuid.uuid4()
    db.session.add(File(filename='dateiname_xyz.odt', uuid=new_uuid.hex, description='Eine sklgfjdgl jslkdfj gljlkfsdjg lksjdflkgj klsdfjglksdfklgj lksdfjklg lange Datei.', categories=[c2, c7]))
    new_uuid = uuid.uuid4()
    db.session.add(File(filename='Arbeitsblatt.pdf', uuid=new_uuid.hex, description='Eine lange Datei.', categories=[c3, c5]))
    db.session.commit()
