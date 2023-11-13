from .. import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', back_populates='orders', uselist=False, single_parent=True)
    products = db.relationship('Product', back_populates='order', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Order %r>' % self.id
