import requests

def test_customers():
    url = "http://localhost/cards"
    reqObj = requests.get(url)
    reqData = reqObj.json()
    assert reqObj.status_code == 200
    assert type(reqData.get('_embedded')['card']) == list