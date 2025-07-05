# backend/database.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "mysql+mysqlconnector://admin:Youngkayla35!"
        "@cis2368spring.cqvqcae80duk.us-east-1.rds.amazonaws.com/cis2368springdb"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
