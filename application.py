from flask import Flask
app = Flask(__name__)
# Create the appropriate app.route functions,

# Create the app.route functions when the user sends the URI "/category"
@app.route('/category')
def catalogFunction():
    return "Works!"

# Create the app.route functions when the user sends the URI "/category/category_id/items"
@app.route('/category/<int:category_id>/items')
def categoryFunction(category_id):
    return "Works too!"

# Create the app.route functions when the user sends the URI "/category/category_id/item_id"
@app.route('/category/<int:category_id>/<int:item_id>')
def itemFunction(category_id, item_id):
    return "Works too too!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
