from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
import pymysql
import secrets


conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
app = Flask(__name__)

app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class g2_materialtable(db.Model):
    #__tablename__ = 'results'
    MaterialID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255))
    DateAdded = db.Column(db.DateTime)
    LastModified = db.Column(db.DateTime)
    Genre = db.Column(db.String(255))
    Author = db.Column(db.String(255))
    ISBN = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | Title: {1} | Date Added: {2} | Last Modified: {3} | Genre: {4} | Author: {5} | ISBN: {6}".format(self.MaterialID, self.Title, self.DateAdded, self.LastModified, self.Genre, self.Author, self.ISBN)

class MaterialForm(FlaskForm):
    MaterialID = IntegerField('Material ID: ')
    Title = StringField('Title:', validators=[DataRequired()])
    DateAdded = DateField('Date Added: ')
    LastModified = DateField('Date Last Modified: ')
    Genre = StringField('Genre: ', validators=[DataRequired()])
    Author = StringField('Author:', validators=[DataRequired()])
    ISBN = IntegerField('ISBN:', validators=[DataRequired()])

@app.route('/')
def index():
    all_materials = g2_materialtable.query.all()
    return render_template('index.html', materials=all_materials, pageTitle='SLPL Materials')

@app.route('/materials')
def materials():
    all_materials = g2_materialtable.query.all()
    return render_template('materials.html', materials=all_materials, pageTitle='Materials', legend='Materials')

@app.route('/search', methods=['GET', 'POST'])
def search_materials():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = g2_materialtable.query.filter( or_(g2_materialtable.Title.like(search), g2_materialtable.Genre.like(search), g2_materialtable.Author.like(search), g2_materialtable.ISBN.like(search))).all()
        return render_template('index.html', materials=results, pageTitle="Materials", legend ="Update A Material")
    else:
        return redirect('/')

@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    form = MaterialForm()
    print('Before validate')
    if form.validate_on_submit():
        print('inside validate')
        material = g2_materialtable(Title=form.Title.data, DateAdded=datetime.datetime.now(),LastModified=datetime.datetime.now(), Genre=form.Genre.data, Author=form.Author.data, ISBN=form.ISBN.data)
        db.session.add(material)
        db.session.commit()
        return redirect('/')
    return render_template('add_material.html', form=form, pageTitle='Add A New Material', legend="Add A New Material")


@app.route('/material/<int:MaterialID>', methods=['GET','POST'])
def material(MaterialID):
    material = g2_materialtable.query.get_or_404(MaterialID)
    return render_template('material.html', form=material, pageTitle='Material Details')

@app.route('/material/<int:MaterialID>/update', methods=['GET','POST'])
def update_material(MaterialID):
    material = g2_materialtable.query.get_or_404(MaterialID)
    form = MaterialForm()

    if form.validate_on_submit():
        material.MaterialID = form.MaterialID.data
        material.Title = form.Title.data
        material.DateAdded = datetime.datetime.now()
        material.LastModified = datetime.datetime.now()
        material.Genre = form.Genre.data
        material.Author = form.Author.data
        material.ISBN = form.ISBN.data
        db.session.commit()
        flash('This material has been updated!')
        return redirect(url_for('material', MaterialID=material.MaterialID))

    form.MaterialID.data = material.MaterialID
    form.Title.data = material.Title
    form.DateAdded.data = material.DateAdded
    form.LastModified.data = material.LastModified
    form.Genre.data = material.Genre
    form.Author.data = material.Author
    form.ISBN.data = material.ISBN
    return render_template('update_material.html', form=form, pageTitle='Update Material',legend="Update A Material")

@app.route('/material/<int:MaterialID>/delete', methods=['POST'])
def delete_material(MaterialID):
    if request.method == 'POST': #if it's a POST request, delete the material from the database
        material = g2_materialtable.query.get_or_404(MaterialID)
        db.session.delete(material)
        db.session.commit()
        flash('Material was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")

class g2_peopletable(db.Model):
    #__tablename__ = 'results'
    PeopleID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(255))
    LastName = db.Column(db.String(255))
    Birthdate = db.Column(db.DateTime)
    Address = db.Column(db.String(255))
    City = db.Column(db.String(255))
    State = db.Column(db.String(255))
    Zip = db.Column(db.Integer())
    PhoneNumber1 = db.Column(db.Integer())
    PhoneNumber2 = db.Column(db.Integer())
    Email = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | First Name: {1} | Last Name: {2} | Birthdate: {3} | Address: {4} | City: {5} | State: {6} | Zip: {7} | Phone Number 1: {8} | Phone Number 2: {9} | Email: {10}".format(self.PeopleID, self.FirstName, self.LastName, self.Birthdate, self.Address, self.City, self.State, self.Zip, self.PhoneNumber1, self.PhoneNumber2, self.Email)

class PeopleForm(FlaskForm):
    PeopleID = IntegerField('People ID: ')
    FirstName = StringField('First Name:', validators=[DataRequired()])
    LastName = StringField('Last Name:', validators=[DataRequired()])
    Birthdate = DateField('Birthdate: ')
    Address = StringField('Address: ', validators=[DataRequired()])
    City = StringField('City:', validators=[DataRequired()])
    State = StringField('State:', validators=[DataRequired()])
    Zip = IntegerField('Zip:', validators=[DataRequired()])
    PhoneNumber1 = IntegerField('Phone Number 1:', validators=[DataRequired()])
    PhoneNumber2 = IntegerField('Phone Number 2:')
    Email = StringField('Email: ', validators=[DataRequired()])

@app.route('/people')
def people():
    all_people = g2_peopletable.query.all()
    return render_template('people.html', people=all_people, pageTitle='Patrons', legend='Patrons')

@app.route('/search', methods=['GET', 'POST'])
def search_people():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = g2_peopletable.query.filter( or_(g2_peopletable.FirstName.like(search), g2_peopletable.LastName.like(search), g2_peopletable.Birthdate.like(search), g2_peopletable.Address.like(search), g2_peopletable.City.like(search), g2_peopletable.State.like(search), g2_peopletable.State.like(search), g2_peopletable.Zip.like(search), g2_peopletable.PhoneNumber1.like(search), g2_peopletable.PhoneNumber2.like(search), g2_peopletable.Email.like(search))).all()
        return render_template('people.html', people=results, pageTitle="People")

    else:
        return redirect('/')

@app.route('/add_people', methods=['GET', 'POST'])
def add_people():
    form = PeopleForm()
    print('Before validate')
    if form.validate_on_submit():
        print('inside validate')
        people = g2_peopletable(FirstName=form.FirstName.data, LastName=form.LastName.data, Birthdate=datetime.Birthdate.now(), Address=form.Address.data, City=form.City.data, State=form.State.data, Zip=form.Zip.data, PhoneNumber1=form.PhoneNumber1.data, PhoneNumber2=form.PhoneNumber2.data, Email=form.Email.data)
        db.session.add(people)
        db.session.commit()
        return redirect('/')
    return render_template('add_people.html', form=form, pageTitle='Add A New Patron', legend="Add A New Patron")


@app.route('/people/<int:PeopleID>', methods=['GET','POST'])
def patron(PeopleID):
    people = g2_peopletable.query.get_or_404(PeopleID)
    return render_template('patron.html', form=people, pageTitle='Patron Details')

@app.route('/patron/<int:PeopleID>/update', methods=['GET','POST'])
def update_people(PeopleID):
    people = g2_peopletable.query.get_or_404(PeopleID)
    form = PeopleForm()

    if form.validate_on_submit():
        people.PeopleID = form.PeopleID.data
        people.FirstName = form.FirstName.data
        people.LastName = form.LastName.data
        people.Birthdate = datetime.Birthdate.now()
        people.Address = form.Address.data
        people.City = form.City.data
        people.State = form.State.data
        people.Zip = form.Zip.data
        people.PhoneNumber1 = form.PhoneNumber1.data
        people.PhoneNumber2 = form.PhoneNumber2.data
        people.Email = form.Email.data
        db.session.commit()

        flash('This patron has been updated!')
        return redirect(url_for('patron', PeopleID=people.PeopleID))

    form.PeopleID.data = people.PeopleID
    form.FirstName.data = people.FirstName
    form.LastName.data = people.LastName
    form.Birthdate.data = people.Birthdate
    form.Address.data = people.Address
    form.City.data = people.City
    form.State.data = people.State
    form.Zip.data = people.Zip
    form.PhoneNumber1.data = people.PhoneNumber1
    form.PhoneNumber2.data = people.PhoneNumber2
    form.Email.data = people.Email
    return render_template('update_people.html', form=form, pageTitle='Update People',legend="Update People")

@app.route('/people/<int:PeopleID>/delete', methods=['POST'])
def delete_people(PeopleID):
    if request.method == 'POST': #if it's a POST request, delete the patron from the database
        people = g2_peopletable.query.get_or_404(PeopleID)
        db.session.delete(people)
        db.session.commit()
        flash('Patron was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")

class circulationtable(db.Model):
    #__tablename__ = 'results'
    CheckoutID = db.Column(db.Integer, primary_key=True)
    MaterialID = db.Column(db.Integer)
    PeopleID = db.Column(db.Integer)
    Checkoutdate = db.Column(db.DateTime)
    Datedue = db.Column(db.DateTime)
def __repr__(self):
    return "id: {0} | People ID: {1} | Material ID: {2} | Checkout Date: {3} | Date Due: {4}".format(self.CheckoutID, self.PeopleID, self.MaterialID, self.Checkoutdate, self.Datedue)

class CheckoutForm(FlaskForm):
    CheckoutID = IntegerField('Checkout ID: ')
    PeopleID = IntegerField('People ID: ')
    MaterialID = IntegerField('Material ID: ')
    Checkoutdate = DateField('Checkout Date:')
    Datedue = DateField('Date Due: ')

@app.route('/checkout')
def checkout():
    all_checkout = circulationtable.query.all()
    return render_template('checkout.html', checkout=all_checkout, pageTitle='Circulation List')

@app.route('/checkout/<int:CheckoutID>', methods=['GET','POST'])
def circulation(CheckoutID):
    checkout = circulationtable.query.get_or_404(CheckoutID)
    return render_template('checkout.html', form=checkout, pageTitle='Circulation Details')

if __name__ == '__main__':
    app.run(debug=True)
