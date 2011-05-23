#-*- conding:utf-8 -*-
"""
Author: Jan Palach
Contact: palach@gmail.com
"""
import os
from flask import Module, Flask, jsonify, render_template, request, session, redirect, url_for, flash
from werkzeug import secure_filename

from utilities.vtk_reader import VTKReader

from persistence.database import Base, db_session, engine
from persistence.models import User, VTKModels

from helper_functions import allowed_files


UPLOAD_FOLDER = "../model_files"

frontend = Module(__name__)


@frontend.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif session["logged_in"] == True:
        return redirect(url_for('main'))
    return redirect(url_for('login'))


@frontend.route('/main', methods=['GET', 'POST'])
def main():
    error = None
    models = VTKModels.query.filter(VTKModels.user_id == session['user_id']).all()#.first()

    return render_template("main.html", models=models)


@frontend.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.get_user(request.form['email'], request.form['password'])

        if user is not None:
            session['logged_in'] = True
            session['user_id'] = user.id
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@frontend.route('/logout')
def logout():
    session.pop('logged_in', False)
    return redirect(url_for('index'))


@frontend.route('/register-user', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        user = User(
                request.form['name'],
                request.form['email'],
                request.form['password']
                )
        db_session.add(user)
        db_session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@frontend.route('/expose-model', methods=['GET', 'POST'])
def expose_model():
    if request.method == 'POST':
        model = VTKModels.query.filter(VTKModels.id == int(request.form['model_select'])).first()
        reader = VTKReader()
        reader.read(model.path, model.type)
        
        dataset_geometry = jsonify(
                            vertices = [vertice for vertice in reader.vertices],
                            indices = [id for id in reader.indices]
                       )
    
        return render_template('models.html', dataset=dataset_geometry)
    return redirect(url_for('main'))


@frontend.route('/register-model', methods=['GET', 'POST'])
def register_model():
    """
    This funtion allow a user to submit a vtk 3D model.
    """
    if request.method == 'POST' and session["logged_in"] == True:
        user_id = session['user_id']
        file = request.files['model_file']

        dir_path = os.path.join(UPLOAD_FOLDER, str(session['user_id']))
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        path = os.path.join(dir_path,file.filename)

        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            file.save(path)

        model = VTKModels(
                    user_id,
                    request.form['model_title'],
                    request.form['model_description'],
                    request.form['model_dataset_type'],
                    path
                )

        db_session.add(model)
        db_session.commit()
    return redirect(url_for('main'))

