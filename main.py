import db_populator
from app import app, db
from standard_api import *


if __name__ == '__main__':
    db_populator.populate()
    app.run(debug=True)

