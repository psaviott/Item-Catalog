from flask import Flask, request, render_template, jsonify, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Item, Category


engine = create_engine('sqlite:///plants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

# Create the app.route function to list all categories
@app.route('/category')
def catalogFunction():
    category = session.query(Category)
    if category == 0:
        flash("You have no categories yet!")
        return render_template('catalog.html', plantas=category)
    else:
        return render_template('catalog.html', plantas=category)
        # return jsonify(Categories=[i.serialize for i in category])

# Create the app.route function to display the items for the selected category
@app.route('/category/<int:category_id>/items')
def categoryFunction(category_id):
    category = session.query(Category)
    category2 = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id)
    if items == 0:
        flash("You have no items yet!")
        return render_template('category.html', plantas=category, plantas2=category2, itemName=items)
    else:
        return render_template('category.html', plantas=category, plantas2=category2, itemName=items)
        # return jsonify(Items=[i.serialize for i in items])

# Create the app.route function to list all items for the category
    # add message to inform the user if the category or item not exist
@app.route('/category/<int:category_id>/items/<int:item_id>')
def itemFunction(category_id, item_id):
    category2 = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', itemName=items)


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
    category2 = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(category2)
        session.commit()
        flash("Category seccessfully deleted!")
        return redirect(url_for('catalogFunction', category2=category2))
    else:
        return render_template('deleteCategory.html', category2=category2)


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
