from .. import db 

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    

    image = db.relationship('Image', back_populates='food', uselist=False, single_parent=True)
    products = db.relationship('Product', back_populates='food', uselist=False, single_parent=True)
    
    def __repr__(self):
        return '<Food %r>' % self.name
