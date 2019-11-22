from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
import datetime
import secrets
#import os

#dbuser = os.environ.get('DBUSER')
#dbpass = os.environ.get('DBPASS')
#dbhost = os.environ.get('DBHOST')
#dbname = os.environ.get('DBNAME')

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

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
    Genre = DateField('Genre: ', validators=[DataRequired()])
    Author = StringField('Author:', validators=[DataRequired()])
    ISBN = IntegerField('ISBN:', validators=[DataRequired()])

@app.route('/')
def index():
    all_materials = g2_materialtable.query.all()
    return render_template('index.html', materials=all_materials, pageTitle='SLPL Materials')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = g2_materialtable.query.filter(or_(g2_materialtable.Title.like(search), g2_materialtable.DateAdded.like(search), g2_materialtable.LastModified.like(search), g2_materialtable.Genre.like(search), g2_materialtable.Author.like(search), g2_materialtable.ISBN.like(search))).all()
        return render_template('index.html', materials=results, pageTitle='SLPL Materials', legend="Search Results")

@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    form = MaterialForm()
    if form.validate_on_submit():
        material = g2_materialtable(MaterialID=form.MaterialID.data, Title=form.Title.data, DateAdded=datetime.DateAdded.now(),LastModified=datetime.LastModified.now(), Genre=form.Genre.data, Author=form.Author.data, ISBN=form.ISBN.data)
        db.session.add(material)
        db.session.commit()
        flash('New material was successfully added!')
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
        material.DateAdded = form.DateAdded.now()
        material.LastModified = datetime.LastModified.now()
        material.Genre = form.Genre.data
        material.Author = form.Author.data
        material.ISBN = form.ISBN.data
        db.session.commit()

        flash('This character has been updated!')
        return redirect(url_for('material', MaterialID=material.MaterialID))
    #elif request.method == 'GET':
    form.MaterialID.data = material.MaterialID
    form.Title.data = material.Title
    form.DateAdded.data = material.DateAdded
    form.lastModified.data = material.lastModified
    form.Genre.data = material.Genre
    form.Author.data = material.Author
    form.ISBN.data = material.ISBN
    return render_template('update_material.html', form=form, pageTitle='Update Material', legend="Update A Material")

@app.route('/material/<int:MaterialID>/delete', methods=['POST'])
def delete_material(MaterialID):
    if request.method == 'POST': #if it's a POST request, delete the material from the database
        material = g2_materialtable.query.filter_by(MaterialID=MaterialID).first()
        db.session.delete(material)
        db.session.commit()
        flash('Material was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
