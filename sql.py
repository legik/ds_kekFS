from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'),
                           nullable=False)
    cluster = db.relationship('Cluster', backref=db.backref('id', lazy=True))
    # TODO: add size constrain
    size = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.alias


class Cluster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    second1 = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    second2 = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    server = db.relationship('Server', backref=db.backref('id', lazy=True))

    def __repr__(self):
        return '<Cluster %r>' % self.id


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.BOOLEAN, nullable=False)
    address = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return '<Server %r>' % self.id


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(125), unique=True, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('id', lazy=True))

    def __repr__(self):
        return '<File %r>' % self.name
