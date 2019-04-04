from apitest import app
from flask import jsonify, request as req
from apitest.model.zip_codes import Zip_Codes
from sqlalchemy import or_, and_
import apitest.config as config


@app.route("/post_location", methods=["POST"])
def post_location():
    min_lat, max_lat, min_long, max_long = 0, 0, 0, 0
    if req.body['lat']:
        min_lat = float(req.body['lat']) - config.PRECISION
        max_lat = float(req.body['lat']) + config.PRECISION
    if req.body['long']:
        min_long = float(req.body['long']) - config.PRECISION
        max_long = float(req.body['long']) + config.PRECISION

    zip_code = Zip_Codes.query.filter(
        or_(and_(Zip_Codes.latitude >= min_lat, Zip_Codes.latitude <= max_lat),
            and_(Zip_Codes.longitude >= min_long, Zip_Codes.longitude <= max_long),
            Zip_Codes.key == req.body['pincode'])).first()
    if zip_code:
        return jsonify({
            "msg": "zipcode already exists",
            "data": {
                "pincode": zip_code.key,
                "place_name": zip_code.place_name,
                "city_name": zip_code.admin_name1,
                "lat": zip_code.latitude,
                "long": zip_code.longitude,
                "accuracy": zip_code.accuracy
            }
        }), 200
    else:
        return jsonify({
            "msg": "added succesfully"
        }), 200
