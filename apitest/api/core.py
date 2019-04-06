from apitest import app, db
from flask import jsonify, request as req
from apitest.model.zip_codes import Zip_Codes
from sqlalchemy import or_, and_
from sqlalchemy.sql import func
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
            and_(Zip_Codes.longitude >= min_long,
                 Zip_Codes.longitude <= max_long),
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


@app.route('/get_using_postgres', methods=["GET"])
def get_using_postgres():
    reqLat = req.args.get('lat')
    reqLong = req.args.get('long')
    dist = req.args.get('dist')
    result = db.engine.execute(
        "select *  from (select *,(point(latitude, longitude)<@>point({}, {}))*1.609344 as dist from {}) t where dist <= {};".format(reqLat, reqLong, config.DB_TABLENAME, dist))
    data = []
    for value in result:
        tempData = {}
        tempData["key"] = value.key
        tempData["place_name"] = value.place_name
        tempData["city_name"] = value.admin_name1
        tempData["lat"] = value.latitude
        tempData["long"] = value.longitude
        tempData["accuracy"] = value.accuracy
        data.append(tempData)

    return jsonify({
        "msg": "all the nearby pin codes ",
        "data": data
    }), 200


@app.route('/get_using_self', methods=["GET"])
def get_using_self():
    reqLat = req.args.get('lat')
    reqLong = req.args.get('long')
    dist = req.args.get('dist')
    result = db.engine.execute("SELECT * FROM (  SELECT *, (((acos(sin(({}*pi()/180)) * sin((latitude*pi()/180))+cos(({}*pi()/180)) * cos((latitude*pi()/180)) * cos((({} - longitude)*pi()/180))))*180/pi())*60*1.1515*1.609344) as distance FROM {}) t WHERE distance <= {};".format(reqLat, reqLat, reqLong, config.DB_TABLENAME, dist))
    data = []
    for value in result:
        tempData = {}
        tempData["key"] = value.key
        tempData["place_name"] = value.place_name
        tempData["city_name"] = value.admin_name1
        tempData["lat"] = value.latitude
        tempData["long"] = value.longitude
        tempData["accuracy"] = value.accuracy
        data.append(tempData)

    return jsonify({
        "msg": "all the nearby pin codes ",
        "data": data
    }), 200
