from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    sig1_path = db.Column(db.String(255))
    sig2_path = db.Column(db.String(255))
    sig3_path = db.Column(db.String(255))
    sig4_path = db.Column(db.String(255))
    # configuration for fields (position, font size, font family)
    config = db.Column(db.JSON, default={})

class ExcelColumn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_hindi = db.Column(db.Boolean, default=False)

class ExcelRow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)
