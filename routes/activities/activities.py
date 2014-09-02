import base64
import json
import requests
import infrastructure
from flask import Blueprint, redirect, request, render_template, abort, session


__author__ = 'carlozamagni'


activities_app = Blueprint('activities', __name__, static_folder='static', template_folder='templates')

base_url = 'https://servicestestext.mywellness.com'

@activities_app.route('/upload', methods=['GET', 'POST'])
def activity_upload():
    user_id = session.get('user_id', None)
    user_token = session.get('user_token', None)

    if user_id is None or user_token is None:
        # go and authorize before uploading
        return redirect('/authorize')

    if request.method == 'GET':
        return render_template('/activities/upload.html')

    uploaded_file = request.files['file']
    if uploaded_file and _is_valid_file(uploaded_file):
        url = '%s/api/v1/User/%s/UploadActivity' % (base_url, user_id)
        payload = {'Token': user_token,
                   'DataType': (uploaded_file.filename.split('.')[-1]).lower(),
                   'Data': base64.b64encode(uploaded_file.read())}

        req = requests.post(url=url,
                            data=json.dumps(payload),
                            headers={'Content-Type': 'application/json'})

        print(req.content)

        return render_template('/activities/upload_result.html', result='')


def _is_valid_file(file):
    u_file_name = file.filename.upper()
    return '.FIT' in u_file_name or '.TCX' in u_file_name