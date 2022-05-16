import requests
import pytest

pytest_plugin = ["docker_compose"]


def test_customers():
    url = "http://localhost/orders"
    reqObj = requests.get(url)
    reqData = reqObj.json()
    assert reqObj.status_code == 500
    assert reqData.get('message') == "User not logged in."
