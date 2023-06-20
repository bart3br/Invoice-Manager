from application import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique = True, nullable = False)
    email = db.Column(db.String(125), unique = True, nullable = False)
    image_file = db.Column(db.String(25), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    #one to many relationship between user and invoice
    #backref let's us access the user who created the invoice from the invoice itself
    invoices = db.relationship('Invoice', backref='author', lazy=True)
    
    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    entries = db.relationship('Entry', backref='invoice', lazy=True)
    
    def __repr__(self) -> str:
        return f"Invoice('{self.name}', '{self.amount}', '{self.date_posted}')"


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    quantity = db.Column(db.Integer, nullable = False, default = 1)
    price = db.Column(db.Numeric(10,2), nullable = False)
    total_price = db.column_property(price * quantity)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable = False)
    
    __table_args__ = (
        db.CheckConstraint(quantity > 0, name='check_quantity_positive'),
        db.CheckConstraint(price > 0, name='check_price_positive'),
    )
    
    def __repr__(self) -> str:
        return f"Entry('{self.name}', '{self.quantity}', '{self.price}', '{self.total_price}')"