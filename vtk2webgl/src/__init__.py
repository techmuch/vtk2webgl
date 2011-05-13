"""
Author: Jan Palach
Contact: palach@gmail.com
"""

from flask import Flask

from vtkweb.persistence.database import db_session


app = Flask(__name__)
app.config.from_object('settings')

from vtkweb.controllers.admin import admin
from vtkweb.controllers.frontend import frontend

app.register_module(admin)
app.register_module(frontend)

@app.after_request
def shutdown_session(response):
    db_session.remove()
    return response
