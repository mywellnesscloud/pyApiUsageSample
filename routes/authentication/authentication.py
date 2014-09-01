import json
from flask import Blueprint, redirect, request, render_template, session, jsonify
import infrastructure
import requests

__author__ = 'carlozamagni'


auth_app = Blueprint('catalog', __name__, static_folder='static', template_folder='templates')

redirect_uri = ''

@auth_app.route('/')
def authorize():
    url = 'https://usertestext.mywellness.com:13443/cloud/OAuthApplication/Login?client_id=%s&redirect_uri=%s&scope=%s&state=state' % (infrastructure.my_wellness_api_app_id, redirect_uri, 'write')
    return redirect(url)

@auth_app.route('/exchange')
def exchange():
    code = request.args.get('code')

    headers = {'Content-Type': 'application/json'}

    try:
        authorize_url = 'http://servicestestext.mywellness.com/OAuth/58FB87D2-B9C1-45D1-83CE-F92C64E787AF/GetAccessToken'
        request_payload = {'code': code, 'client_id': infrastructure.my_wellness_api_app_id,
                           'client_secret': infrastructure.my_wellness_api_app_secret,
                           'grant_type': 'authorization_code',
                           'redirect_uri': redirect_uri}

        response = requests.post(authorize_url,
                                 data=json.dumps(request_payload),
                                 headers=headers)
    except Exception, e:

        return 'error %s' % str(e)
    content = json.loads(response.content)

    return render_template('/authorized_user.html')