from flask import Flask, request, render_template, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Plant, Category


engine = create_engine('sqlite:///plants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

# Create the app.route functions when the user sends the URI "/category"
@app.route('/category')
def catalogFunction():
    plantas = session.query(Category)
    if plantas == 0:
        return "no categories"
    else:
        return render_template('catalog.html', plantas=plantas)
        # return jsonify(Categories=[i.serialize for i in plantas])

# Create the app.route functions when the user sends the URI "/category/category_id/items"
@app.route('/category/<int:category_id>/items')
def categoryFunction(category_id):
    return render_template('category.html')

# Create the app.route functions when the user sends the URI "/category/category_id/item_id"
@app.route('/category/<int:category_id>/<int:item_id>')
def itemFunction(category_id, item_id):
    return render_template('item.html')

# temporary
@app.route('/category/add', methods = ['GET', 'POST'])
def makeANewPuppy():
    name = 'novo'
    category = Category(name=name)
    session.add(category)
    session.commit()
    return jsonify(Category=category.serialize)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
