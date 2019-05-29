from flask import Flask, request, render_template, jsonify, url_for, redirect, flash
import requests
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from models import Base, Item, Category, User
from flask_httpauth import HTTPBasicAuth
from flask import session as login_session
import json, random, string
from googleapiclient.discovery import build
import httplib2
from oauth2client import client

engine = create_engine('sqlite:///plants.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)
auth = HTTPBasicAuth()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item-Catalog"

@app.route('/login')
def showLogin():
    return render_template('loginteste.html')

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # If this request does not have `X-Requested-With` header, this could be a CSRF
    if not request.headers.get('X-Requested-With'):
        abort(403)

    # Set path to the Web application client_secret_*.json file you downloaded from the
    # Google API Console: https://console.developers.google.com/apis/credentials
    CLIENT_SECRET_FILE = '/client_secrets.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
        auth_code)

    # Call Google API
    http_auth = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http_auth)
    appfolder = drive_service.files().get(fileId='appfolder').execute()

    id_token = credentials.id_token
    # Get profile info from ID token
    login_session['name'] = credentials.id_token['sub']
    login_session['email'] = credentials.id_token['email']
    login_session['picture'] = credentials.id_token['picture']

    # Store the access token in the session for later use.
    login_session['id_token'] = credentials.id_token

# Add JSON API Endpoint for categories
# Fix: display items into the correct catalog
@app.route('/category/JSON')
def categoriesJSON():
    category = session.query(Category)
    items = session.query(Item).filter_by(category_id=Item.category_id).all()
    return jsonify(Categories=[i.serialize for i in category], Items=[i.serialize for i in items])

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
# Fix: Display message when has no categories
@app.route('/category')
def catalogFunction():
    category = session.query(Category)
    items = session.query(Item).filter_by(category_id=Item.category_id).order_by(Item.id.desc()).all()
    if 'username' not in login_session:
        if category.count() == 0:
            flash("You have no categories yet!")
            return render_template('publicCatalog.html', plantas=category, itemName = items)
        else:
            return render_template('publicCatalog.html', plantas=category, itemName = items)
    else:
        if category.count() == 0:
            flash("You have no categories yet!")
            return render_template('catalog.html', plantas=category, itemName = items)
        else:
            return render_template('catalog.html', plantas=category, itemName = items)

# Create the app.route functions for create a new category
@app.route('/category/new', methods=['GET', "POST"])
def newCategoryFunction():
    category = session.query(Category)
    if 'username' not in login_session:
        return redirect('/login')
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
    category2 = session.query(Category).filter_by(id=category_id).first()
    if not hasattr(category2, 'id'):
        return "this category not exist"
    if 'username' not in login_session:
        return redirect('/login')
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
    category2 = session.query(Category).filter_by(id=category_id).first()
    deleteItem = session.query(Item).filter_by(id=category_id).all()
    if not hasattr(category2, 'id'):
        return "this category not exist"
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(category2)
        session.delete(deleteItem)
        session.commit()
        flash("Category and his items was seccessfully deleted!")
        return redirect(url_for('catalogFunction', plantas=category))
    else:
        return render_template('deleteCategory.html', category2=category2)

# Create the app.route function to display the items for the selected category
# Fix: display messagem whem have no items
@app.route('/category/<int:category_id>/items')
def categoryFunction(category_id):
    category = session.query(Category)
    category2 = session.query(Category).filter_by(id=category_id).first()
    if not hasattr(category2, 'id'):
        return "this category not exist"
    items = session.query(Item).filter_by(category_id=category2.id)
    if 'username' not in login_session:
        if items.count() == 0:
            flash("You have no items yet!")
            return render_template('publicCategory.html', plantas=category, plantas2=category2, itemName=items)
        else:
            return render_template('publicCategory.html', plantas=category, plantas2=category2, itemName=items)
    else:
        if items.count() == 0:
            flash("You have no items yet!")
            return render_template('category.html', plantas=category, plantas2=category2, itemName=items)
        else:
            return render_template('category.html', plantas=category, plantas2=category2, itemName=items)

# Create the app.route function to display item
@app.route('/category/<int:category_id>/items/<int:item_id>')
def itemFunction(category_id, item_id):
    category2 = session.query(Category).filter_by(id=category_id).first()
    if not hasattr(category2, 'id'):
        return "this category not exist"
    items = session.query(Item).filter_by(id=item_id).first()
    if not hasattr(items, 'id'):
        return "this item not exist"
    if 'name' not in login_session:
        return render_template('publicItem.html', itemName=items, category=category2)
    else:
        return render_template('item.html', itemName=items, category=category2)

# Create the app.route function to add new item to category
@app.route('/category/<int:category_id>/items/new', methods=['GET', "POST"])
def newItemFunction(category_id):
    category = session.query(Category)
    category2 = session.query(Category).filter_by(id=category_id).first()
    if not hasattr(category2, 'id'):
        return "this category not exist"
    if 'username' not in login_session:
        return redirect('/login')
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


# Create the app.route function to edit item
@app.route('/category/<int:category_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def editItemFunction(category_id, item_id):
    category = session.query(Category)
    category2 = session.query(Category).filter_by(id=category_id).first()
    if not hasattr(category2, 'id'):
        return "this category not exist"
    editItem = session.query(Item).filter_by(id=item_id).first()
    if not hasattr(editItem, 'id'):
        return "this item not exist"
    if 'username' not in login_session:
        return redirect('/login')
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
    category2 = session.query(Category).filter_by(id=category_id).first()
    if not hasattr(category2, 'id'):
        return "this category not exist"
    deleteItem = session.query(Item).filter_by(id=item_id).first()
    if not hasattr(deleteItem, 'id'):
        return "this item not exist"
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("Menu item seccessfully deleted!")
        return redirect(url_for('categoryFunction', category_id=category2.id))
    else:
        return render_template('deleteItem.html', category_id=category_id, item=deleteItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
