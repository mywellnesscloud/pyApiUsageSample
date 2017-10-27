import json
import urllib
import requests
import infrastructure
from flask import Blueprint, redirect, request, render_template, abort, session


__author__ = 'carlozamagni'


auth_app = Blueprint('authorize', __name__, static_folder='static', template_folder='templates')

# redirect_uri = 'http://localhost:5000/authorize/exchange'
redirect_uri = 'http://mywellnessapisample.herokuapp.com/authorize/exchange'
# oauth_step_1_url = '%s/cloud/OAuthApplication/Login' % infrastructure.my_wellness_api_auth_base_url
oauth_step_1_url = 'https://www-test.mywellness.com/oauth'
oauth_step_2_url = '{0}/OAuth/58FB87D2-B9C1-45D1-83CE-F92C64E787AF/GetAccessToken'.format('https://servicestestext.mywellness.com')


@auth_app.route('/')
def authorize():
    encoded_redirect_url = urllib.quote_plus(redirect_uri)
    url = '%s?client_id=%s&redirect_uri=%s&scope=%s&response_type=code' % (oauth_step_1_url, infrastructure.my_wellness_api_app_id, encoded_redirect_url, 'write')
    return redirect(url)


@auth_app.route('/exchange')
def exchange():
    code = request.args.get('code')
    headers = {'Content-Type': 'application/json'}

    try:
        request_payload = {'code': code,
                           'client_id': infrastructure.my_wellness_api_app_id,
                           'client_secret': infrastructure.my_wellness_api_app_secret,
                           'grant_type': 'authorization_code',
                           'redirect_uri': redirect_uri}

        response = requests.post(oauth_step_2_url,
                                 data=json.dumps(request_payload),
                                 headers=headers)

        content = json.loads(response.content)

        if content.get('error_code', None) is not None:
            abort(500)

        session['user_token'] = content['access_token']
        session['user_id'] = content['user_id']

    except Exception, e:
        abort(500)

    return render_template('/authentication/authorized_user.html', auth_result=content)