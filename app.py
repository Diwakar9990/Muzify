from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '0de0b0cb353e9fd582cd896c4046eba6f9314fd70a4d647c63d1da7b247d95d0fe4df65d81014c1cc8c06381ef9acafd96aef446bf7f027ae8cd58f77b97e8e8'

import models as models
import routes as routes

if __name__ == '__main__':
    app.run(debug=True)