"""
Author: Jan Palach
Contact: palach@gmail.com
"""

from flask import Flask

from persistence.database import db_session
from controllers.admin import admin
from controllers.frontend import frontend


app = Flask(__name__)
app.config.from_object('settings')
app.register_module(admin)
app.register_module(frontend)

@app.after_request
def shutdown_session(response):
    db_session.remove()

    return response

app.run(host='127.0.0.1', port=8000)

