from flask import Flask, request, render_template, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Item, Category


engine = create_engine('sqlite:///plants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

# Create the app.route functions when the user sends the URI "/category"
@app.route('/category')
def catalogFunction():
    category = session.query(Category)
    if category == 0:
        return "no categories"
    else:
        return render_template('catalog.html', plantas=category)
        # return jsonify(Categories=[i.serialize for i in category])

# Create the app.route functions when the user sends the URI "/category/category_id/items"
@app.route('/category/<int:category_id>/items')
def categoryFunction(category_id):
    category = session.query(Category)
    category2 = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id)
    if items == 0:
        return "No items yet"
    else:
        return render_template('category.html', plantas=category, plantas2=category2, itemName=items)
        # return jsonify(Items=[i.serialize for i in items])

# Create the app.route functions when the user sends the URI "/category/category_id/item_id"
@app.route('/category/<int:category_id>/items/<int:item_id>')
def itemFunction(category_id, item_id):
    category2 = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', itemName=items)

# temporary
@app.route('/category/add', methods=['GET', 'POST'])
def makeANewPuppy():
    name = 'novo'
    category = Category(name=name)
    session.add(category)
    session.commit()
    return jsonify(Category=category.serialize)

# temporary
@app.route('/category/<int:category_id>/add', methods=['GET', 'POST'])
def makeANewItem():
    name = 'novo item'
    description = 'nova descricao'
    item = Item(name=name, description=description)
    session.add(item)
    session.commit()
    return jsonify(Item=item.serialize)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
