from flask import Flask, session, request, redirect, make_response, g
import json
from MainServer.decorators import catch_errors, required_structure, jwt_required
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
# csrf = CSRFProtect(app)

CORS(app, supports_credentials=True)


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

    return redirect(
        'https://copy-helper.onrender.com/login?callback=https://myjunior-api-mokk.onrender.com/myjunior/auth/callback')


@app.route('/myjunior/auth/callback')
@catch_errors
def auth_callback():
    request_args = request.args
    data = request_args.get('data')
    credentials_dict = json.loads(urllib.parse.unquote(data))['credentials']

    user_info = get_user_info(credentials_dict['token'])
    access_code_from_email = hashlib.sha256((user_info['email'] + app.secret_key).encode()).hexdigest()
    if not access_code_from_email == session.get('access_code'):
        return {'message': f'Access code is not correct for {user_info["email"]}'}

    payload = {'sub': user_info['id']}
    jwt_token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")

    create_user_url = "https://myjunior-db.onrender.com/v1/users"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    json_data = {'credentials': credentials_dict}
    requests.post(create_user_url, headers=headers, json=json_data)

    return redirect(f"https://maker-copy.vercel.app/set-cookies?jwtToken={jwt_token}")


@app.route('/make/copies', methods=['POST'])
@catch_errors
@jwt_required
@required_structure(['domainId', 'date'])
def make_copies():
    request_args = request.json

    headers = {"Authorization": f"Bearer {g.jwt_token}"}

    DB_URL = 'https://myjunior-db.onrender.com/v1'
    domain_info = requests.get(DB_URL + f'/domains/{request_args["domainId"]}', headers=headers).json()
    user_info = requests.get(DB_URL + '/users', headers=headers).json()

    copies = requests.get('https://copy-helper.onrender.com/domain/copies', json=
    {
        'domain': {
            'name': domain_info['name'],
            'broadcastId': user_info['yourTeamBroadcastSheetID'],
            'broadcastPage': domain_info['pageInBroadcast']
        },
        'date': request_args['date'],
        "credentials": user_info['credentials']}
                          )

    result = []
    for copy_str in copies.json():
        if not copy_str:
            continue

        ready_copy = requests.post('https://copy-helper.onrender.com/copy/make',
                                   json={"credentials": user_info['credentials'],
                                         "domainInfo": domain_info,
                                         'userSettings': user_info,
                                         'copy': copy_str

                                         }).json()
        ready_copy['copyName'] = copy_str
        result.append(ready_copy)

    return result


if __name__ == "__main__":
    app.run(debug=True, port=5001)
