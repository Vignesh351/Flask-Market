from market import app
from flask import render_template , redirect ,url_for , flash , request
from market.model import Item , user
from market.forms import RegisterForm ,LoginForm , PurchaseItemForm , SellItemForm
from market import db 
from flask_login import login_user , logout_user , login_required , current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name = purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"confirmed purchase of {p_item_object.name}", category="success")
            else :
                flash(f"Not enough budget to purchase {p_item_object.name}", category="danger")
        
        sold_item = request.form.get('sold_item')
        s_item_object =  Item.query.filter_by(name= sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"confirmed Selling of {s_item_object.name}", category="success")
            else :
                flash(f"Somthing went wrong in selling {s_item_object.name}", category="danger")
        return redirect(url_for("market_page"))
    if request.method =='GET':
        items = Item.query.filter_by(owner_id=None)
        owned_items = Item.query.filter_by(owner_id=current_user.id).all()
        return render_template('market.html', items=items , purchase_form=purchase_form , owned_items=owned_items , selling_form=selling_form)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if  form.validate_on_submit():
        user_to_create = user(username = form.username.data,
                              email_address = form.email_address.data,
                              password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f" Account created successfully , You are logged in as {user_to_create.username}",category="success")

        return redirect(url_for('market_page'))
    
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Error: {err}" ,category='danger')
    return render_template('register.html' , form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user_logged_in = user.query.filter_by(username=form.username.data).first()
        
        if user_logged_in and user_logged_in.check_password_correction(attempted_password= form.password.data):
            login_user(user_logged_in)
            flash(f"You are logged in as {user_logged_in.username}",category="success")
            return redirect(url_for('market_page'))
        
        else:
            flash(f"Invalid username or password", category="warning")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("you have been logged out" , category="info")
    return redirect(url_for('home_page'))
    