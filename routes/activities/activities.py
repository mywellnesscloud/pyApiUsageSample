import json
import requests
import infrastructure
from flask import Blueprint, redirect, request, render_template, abort, session


__author__ = 'carlozamagni'


activities_app = Blueprint('catalog', __name__, static_folder='static', template_folder='templates')



@activities_app.route('/upload', methods=['GET', 'POST'])
def activity_upload():
    user_id = session['user_id']
    user_token = session['user_token']

    if user_id is None or user_token is None:
        # go and authorize before uploading
        return redirect('')

    if request.method == 'GET':
        return render_template('/activities/upload.html')

    pass