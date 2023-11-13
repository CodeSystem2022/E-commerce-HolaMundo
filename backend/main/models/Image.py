from .. import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    

    food = db.relationship('Food', back_populates='image', cascade='all, delete-orphan')
    
    def __repr__(self):
        return '<Image %r>' % self.id
