from market import app
from flask import render_template,redirect,url_for,flash,get_flashed_messages,request
from market.models import Item,User
from market.forms import Registerform
from market.forms import LoginForm
from market.forms import PurchaseItemForm
from market.forms import SellItemForm
from market import db
from flask_login import login_user,logout_user,login_required,current_user

@app.route('/')
@app.route('/home')
def helloworld():
    return render_template('home.html')


@app.route('/market',methods=['GET','POST'])
@login_required
def market():
    
    form = PurchaseItemForm()

    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congraulations! you purchased {p_item_object.name} for {p_item_object.price}",category='danger')
            else:
                flash(f"no money {p_item_object.name} for {p_item_object.price} ",category='danger')

    # if request.method == "GET":
    items = Item.query.filter_by(owner=None)
    owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template('market.html',product=items,form=form,owned_items=owned_items)

    # if form.validate_on_submit():
    #     print(request.form.get('purchased_item'))

    

@app.route('/users')
def users():
    user = User.query.all()
    return render_template('users.html',users=user)

@app.route('/register',methods=['GET','POST'])    
def register_page():
    form = Registerform()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,passwordhash=form.password1.data)
        db.session.add(user);
        db.session.commit();
        # return redirect(url_for('/login'))
        return redirect('/login')
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f"{err_msg}",category="danger")    
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST']) 
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password = form.password.data
        ): 
            login_user(attempted_user) 
            flash(f"Sucess! You are logged in {attempted_user.username}",category='sucess')
            return redirect("/")
        else:
            flash("Username and password is not match",category='danger')

    return render_template("login.html",form=form)  


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logout",category='danger')
    return redirect('/')
