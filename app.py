from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
import secrets
import datetime

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
app = Flask(__name__)

app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
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
        return redirect('/')

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


if __name__ == '__main__':
    app.run(debug=True)
