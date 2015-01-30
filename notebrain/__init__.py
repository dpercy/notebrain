
import os

from flask import Flask, abort, g, redirect, request, session
from flask.ext import openid
from flask.ext.mako import MakoTemplates, render_template
from flask.ext.mongoengine import MongoEngine


app = Flask(__name__)

app.config.from_object(os.environ['NOTEBRAIN_CONFIG'])
db = MongoEngine(app)
mako = MakoTemplates(app)

from .mod_auth.views import mod_auth as auth_module
app.register_blueprint(auth_module)

from  notebrain import views
