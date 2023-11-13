from .. import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=True)

    order = db.relationship('Order', back_populates='products')
    food = db.relationship('Food', back_populates='products')

    def __repr__(self):
        return '<Product %r>' % self.id