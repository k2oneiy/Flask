from market import db,login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(length=50),nullable=False,unique=True)
    email = db.Column(db.String(length=60),nullable=False,unique=True)
    password = db.Column(db.String(length=60),nullable=False)
    buget = db.Column(db.Integer,nullable=False,default=1000)
    item = db.relationship('Item',backref='owned_user',lazy=True)

    def __repr__(self):
        return f'Item {self.username}'

    @property
    def passwordhash(self):
        return self.password

    @passwordhash.setter
    def passwordhash(self,plain_text_password):  
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8') 

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password,attempted_password)

    def can_purchase(self,item_obj):
        return self.buget >= item_obj.price




class Item(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(length=30),nullable=False,unique= True)
    price = db.Column(db.Integer,nullable=False)
    bercode = db.Column(db.String(length=12),nullable=False,unique= True)
    description = db.Column(db.String(length=1024),nullable=False,unique= True)
    owner = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name} {self.price}'

    def buy(self,user):
        self.owner = user.id
        user.buget -= self.price
        db.session.commit()    



