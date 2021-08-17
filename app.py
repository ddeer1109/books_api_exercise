from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from Configuration import Configuration

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Configuration.sqlalchemy_test_db
db = SQLAlchemy(app)
