from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import datetime
from datetime import date, timedelta
import pymysql
#import secrets
from time import strftime
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)


app = Flask(__name__)

app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class g2_materialtable(db.Model):
    #__tablename__ = 'results'
    MaterialID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255))
    Genre = db.Column(db.String(255))
    Author = db.Column(db.String(255))
    ISBN = db.Column(db.String(255))
    DateAdded = db.Column(db.DateTime)
    LastModified = db.Column(db.DateTime)

    def __repr__(self):
        return "id: {0} | Title: {1} | Genre: {2} | Author: {3} | ISBN: {4} | Date Added: {5} | Last Modified: {6}".format(self.MaterialID, self.Title, self.Genre, self.Author, self.ISBN, self.DateAdded, self.LastModified)

class MaterialForm(FlaskForm):
    MaterialID = IntegerField('Material ID: ')
    Title = StringField('Title: ', validators=[DataRequired()])
    Genre = StringField('Genre: ', validators=[DataRequired()])
    Author = StringField('Author: ', validators=[DataRequired()])
    ISBN = IntegerField('ISBN: ', validators=[DataRequired()])
    DateAdded = DateField('Date Added (YYYY-MM-DD): ')
    LastModified = DateField('Date Last Modified: ')

@app.route('/')
def index():
    return render_template('index.html', pageTitle='South Liberty Public Library')

@app.route('/materials')
def materials():
    all_materials = g2_materialtable.query.all()
    return render_template('materials.html', materials=all_materials, pageTitle='Materials', legend='Materials')

@app.route('/searchmaterials', methods=['GET', 'POST'])
def search_materials():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = g2_materialtable.query.filter( or_(g2_materialtable.Title.like(search), g2_materialtable.Genre.like(search), g2_materialtable.Author.like(search), g2_materialtable.ISBN.like(search), g2_materialtable.DateAdded.like(search), g2_materialtable.LastModified.like(search))).all()
        return render_template('materials.html', materials=results, pageTitle="Materials", legend ="Update A Material")
    else:
        return redirect('/')

@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    form = MaterialForm()
    if form.validate_on_submit():
        material = g2_materialtable(Title=form.Title.data, Genre=form.Genre.data, Author=form.Author.data, ISBN=form.ISBN.data, DateAdded=form.DateAdded.data, LastModified=datetime.datetime.now())
        db.session.add(material)
        db.session.commit()
        flash('Material was successfully added!')
        return redirect("/materials")
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
        material.Title = form.Title.data
        material.Genre = form.Genre.data
        material.Author = form.Author.data
        material.ISBN = form.ISBN.data
        material.DateAdded = form.DateAdded.data
        material.LastModified = datetime.datetime.now()
        db.session.commit()
        flash('This material has been updated!')
        return redirect(url_for('material', MaterialID=material.MaterialID))

    form.MaterialID.data = material.MaterialID
    form.Title.data = material.Title
    form.Genre.data = material.Genre
    form.Author.data = material.Author
    form.ISBN.data = material.ISBN
    form.DateAdded.data = material.DateAdded
    form.LastModified.data = material.LastModified
    return render_template('update_material.html', form=form, pageTitle='Update Material',legend="Update A Material")

@app.route('/material/<int:MaterialID>/delete', methods=['POST'])
def delete_material(MaterialID):
    if request.method == 'POST': #if it's a POST request, delete the material from the database
        material = g2_materialtable.query.get_or_404(MaterialID)
        db.session.delete(material)
        db.session.commit()
        flash('Material was successfully deleted!')
        return redirect("/materials")
    else: #if it's a GET request, send them to the home page
        return redirect("/")

class g2_peopletable(db.Model):
    #__tablename__ = 'results'
    PeopleID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(255))
    LastName = db.Column(db.String(255))
    Birthdate = db.Column(db.String(255))
    Address = db.Column(db.String(255))
    City = db.Column(db.String(255))
    State = db.Column(db.String(255))
    Zip = db.Column(db.Integer)
    PhoneNumber1 = db.Column(db.Integer)
    PhoneNumber2 = db.Column(db.Integer)
    Email = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | First Name: {1} | Last Name: {2} | Birthdate: {3} | Address: {4} | City: {5} | State: {6} | Zip: {7} | Phone Number 1: {8} | Phone Number 2: {9} | Email: {10}".format(self.PeopleID, self.FirstName, self.LastName, self.Birthdate, self.Address, self.City, self.State, self.Zip, self.PhoneNumber1, self.PhoneNumber2, self.Email)

class PeopleForm(FlaskForm):
    PeopleID = IntegerField('People ID: ')
    FirstName = StringField('First Name: ', validators=[DataRequired()])
    LastName = StringField('Last Name: ', validators=[DataRequired()])
    Birthdate = StringField('Birthdate (YYYY-MM-DD): ', validators=[DataRequired()])
    Address = StringField('Address: ', validators=[DataRequired()])
    City = StringField('City: ', validators=[DataRequired()])
    State = StringField('State: ', validators=[DataRequired()])
    Zip = IntegerField('Zip: ', validators=[DataRequired()])
    PhoneNumber1 = IntegerField('Phone Number 1: ', validators=[DataRequired()])
    PhoneNumber2 = IntegerField('Phone Number 2: ')
    Email = StringField('Email: ', validators=[DataRequired()])

@app.route('/people')
def people():
    all_people = g2_peopletable.query.all()
    return render_template('people.html', people=all_people, pageTitle='Patrons', legend='Patrons')

@app.route('/searchpeople', methods=['GET', 'POST'])
def search_people():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = g2_peopletable.query.filter( or_(g2_peopletable.FirstName.like(search), g2_peopletable.LastName.like(search), g2_peopletable.Birthdate.like(search), g2_peopletable.Address.like(search), g2_peopletable.City.like(search), g2_peopletable.State.like(search), g2_peopletable.Zip.like(search), g2_peopletable.PhoneNumber1.like(search), g2_peopletable.PhoneNumber2.like(search), g2_peopletable.Email.like(search))).all()
        return render_template('people.html', people=results, pageTitle="People")

    else:
        return redirect('/')

@app.route('/add_people', methods=['GET', 'POST'])
def add_people():
    form = PeopleForm()
    if form.validate_on_submit():
        people = g2_peopletable(FirstName=form.FirstName.data, LastName=form.LastName.data, Birthdate=form.Birthdate.data, Address=form.Address.data, City=form.City.data, State=form.State.data, Zip=form.Zip.data, PhoneNumber1=form.PhoneNumber1.data, PhoneNumber2=form.PhoneNumber2.data, Email=form.Email.data)
        db.session.add(people)
        db.session.commit()
        flash('Patron was successfully added!')
        return redirect('/people')
    return render_template('add_people.html', form=form, pageTitle='Add New Patron', legend="Add New Patron")


@app.route('/patron/<int:PeopleID>', methods=['GET','POST'])
def patron(PeopleID):
    patron = g2_peopletable.query.get_or_404(PeopleID)
    return render_template('patron.html', form=patron, pageTitle='Patron Details')

@app.route('/patron/<int:PeopleID>/update', methods=['GET','POST'])
def update_patron(PeopleID):
    patron = g2_peopletable.query.get_or_404(PeopleID)
    form = PeopleForm()

    if form.validate_on_submit():
        patron.FirstName = form.FirstName.data
        patron.LastName = form.LastName.data
        patron.Birthdate = form.Birthdate.data
        patron.Address = form.Address.data
        patron.City = form.City.data
        patron.State = form.State.data
        patron.Zip = form.Zip.data
        patron.PhoneNumber1 = form.PhoneNumber1.data
        patron.PhoneNumber2 = form.PhoneNumber2.data
        patron.Email = form.Email.data
        db.session.commit()

        flash('This patron has been updated!')
        return redirect(url_for('patron', PeopleID=patron.PeopleID))

    form.PeopleID.data = patron.PeopleID
    form.FirstName.data = patron.FirstName
    form.LastName.data = patron.LastName
    form.Birthdate.data = patron.Birthdate
    form.Address.data = patron.Address
    form.City.data = patron.City
    form.State.data = patron.State
    form.Zip.data = patron.Zip
    form.PhoneNumber1.data = patron.PhoneNumber1
    form.PhoneNumber2.data = patron.PhoneNumber2
    form.Email.data = patron.Email
    return render_template('update_patron.html', form=form, pageTitle='Update Patron',legend="Update People")

@app.route('/patron/<int:PeopleID>/delete', methods=['POST'])
def delete_patron(PeopleID):
    if request.method == 'POST': #if it's a POST request, delete the patron from the database
        people = g2_peopletable.query.get_or_404(PeopleID)
        db.session.delete(people)
        db.session.commit()
        flash('Patron was successfully deleted!')
        return redirect("/people")
    else: #if it's a GET request, send them to the home page
        return redirect("/")

class g2_circulationtable(db.Model):
    #__tablename__ = 'results'
    CheckoutID = db.Column(db.Integer, primary_key=True)
    PeopleID = db.Column(db.Integer, db.ForeignKey('g2_peopletable.PeopleID'), nullable=False)
    MaterialID = db.Column(db.Integer, db.ForeignKey('g2_materialtable.MaterialID'), nullable=False)
    Checkoutdate = db.Column(db.DateTime)
    Datedue = db.Column(db.DateTime)

def __repr__(self):
    return "id: {0} | People ID: {1} | Material ID: {2} | Checkout Date: {3} | Date due: {4}".format(self.CheckoutID, self.PeopleID, self.MaterialID, self.Checkoutdate, self.Datedue)

class CheckoutForm(FlaskForm):
    CheckoutID = IntegerField('Checkout ID: ')
    PeopleID = IntegerField('People ID: ')
    MaterialID = IntegerField('Material ID: ')
    Checkoutdate = DateField('Checkout Date:')
    Datedue = DateField('Date Due: ')

@app.route('/checkout')
def checkout():
    all_checkout = g2_circulationtable.query.all()
    return render_template('checkout.html', checkout=all_checkout, pageTitle='Circulation List')

@app.route('/checkout/<int:CheckoutID>', methods=['GET','POST'])
def circulation(CheckoutID):
    checkout = g2_circulationtable.query.get_or_404(CheckoutID)
    return render_template('checkout.html', form=checkout, pageTitle='Circulation Details')

@app.route('/searchcheckout', methods=['GET', 'POST'])
def search_checkout():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = g2_circulationtable.query.filter( or_(g2_circulationtable.PeopleID.like(search), g2_circulationtable.MaterialID.like(search), g2_circulationtable.Checkoutdate.like(search), g2_circulationtable.Datedue.like(search))).all()
        return render_template('checkout.html', checkout=results, pageTitle="People")

    else:
        return redirect('/')

@app.route('/add_checkout', methods=['GET', 'POST'])
def add_checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        checkout = g2_circulationtable(PeopleID=form.PeopleID.data, MaterialID=form.MaterialID.data, Checkoutdate=date.today(), Datedue=(date.today() + timedelta(days=14) ))
        db.session.add(checkout)
        db.session.commit()
        flash('Checkout successfully completed!')
        return redirect("/checkout")
    return render_template('add_checkout.html', form=form, pageTitle='Add A New Material', legend="Add A New Material")

@app.route('/circulation/<int:CheckoutID>', methods=['GET','POST'])
def g2_circulation(CheckoutID):
    checkout = g2_circulationtable.query.get_or_404(CheckoutID)
    return render_template('circulation.html', form=checkout, pageTitle='Circulation Details')

@app.route('/circulation/<int:CheckoutID>/delete', methods=['POST'])
def delete_checkout(CheckoutID):
    if request.method == 'POST': #if it's a POST request, delete the circulation from the database
        checkout = g2_circulationtable.query.get_or_404(CheckoutID)
        db.session.delete(checkout)
        db.session.commit()
        flash('Check-in was successfully completed!')
        return redirect("/checkout")

    else: #if it's a GET request, send them to the home page
        return redirect("/")

@app.route('/circulations/overdue')
def circulationsoverdue():
    overdue_circulations = g2_circulationtable.query.filter(g2_circulationtable.Datedue<date.today())
    return render_template('circulationsoverdue.html', circulations=overdue_circulations, pageTitle='Overdue Materials', legend='Overdue Materials')

@app.route('/circulations/duetoday')
def circulationsduetoday():
    duetoday_circulations = g2_circulationtable.query.filter(g2_circulationtable.Datedue==date.today())
    return render_template('circulationsduetoday.html', circulations=duetoday_circulations, pageTitle='Materials Due Today', legend='Materials Due Today')


if __name__ == '__main__':
    app.run(debug=True)
