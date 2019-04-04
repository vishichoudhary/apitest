from apitest import app
from flask import jsonify, request as req
from apitest.model.zip_codes import Zip_Codes


@app.route("/post_location", methods=["POST"])
def post_location():
    zip_code = Zip_Codes.query.filter_by(key=req.body['pincode']).first()
    if zip_code:
        return jsonify({
            "msg": "pincode already exists"
        }), 200
    else:
        return jsonify({
            "msg": "added succesfully"
        }), 200
