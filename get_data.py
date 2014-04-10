from parse_rest.connection import register
from parse_rest.datatypes import Object
import os
import pickle
APP_ID = 'f0zwTm7O0dYBWQ3liRpqABtiKE7wqKq1MGFw1bV1'
APP_REST = ''.join([chr(x) for x in [80, 117, 120, 78, 65, 118, 79, 107, 52, 108, 66, 99, 76, 104, 88, 118, 114, 79, 102, 87, 113, 113, 48, 113, 78, 50, 82, 97, 121, 77, 109, 114, 84, 90, 100, 109, 117, 56, 68, 85]])

register(APP_ID,APP_REST)


class roche(Object):
    pass

objs = [(o.code, o.type) for o in roche.Query.all()]
pickle.dump(objs,open('data.pkl','wb'))

