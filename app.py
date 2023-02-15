from flask import Flask
from flask_cors import CORS
app= Flask(__name__)

CORS(app)


@app.route("/get")
def get():
    return "i am bilal "

if __name__ == "__main__":
    app.run(debug=True)


import controller