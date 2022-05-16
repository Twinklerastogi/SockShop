from atexit import register
from email.quoprimime import header_check
from tokenize import cookie_re
import requests
import base64
import json


class TestIntigration:

    def setup(self):
        self.url = "http://localhost/"
        self.username = 'test'
        self.password = 'test'
        self.session = requests.Session()

    def hit_api(self, method, api, payload=None, headers=None, cookies=None):

        
        apiS = {
            'register': 'register',
            'login': 'login',
            'add_to_cart': 'cart',
            'get_cart': 'cart'
        }
        url = "%s%s" % (self.url, apiS[api])
        if method == 'GET':
            response = self.session.get(
                url, headers=headers)
        else:
            response = self.session.get(
                url, headers=headers, data=json.dumps(payload))
        return response

    def test_login(self):

        self.setup()
        # Register user first
        payload = {
            "username": self.username,
            "password": self.password,
            "email": "text@dan"
        }
        res = self.hit_api('POST', 'register', payload, headers={
                           'Content-Type': 'application/json'})

        authString = '%s:%s' % (self.username, self.password)
        authString = authString.encode("ascii")
        authString = base64.b64encode(authString)
        authString = authString.decode("utf-8")
        res = self.hit_api('GET', 'login', headers={
                           'Authorization': 'Basic %s' % (authString)})
        assert res.status_code == 200

    def test_add_to_cart(self):

        self.setup()
        authString = '%s:%s' % (self.username, self.password)
        authString = authString.encode("ascii")
        authString = base64.b64encode(authString)
        authString = authString.decode("utf-8")
        res_login = self.hit_api('GET', 'login', headers={
            'Authorization': 'Basic %s' % (authString)})
        cookie_header = ''
        ck_dic = self.session.cookies.get_dict()
        for ele in ck_dic:
            cookie_header += "%s=%s; " % (ele, ck_dic[ele])
        res = self.hit_api('POST', 'add_to_cart', payload={
                           "id": 1, "quantity": 1}, headers={
                           'Cookie': cookie_header})

        res = self.hit_api('GET', 'get_cart', headers={
                           'Cookie': cookie_header})
        res = res.json()
        print(res)
        if res:
            assert res[0].get('quantity', 0)
