from flask import Flask, session, request, redirect, make_response
import json
from decorators import catch_errors, required_structure, jwt_required
import urllib.parse
import os
import jwt
import requests
import hashlib
from flask_cors import cross_origin
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.getenv("SERVER_SECRET_KEY")
csrf = CSRFProtect(app)

CORS(app, origins=["https://toolza-alpha-7s37.vercel.app"], supports_credentials=True)


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


@app.route('/myjunior/auth/login', methods=['GET'])
@catch_errors
def login():
    request_args = request.args
    access_code = request_args.get('access_code')
    if not access_code:
        return {'message': 'Access Code missing'}, 401

    session['access_code'] = access_code

    return redirect('http://127.0.0.1:5000/login?callback=http://127.0.0.1:5001/myjunior/auth/callback')


@app.route('/myjunior/auth/callback')
@catch_errors
def auth_callback():
    request_args = request.args
    data = request_args.get('data')
    credentials_dict = json.loads(urllib.parse.unquote(data))['credentials']

    user_info = get_user_info(credentials_dict['token'])
    access_code_from_email = hashlib.sha256((user_info['email'] + app.secret_key).encode()).hexdigest()
    if not access_code_from_email == session.get('access_code'):
        return {'message': f'Access code is not correct for {user_info['email']}'}

    payload = {'sub': user_info['id']}
    jwt_token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")

    # create_user_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    # headers = {"Authorization": f"Bearer {jwt_token}"}
    # json_data = {'credentials': credentials_dict}
    # db_response = requests.get(create_user_url, headers=headers, json=json_data)
    # if not db_response.status_code == 200:
    #     return db_response.json(), db_response.status_code

    response = make_response(redirect("https://toolza-alpha-7s37.vercel.app"))  # change to front url
    response.set_cookie(
        "jwtToken",
        jwt_token,
        httponly=False,
        secure=True,
        samesite='None'
    )
    return response


# @app.route('/make/copies', methods=['POST'])
# @catch_errors
# @jwt_requared
# @required_structure(['domainId', 'date'])
# def make_copies():
#     headers = {"Authorization": f"Bearer {g.jwt_token}"}
#     response = requests.get(url, headers=headers)
#     domain_info = requests.get('')


if __name__ == "__main__":
    app.run(debug=True, port=5001)
