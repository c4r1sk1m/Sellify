from app import app, db
from flask import render_template,flash,redirect,url_for,request, jsonify
# Import Forms
from app.forms import LoginForm,RegistrationForm,EditProfileForm,SaleForm,ItemForm
# Import Login Related packages
from flask_login import current_user, login_user,logout_user,login_required
# Import DB Objects
from app.models import User,Sale,Item
# URL Parsing Package
from werkzeug.urls import url_parse
# Datetime
from datetime import datetime

import requests

# Image Library
import imghdr

# Mapping Libraries
from googlemaps import Client as GoogleMaps
import pandas as pd 


# -------------------------------- Before Request ----------------------------------- #
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# -------------------------------- Page Routing ----------------------------------- #
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username':'Chris'}
    return render_template('index.html',user=user)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    sales = user.sales.order_by(Sale.post_date.desc()).paginate(page,app.config['SALES_PER_PAGE'],False)
    next_url = url_for('user',username=username, page=sales.next_num) \
        if sales.has_next else None
    prev_url = url_for('user',username=username, page=sales.prev_num) \
        if sales.has_prev else None    
    # sales = [
    #     {'seller':user, 'name':'Selling all my things'},
    #     {'seller':user, 'name':'Selling all my things again'}
    # ]
    return render_template('user.html',user=user,sales=sales.items,next_url=next_url,prev_url=prev_url)

@app.route('/search')
def search():
    page = request.args.get('page', 1, type=int)
    sales = Sale.query.order_by(Sale.post_date.desc()).paginate(page,app.config['SALES_PER_PAGE'],False)
    next_url = url_for('search', page=sales.next_num) \
        if sales.has_next else None
    prev_url = url_for('search', page=sales.prev_num) \
        if sales.has_prev else None
    return render_template('/sales/search.html',title='Search',sales=sales.items,next_url=next_url,prev_url=prev_url)


# -------------------------------- SALE Management -------------------------------- #
@app.route('/sale/<id>')
def sale(id):
    sale = Sale.query.filter_by(id=id).first()

    items = sale.items

    map = map_results(sale.address_1, sale.address_2, sale.zipcode)


    return render_template('/sales/sale.html',sale=sale,items=items,user=current_user, map=map)


@app.route('/sale/<id>/item',methods=['GET','POST'])
@login_required
def add_items(id):
    sale = Sale.query.filter_by(id=id).first()
    if sale.user_id != current_user.id:
        return redirect(url_for('index'))
    form = ItemForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data
        item = Item(name=name,description=description,price=price,sale_id=sale.id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('sale',id=id))

    return render_template('/sales/add_items.html',form=form)

@app.route('/new_sale',methods=['GET','POST'])
def create_sale():
    form = SaleForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        zipcode = form.zipcode.data
        address_1 = form.address_1.data
        address_2 = form.address_2.data
        start_date = form.start_date.data
        end_date =  form.end_date.data
        user_id = current_user.id
        sale = Sale(name=name,description=description,zipcode=zipcode,address_1=address_1,address_2=address_2,start_date=start_date,end_date=end_date,user_id=user_id)
        db.session.add(sale)
        db.session.commit()        
 
        flash('Sale Listed')
    else:
        pass
    
    return render_template('/sales/newsale.html',form=form)

# -------------------------------- Mapping ---------------------------------------- #
def map_results(address_1,address_2,zipcode):
    key = 'AIzaSyC8K_D77-BvH6JwBGy1OiVaYzhEwerxAVY'
    gmaps =  GoogleMaps(key)

    addresses = '11 Wisteria Dr Apt 3S, Fords, NJ 08863, USA'
    geocode_result = gmaps.geocode(addresses)
    latitude =  str(geocode_result[0]['geometry']['location'] ['lat'])
    longitude = str(geocode_result[0]['geometry']['location']['lng'])
    print(latitude,longitude)

    map_string =  "<img src='https://maps.googleapis.com/maps/api/staticmap?center="+latitude+","+longitude+"&zoom=13&size=400x400&markers=color:blue%7Clabel:Sale%7C"+latitude+","+longitude+"&key=AIzaSyC8K_D77-BvH6JwBGy1OiVaYzhEwerxAVY'/>"
    print(map_string)
    return map_string





# -------------------------------- USER Management -------------------------------- #
# Edit Profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

# Login
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password!')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html',title='Sign in',form=form)


# User Registration
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            user = User(username=form.username.data,email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Thank you, '+user.username+'. You have been registerd as a user!')
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
    return render_template('register.html',title='Register',form=form)


# Logout Button
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))