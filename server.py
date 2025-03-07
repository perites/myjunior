from flask import Flask

from decorators import catch_errors, required_structure

app = Flask(__name__)


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
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQV51n74T1DasDqtAQR9vchlb1LrowQyr31g&s",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQV51n74T1DasDqtAQR9vchlb1LrowQyr31g&s",
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


if __name__ == "__main__":
    app.run(debug=True)
