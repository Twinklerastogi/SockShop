import requests

def test_customers():
    url = "http://localhost/customers"
    reqObj = requests.get(url)
    reqData = reqObj.json()
    assert reqObj.status_code == 200
    assert type(reqData.get('_embedded')) == dict