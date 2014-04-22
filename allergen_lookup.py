import pickle
from pyquery import PyQuery as pq
import base64
import hashlib
import hmac
import urllib
import os
import requests
from collections import namedtuple
API_BASE_URL =  "http://digit-eyes.com/gtin/v2_0/"

kee = ''.join([chr(x) for x in [47, 57, 100, 85, 69, 49, 86, 81, 117, 81, 73, 47]])
auf = ''.join([chr(x) for x in [78, 119, 57, 55, 90, 51, 108, 55, 98, 52, 78, 97, 50, 66, 104, 53]])

Item = namedtuple('Item', 'name, href')


def make_auth_token(upc_code):
    return base64.b64encode(hmac.new(auf, upc_code, hashlib.sha1).digest())

def get_product(upc_code):
    p = requests.get(API_BASE_URL, params=dict(
        upc_code= upc_code,
        app_key=kee,
        signature=make_auth_token(upc_code),
        language='en',
            field_names=','.join(['description',
                                 'brand',
                                 'nutrition',
                                 'ingredients',
                                 'manufacturer',
                                 'image'
                                 ]),
        )).json()
    p['image'] = p.get('image', 'null')
    return p

def get_allergens(description):
    d = pq(get_search_url(description))
    
    all_allergens = set()
    allergens_dict = {}
    different = False

    for i, item in enumerate(map(pq, d('.product-item-content h2>a')[:5])):
        name = item.text()
        url = "http://www.foodfacts.com%s" % item.attr('href')
        item_allergens = get_allergies(url)
        
        if all_allergens:
            if not all_allergens == item_allergens:
                different = True

        all_allergens.update(item_allergens)
        allergens_dict[Item(name,url)] = item_allergens
    return all_allergens, allergens_dict, different


def get_allergies(url):
    d = pq(url)
    allergens = set()

    for a in d('.allergens li a'):
        try:
            allergens.add(pq(a).attr('title'))
        except:
            pass

    return allergens


def get_search_url(description):
    return "http://www.foodfacts.com/index.php?%s" % (
        urllib.urlencode({
            'option':'com_products',
            'view':'products_search',
            'searchWord':description,
            'searchType':'Keywords',
            'id':'-999'
            })
        )

if __name__ == '__main__':
    item_list = pickle.load(open('data.pkl','rb'))


    for upc, code_type in item_list[:10]:
        j  = get_product(upc)
        all_allergens, allergens, different = get_allergens(j.get('description'))
        print "DIFFERENT=%s, %s => %s" % (
                                          diff, 
                                          j.get('description'),
                                          all_allergens
                                          )
