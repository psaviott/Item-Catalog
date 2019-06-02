# Item Catalog

Modern web applications perform a variety of functions and provide features and utilities to their usersbcreating, reading, updating and deleting data. In this project, combine knowledge about front-end development to make a good resposive page and back-end development to create a persistent data storage and user authentication&authorization to create a web application that provides a compelling service to your users.

This application provides a list of items within a variety of categories as well as provide a user registration and authentication system.
Registered users will have the ability to create, edit and delete their own items or categories.

## Getting Started
This project use a Python3 web server. You can run this in a virtual machine. If you need help to install and setup a virtual machine with VirtualBox and Vagrant, check the reference link bellow on Resources.

### Prerequisites
* [Python3](https://www.python.org/ "Python Homepage")
* [Python3 Modules](requirements.txt "Requisites for python3")
* [Web Server](https://en.wikipedia.org/wiki/Web_server/ "Wikipedia article about Web Servers")

### Installing and Running
1. Clone this git repositoriy:
    ```
      $ git clone https://github.com/psaviott/Item-Catalog.git
    ```

2. Install the required modules:
    ```python3
      $ pip3 install -r /path/to/requirements.txt
    ```

3. If you whant to populate the database run:
    ```python3
      $ python3 setup_database.py
    ```

4. Run the application:
    ```python3
      $ python3 application.py
    ```

5. Access the main page of the application:
```
  http://localhost:5000/
```

## Running the tests

The endpoints can be acessible for all clients, but some pages is only available to logged users

### List of HTML Endpoints:

> * List all categories: **/category**
>   * example: http://localhost:5000/category
> * Create a new category: **/category/news**
>   * example: http://localhost:5000/category/new
> * Edit a category: **/category/<int:category_id>/edit**
>   * example: http://localhost:5000/category/1/edit
> * Delete a category: **/category/<int:category_id>/delete**
>   * example: http://localhost:5000/category/1/delete
> * List all items for the category:
> **/category/<int:category_id>/items**
>   * example: http://localhost:5000/category/1/items
> * Display an item:
> **/category/<int:category_id>/items/<int:item_id>**
>   * example: http://localhost:5000/category/1/items/1
> * Add an item: **/category/<int:category_id>/items/new**
>   * example: http://localhost:5000/category/1/items/news
> * Edit an item:
> **/category/<int:category_id>/items/<int:item_id>/edit**
>   * example: http://localhost:5000/category/1/items/1/edit
> * Delete an item:
> **/category/<int:category_id>/items/<int:item_id>/delete**
>   * example: http://localhost:5000/category/1/items/1/delete

### List of JSON Endpoint

> * List categories with respective items: **/category/JSON**
>  * example: http://localhost:5000/category/JSON
> * List all items for the category: **/category/<int:category_id>/items/JSON**
>  * example: http://localhost:5000/category/1/JSON
> * Display item infos: **/category/<int:category_id>/items/<int:item_id>/JSON**
>  * example: http://localhost:5000/category/1/items/1/JSON

## Built With

* [Python3](https://docs.python.org/ "Python3 documentation") Programming Language
* [Flask](http://flask.pocoo.org/ "Flask homepage") Python Framework
* [SQLAlchemy](https://www.sqlalchemy.org/ "SQLAlchemy homepage") Python SQL toolkit and Object Relational Mapper
* [OAuth2.0](https://oauth.net/2/ "OAuth2.0 homepage") industry-standard protocol for authorization

## Authors

* Philipe Saviott - [psaviott](https://github.com/psaviott)

## Acknowledgments
* [Google Sign-In](https://developers.google.com/identity/sign-in/web/sign-in "PostgreSQL documentation") Integrating Google Sign-In into your web app
* [Python3](https://docs.python.org/3.6/index.html "Python3 documentation") documentation
* [VirtualBox and Vagrant](https://www.taniarascia.com/what-are-vagrant-and-virtualbox-and-how-do-i-use-them/ "How to use Vagrant and VirtualBox") by Tania Rascia
