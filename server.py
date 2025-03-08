from flask import Flask, session, request, redirect
import json
from decorators import catch_errors, required_structure
import urllib.parse
import os
import pyotp
import requests
import hashlib
from flask_cors import cross_origin
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app_secret_key = os.getenv("SERVER_SECRET_KEY")
if not app_secret_key:
    raise ValueError('No server secret key provided')
app.secret_key = app_secret_key
csrf = CSRFProtect(app)


def get_user_info(credentials_token):
    url = "https://www.googleapis.com/oauth2/v2/userinfo"

    headers = {"Authorization": f"Bearer {credentials_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        raise Exception(
            f'Error while receiving user data. Response from google : {response.json()} status code : {response.status_code}')


@app.route('/myjunior/auth/login/web', methods=['GET'])
@catch_errors
def login():
    request_args = request.args
    access_code = request_args.get('access_code')
    if not access_code:
        return {'message': 'Access Code missing'}, 401

    session['auth'] = {'access_code': access_code, 'logged': False}

    return redirect('http://127.0.0.1:5000/login?callback=http://127.0.0.1:5001/myjunior/auth/callback/web')


@app.route('/myjunior/auth/callback/web')
@catch_errors
def web_callback():
    session_auth = session['auth']
    if not session_auth['logged']:
        session_auth['logged'] = True

        request_args = request.args
        data = request_args.get('data')

        credentials_dict = json.loads(urllib.parse.unquote(data))['credentials']

        session_auth['credentials'] = credentials_dict
        secret_totp_key = pyotp.random_base32()
        session_auth['secret_totp_key'] = secret_totp_key

        totp = pyotp.TOTP(secret_totp_key, interval=60)
        otp = totp.now()

        session['auth'] = session_auth

        return otp  # call for web app with otp password
    else:
        return {
            'message': 'Invalid callback call'
        }, 403


@app.route('/myjunior/auth/set-cookies')
@catch_errors
@cross_origin(origins="https://myfrontend.com")
def set_cookies():
    session_auth = session['auth']
    del session['auth']

    print(request.headers.get('Origin'))
    if request.headers.get('Origin') != 'https://myfrontend.com':
        return {'message': 'Wrong Origin'}, 403

    request_args = request.args
    otp = request_args.get('otp')
    if not otp:
        return {'message': 'OTP is missing'}, 401

    secret_totp_key = session_auth['secret_totp_key']
    totp = pyotp.TOTP(secret_totp_key, interval=60)

    if not totp.verify(otp):
        return {'message': 'OTP not valid'}, 403

    credentials_dict = session_auth['credentials']

    user_info = get_user_info(credentials_dict['token'])

    access_code_from_email = hashlib.sha256((user_info['email'] + app_secret_key).encode()).hexdigest()

    if not access_code_from_email == session_auth['access_code']:
        return {'message': f'Access code is not correct for {user_info['email']}'}

    return user_info  # responce.setcookies


# def check_cookies

if __name__ == "__main__":
    app.run(debug=True, port=5001)
