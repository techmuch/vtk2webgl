"""
Author: Jan Palach
Contact: palach@gmail.com
"""

from flask import Module

admin = Module(__name__, url_prefix='/admin')


@admin.route('/')
def index():
    return "admin index"

@admin.route('/login')
def login():
    pass

@admin.route('/logout')
def logout():
    pass

