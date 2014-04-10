import pickle
from pyquery import PyQuery as pq
import base64
import hashlib
import hmac
import requests

API_BASE_URL =  "http://digit-eyes.com/gtin/v2_0/"
kee = ''.join([chr(x) for x in [47, 57, 100, 85, 69, 49, 86, 81, 117, 81, 73, 47]])
auf = ''.join([chr(x) for x in [78, 119, 57, 55, 90, 51, 108, 55, 98, 52, 78, 97, 50, 66, 104, 53]])


def make_auth_token(upc_code):
    return base64.b64encode(hmac.new(auf, upc_code, hashlib.sha1).digest())

def get_request(upc_code):
    return requests.get(API_BASE_URL, params=dict(
        upc_code= upc_code,
        app_key=kee,
        signature=make_auth_token(upc_code),
        language='en',
        field_names=''.join(['description',
                             'brand',
                             'nutrition',
                             'ingredients',
                             'manufacturer'
                             ]),
        ))


item_list = pickle.load(open('data.pkl','rb'))


for upc, code_type in item_list:
    print get_request(upc).json()

