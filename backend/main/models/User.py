from main import db
from werkzeug.security import generate_password_hash, check_password_hash 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(120), nullable=False)

    orders = db.relationship('Order', back_populates='user', cascade = 'all, delete-orphan')

    @property
    def plain_password(self):
        raise AttributeError('password is not a readable attribute')

    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)


    def generate_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username

   