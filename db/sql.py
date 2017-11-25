from flask import Flask
from flask_login._compat import unicode
from flask_sqlalchemy import SQLAlchemy
from db import cfg

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.connection
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    cluster = db.Column(db.Integer, db.ForeignKey('cluster.id'),
                        nullable=False)
    port = db.Column(db.Integer, nullable=False)
    files = db.relationship('File', backref='owner', lazy='dynamic')
    # TODO: add size constrain
    size = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.alias

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Cluster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    second1 = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    second2 = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    users = db.relationship('User', backref='tenant', lazy='dynamic')

    def __repr__(self):
        return '<Cluster %r>' % self.id


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.BOOLEAN, nullable=False)
    address = db.Column(db.String(45), nullable=False)
    main_clusters = db.relationship('Cluster', backref='mains', lazy='dynamic',
                                    foreign_keys=[Cluster.main])
    second1_clusters = db.relationship('Cluster', backref='seconds1',
                                       lazy='dynamic',
                                       foreign_keys=[Cluster.second1])
    second2_clusters = db.relationship('Cluster', backref='seconds2',
                                       lazy='dynamic',
                                       foreign_keys=[Cluster.second2])

    def __repr__(self):
        return '<Server %r>' % self.id


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(125), unique=True, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<File %r>' % self.name
