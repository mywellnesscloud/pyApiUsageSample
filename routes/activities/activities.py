import base64
import json
import requests
import infrastructure
from flask import Blueprint, redirect, request, render_template, abort, session


__author__ = 'carlozamagni'

activities_app = Blueprint('activities', __name__, static_folder='static', template_folder='templates')

requests_headers = {'Content-Type': 'application/json',
                    'X-MWAPPS-OAUTHCLIENTID': infrastructure.my_wellness_api_app_id}


@activities_app.route('/timeseries/')
@activities_app.route('/timeseries/<data_type>')
def time_series(data_type=''):
    user_id = session.get('user_id', None)
    user_token = session.get('user_token', None)

    if user_id is None or user_token is None:
        # go and authorize before uploading
        return redirect('/authorize')

    if len(data_type) == 0 or data_type not in ['Move', 'Calories', 'RunningDistance', 'CyclingDistance']:
        return render_template('/activities/time_series.html')

    time_series_url = '%s/api/v1/ActivityStream/%s/TimeSeries' % (infrastructure.my_wellness_api_base_url, '201408')
    response = requests.get(url=time_series_url,
                            data=json.dumps({'dataType': data_type, 'token': user_token}),
                            headers=requests_headers)

    if response.status_code != 200:
        render_template('/activities/time_series.html')

    response_data = (json.loads(response.content))['data']

    labels = []
    data = []
    for d in response_data['days']:
        labels.append(str(d['day'])[-2:len(str(d['day']))])
        data.append(int(d['value']))

    return render_template('/activities/time_series.html', labels=json.dumps(labels), series_data=json.dumps(data))


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
        url = '%s/api/v1/User/%s/UploadActivity' % (infrastructure.my_wellness_api_base_url, user_id)
        payload = {'Token': unicode(user_token),
                   'DataType': (uploaded_file.filename.split('.')[-1]).lower(),
                   'Data': base64.b64encode(uploaded_file.read())}

        res = requests.post(url=url,
                            data=json.dumps(payload),
                            headers=requests_headers,
                            verify=infrastructure.verify_ssl_cert)

        print(res.content)

        result = json.loads(res.content)
        success = False if 'errors' in res.content else True

        return render_template('/activities/upload_result.html', success=success, result=result)


def _is_valid_file(file):
    u_file_name = file.filename.upper()
    return '.FIT' in u_file_name or '.TCX' in u_file_name


def _get_current_user_or_login():
    user_id = session.get('user_id', None)
    user_token = session.get('user_token', None)

    if user_id is None or user_token is None:
        # go and authorize before uploading
        return redirect('/authorize')

    return user_id, user_token