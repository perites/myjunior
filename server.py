from flask import Flask
from flask_cors import CORS
from decorators import catch_errors, required_structure

app = Flask(__name__)
CORS(app, supports_credentials=True)
DOMAINS = [
    {
        'id': '121212',
        'name': 'TheClassyInvestor.com',
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
        "template": "<html><body><h1>Exclusive Offer Just for You!</h1><p>Click the link below to claim your discount now!</p></body></html>"
    },
    {
        'id': '101010',
        'name': 'StateOfMoney.com',
        "shortName": "SOM",
        "pageInBroadcast": 'IMG`24',
        "antiSpam": False,
        "trackingLinkInfo": {
            "type": "view",
            "start": "key112",
            "end": "key334"
        },
        "customPriorityUnsubLinkInfo": {
            "type": "unsubscribe",
            "start": "key556",
            "end": "key778"
        },
        "stylesSettings": {
            "fontSize": 16,
            "fontFamily": "Roboto",
            "linksColor": "#FF5733",
            "sidePadding": 20,
            "upperDownPadding": 25,
            "addAfterPriorityBlock": '',
            "priorityFooterUrlTemplate": "https://myportfolio.alex/footer",
            "imageBlock": {
                "src": "https://myportfolio.alex/banner.jpg",
                "alt": "Personal Portfolio Offer"
            }
        },
        "template": "<html><body><h1>Your Personal Portfolio Awaits!</h1><p>Don't miss your chance to get exclusive access!</p></body></html>"
    },
    {
        'id': '2020',
        'name': 'TheBruhDomain.com',
        "shortName": "TBD",
        "pageInBroadcast": 'platoon',
        "antiSpam": False,
        "trackingLinkInfo": {
            "type": "click",
            "start": "key999",
            "end": "key333"
        },
        "customPriorityUnsubLinkInfo": {
            "type": "unsubscribe",
            "start": "key555",
            "end": "key888"
        },
        "stylesSettings": {
            "fontSize": 15,
            "fontFamily": "Verdana",
            "linksColor": "#32CD32",
            "sidePadding": 15,
            "upperDownPadding": 30,
            "addAfterPriorityBlock": '<br><br><br>',
            "priorityFooterUrlTemplate": "https://alex-dev.io/footer",
            "imageBlock": {
                "src": "https://alex-dev.io/banner.jpg",
                "alt": "Developer Tools Offer"
            }
        },
        "template": "<html><body><h1>Special Discount for Developers!</h1><p>Claim your offer now and enhance your development tools!</p></body></html>"
    }

]


@app.route('/make/copies', methods=['POST'])
@catch_errors
@required_structure(['domainId', 'date'])
def make_copies():
    return [
        {

            "copyName": "RHOB235",
            "copyHtml": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>RHOB235 Page</title>\n    <style>\n        body { font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; }\n        h1 { color: #333; }\n        p { font-size: 16px; }\n    </style>\n</head>\n<body>\n    <h1>Welcome to RHOB235</h1>\n    <p>This is a simple example page for RHOB235.</p>\n    <img src=\"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQV51n74T1DasDqtAQR9vchlb1LrowQyr31g&s\" alt=\"Image 1\">\n    <img src=\"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQV51n74T1DasDqtAQR9vchlb1LrowQyr31g&s\" alt=\"Image 2\">\n    <img src=\"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQV51n74T1DasDqtAQR9vchlb1LrowQyr31g&s\" alt=\"Image 3\">\n</body>\n</html>",
            "copySLS": [
                "Simple page for RHOB235"
            ],
            "copyImagesUrls": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQV51n74T1DasDqtAQR9vchlb1LrowQyr31g&s"
            ]
        },
        {

            "copyName": "MPEE25",
            "copyHtml": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>MPEE25 Page</title>\n    <style>\n        body { font-family: Verdana, sans-serif; padding: 20px; background: #e3f2fd; }\n        h1 { color: #0277bd; }\n        .content { padding: 10px; background: white; border-radius: 5px; }\n    </style>\n</head>\n<body>\n    <div class=\"content\">\n        <h1>Welcome to MPEE25</h1>\n        <p>This is another example page for MPEE25.</p>\n        <img src=\"https://media1.tenor.com/m/UfA8GLtoGIIAAAAC/%D0%BA%D0%BE%D0%BF%D0%B8%D0%BC-%D1%8D%D0%BB%D0%B8%D0%BA.gif\" alt=\"Image 1\">\n        <img src=\"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQV51n74T1DasDqtAQR9vchlb1LrowQyr31g&s\" alt=\"Image 2\">\n    </div>\n</body>\n</html>",
            "copySLS": [
                "Уникальное предложение только сегодня: получите скидку 50% на всю продукцию!",
                "Не упустите шанс! Последний день распродажи с невероятными скидками и бонусами!",
                "Эксклюзивный доступ к новым товарам: станьте первым, кто их увидит!",
                "Уникальное предложение только сегодня: получите скидку 50% на всю продукцию!",
                "Не упустите шанс! Последний день распродажи с невероятными скидками и бонусами!",
                "Эксклюзивный доступ к новым товарам: станьте первым, кто их увидит!",
                "Уникальное предложение только сегодня: получите скидку 50% на всю продукцию!",
                "Не упустите шанс! Последний день распродажи с невероятными скидками и бонусами!",
                "Эксклюзивный доступ к новым товарам: станьте первым, кто их увидит!"
            ],
            "copyImagesUrls": [
                "https://media1.tenor.com/m/UfA8GLtoGIIAAAAC/%D0%BA%D0%BE%D0%BF%D0%B8%D0%BC-%D1%8D%D0%BB%D0%B8%D0%BA.gif",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQV51n74T1DasDqtAQR9vchlb1LrowQyr31g&s"
            ]
        }
    ]


@app.route('/user/domains', methods=['GET'])
@catch_errors
def user_domains():
    return [
        {
            'id': '121212',
            'name': 'TheClassyInvestor.com'},
        {
            'id': '101010',
            'name': 'StateOfMoney.com'
        },
        {
            'id': '2020',
            'name': 'TheBruhDomain.com'
        }
    ]


@app.route('/user/domains/<domain_id>')
@catch_errors
def domain_settings(domain_id):
    for domain_info in DOMAINS:
        if domain_info['id'] == domain_id:
            return domain_info, 200

    return {'message': 'Domain with specified id not found in current user'}, 400


if __name__ == "__main__":
    app.run(debug=True)
