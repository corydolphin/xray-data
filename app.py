from flask import Flask, jsonify, render_template
app = Flask(__name__)
from allergen_lookup import get_allergens,get_product


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/lookup/<upc_code>')
def lookup(upc_code):
    print "Started"
    product = get_product(upc_code)
    print product
    all_allergens, allergens_dict, different = get_allergens(product.get('description'))
    return jsonify(product=product,
                   allergens=to_list(all_allergens),
                   allergens_by_product=to_dict(allergens_dict)
                   )

def to_list(_set):
    return [s for s in _set]

def to_dict(allergens):
    return {item.name:to_list(_allergens) for item,_allergens in allergens.iteritems()}

if __name__ == '__main__':
    app.run(debug=True)