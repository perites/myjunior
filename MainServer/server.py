from flask import Flask, session, request, redirect, make_response, g
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
# csrf = CSRFProtect(app)

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


@app.route('/make/copies', methods=['POST'])
@catch_errors
# @jwt_required
@required_structure(['domainId', 'date'])
def make_copies():
    request_args = request.args

    # headers = {"Authorization": f"Bearer {g.jwt_token}"}

    domain_info = {
        'id': '121212',
        'name': 'WorldFinReport.com',
        "shortName": "TCI",
        "pageInBroadcast": 'IMG`24',
        "antiSpam": False,
        "trackingLinkInfo": {
            "type": "click",
            "start": "key123",
            "end": "key456"
        },
        "customPriorityUnsubLinkInfo": {
            "type": "",
            "start": "",
            "end": ""
        },
        "stylesSettings": {
            "fontSize": 14,
            "fontFamily": "Arial",
            "linksColor": "#1E90FF",
            "sidePadding": 30,
            "upperDownPadding": 20,
            "addAfterPriorityBlock": '<br><br>',
            "priorityFooterUrlTemplate": "https://alex-site.com/footer",
            "imageBlock": {
                "src": "https://alex-site.com/banner.jpg",
                "alt": "Exclusive Offer Banner"
            }
        },
        "template": ''
    }
    credentials = 'RECIVE FROM DB'

    user_info = {
        "yourTeamBroadcastSheetID": "1ZL2P0DOJvMkQqS3eKZaki5xYW0dkwXsLmMrdbFWxDTU",
        "FolderWithPartners": "1-WFEkKNjVjaJDNt2XKBeJhpIQUviBVim",
        "PriorityProductsTableId": "1e40khWM1dKTje_vZi4K4fL-RA8-D6jhp2wmZSXurQH0",

        "DefaultStyles": {
            "FontSize": "21px",
            "FontFamily": "Tahoma",
            "LinksColor": "#005fde",
            "SidePadding": "30px",
            "UpperDownPadding": "10px",
            "AddAfterPriorityBlock": "<br><br>",
            "PriorityFooterUrlTemplate": "<b><a target=\"_blank\" href=\"PRIORITY_FOOTER_URL\" style=\"text-decoration: underline; color: #ffffff;\">PRIORITY_FOOTER_TEXT_URL</a></b>",
            "ImageBlock": "<table align=\"center\"><tr>\n  <td height=\"20\" width=\"100%\" style=\"max-width: 100%\" class=\"horizontal-space\"></td>\n</tr>\n<tr>\n  <td class=\"img-bg-block\" align=\"center\">\n    <a href=\"urlhere\" target=\"_blank\">\n      <img alt=\"ALT_TEXT\" height=\"auto\" src=\"IMAGE_URL\" style=\"border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;max-width: 550px;font-size:13px;\" width=\"280\" />\n        </a>\n  </td>\n</tr>\n<tr>\n  <td height=\"20\" width=\"100%\" style=\"max-width: 100%\" class=\"horizontal-space\"></td>\n</tr></table>"
        },
        "AntiSpamReplacements": {
            "A": "А",
            "E": "Е",
            "I": "І",
            "O": "О",
            "P": "Р",
            "T": "Т",
            "H": "Н",
            "K": "К",
            "X": "Х",
            "C": "С",
            "B": "В",
            "M": "М",
            "e": "е",
            "y": "у",
            "i": "і",
            "o": "о",
            "a": "а",
            "x": "х",
            "c": "с",
            "%": "％",
            "$": "＄"
        }
    }

    copies = requests.get('http://127.0.0.1:5000/domain/copies', json=
    {
        'domainInfo': {
            'name': domain_info['name'],
            'pageInBroadcast': domain_info['pageInBroadcast']
        },
        'broadcastId': user_info['yourTeamBroadcastSheetID'],
        'date': '2/16',
        "credentials": credentials}
                          )

    result = []
    for copy_str in copies.json():
        if not copy_str:
            continue

        ready_copy = requests.post('http://127.0.0.1:5000/copy/make', json={"credentials": credentials,
                                                                            "domainInfo": domain_info,
                                                                            'userSettings': user_info,
                                                                            'copy': copy_str

                                                                            }).json()
        ready_copy['copyName'] = copy_str
        result.append(ready_copy)

    return result


if __name__ == "__main__":
    app.run(debug=True, port=5001)
