from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'url'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'),
                           nullable=False)
    cluster = db.relationship('Cluster', backref=db.backref('id', lazy=True))
    size = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username


class Cluster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Cluster %r>' % self.name