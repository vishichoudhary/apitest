from apitest import db


class Zip_Codes(db.Model):
    __tablename__ = 'zipcodes'
    key = db.Column(db.String(10), primary_key=True)
    place_name = db.Column(db.String(200), unique=False, nullable=True)
    admin_name1 = db.Column(db.String(200), unique=False, nullable=True)
    latitude = db.Column(db.Float, unique=False, nullable=True)
    longitude = db.Column(db.Float, unique=False, nullable=True)
    accuracy = db.Column(db.Integer, unique=False, nullable=True)
