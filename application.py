from flask import Flask, request, render_template, jsonify, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from models import Base, Item, Category


engine = create_engine('sqlite:///plants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

# Add JSON API Endpoint for categories
@app.route('/category/JSON')
def categoriesJSON():
    category = session.query(Category)
    return jsonify(Categories=[i.serialize for i in category])

# Add JSON API Endpoint for a category items
@app.route('/category/<int:category_id>/items/JSON')
def categoriesItemsJSON(category_id):
    category2 = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])

# Add JSON API Endpoint for a item
@app.route('/category/<int:category_id>/items/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    items = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Items=items.serialize)

# Create the app.route function to list all categories
@app.route('/category')
def catalogFunction():
    category = session.query(Category)
    if category == 0:
        flash("You have no categories yet!")
        return render_template('catalog.html', plantas=category)
    else:
        return render_template('catalog.html', plantas=category)

# Create the app.route functions for create a new category
@app.route('/category/new', methods=['GET', "POST"])
def newCategoryFunction():
    category = session.query(Category)
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'])
        session.add(newCategory)
        session.commit()
        flash("New category created!")
        return redirect(url_for('catalogFunction', category=category))
    else:
        return render_template('newCategory.html', category=category)
        # return jsonify(Categories=[i.serialize for i in category])

# Create the app.route function for edit a category
@app.route('/category/<int:category_id>/edit', methods=['GET', "POST"])
def editCategoryFunction(category_id):
    category2 = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            category2.name = request.form['name']
        session.add(category2)
        session.commit()
        flash("The category was seccessfully edited!")
        return redirect(url_for('catalogFunction', category2=category2))
    else:
        return render_template('editCategory.html', category2=category2)

# Create the app.route function for delete a category
@app.route('/category/<int:category_id>/delete', methods=['GET', "POST"])
def deleteCategoryFunction(category_id):
    category = session.query(Category)
    category2 = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(category2)
        session.commit()
        flash("Category seccessfully deleted!")
        return redirect(url_for('catalogFunction', plantas=category))
    else:
        return render_template('deleteCategory.html', category2=category2)

# Create the app.route function to display the items for the selected category
    # Fix: display messagem whem have no items
@app.route('/category/<int:category_id>/items')
def categoryFunction(category_id):
    category = session.query(Category)
    category2 = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category2.id)
    if not items:
        flash("You have no items yet!")
        return render_template('category.html', plantas=category, plantas2=category2, itemName=items)
    else:
        return render_template('category.html', plantas=category, plantas2=category2, itemName=items)

# Create the app.route function to add new item to category
@app.route('/category/<int:category_id>/items/new', methods=['GET', "POST"])
def newItemFunction(category_id):
    category = session.query(Category)
    category2 = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'], description=request.form['description'],
            category_id=category_id)
        session.add(newItem)
        session.commit()
        flash("New menu item created!")
        return redirect(url_for('categoryFunction', category_id=category_id))
    else:
        return render_template('newItem.html', category=category, category2=category2)

# Create the app.route function to display item
@app.route('/category/<int:category_id>/items/<int:item_id>')
def itemFunction(category_id, item_id):
    category2 = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', itemName=items)


# Create the app.route function to edit item
@app.route('/category/<int:category_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def editItemFunction(category_id, item_id):
    category = session.query(Category)
    category2 = session.query(Category).filter_by(id=category_id).one()
    editItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        if request.form['category']:
            editItem.category_name = request.form['category']
        session.add(editItem)
        session.commit()
        flash("Item seccessfully edited!")
        return redirect(url_for('itemFunction', category_id=category_id, item_id=item_id))
    else:
        return render_template('editItem.html', category=category, category2=category2, editItem=editItem)

# Create the app.route function to delete a item
@app.route('/category/<int:category_id>/items/<int:item_id>/delete', methods=['GET', "POST"])
def deleteItemFunction(category_id, item_id):
    category2 = session.query(Category).filter_by(id=category_id).one()
    deleteItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("Menu item seccessfully deleted!")
        return redirect(url_for('categoryFunction', category_id=category2.id))
    else:
        return render_template('deleteItem.html', category_id=category_id, item=deleteItem)

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
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
