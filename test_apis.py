from run import app
import json


def test_get_using_postgres():
    response = app.test_client().get('/get_using_postgres?lat=28.55&long=77.61&dist=3')
    assert response.status_code == 200


def test_get_using_self():
    response = app.test_client().get('/get_using_self?lat=28.55&long=77.61&dist=3')
    assert response.status_code == 200


def test_post_location():
    headers = {
        'ContentType': 'application/json',
        'dataType': 'json'
    }
    data = {
        "lat": "28.633",
        "long": "77.216",
        "pincode": "IN/11001",
        "address": "",
        "city": ""
    }
    response = app.test_client().post('/post_location',
                                      data=json.dumps(data),
                                      content_type='application/json',
                                      follow_redirects=True)
    assert response.status_code == 200
