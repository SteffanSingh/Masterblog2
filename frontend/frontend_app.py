from flask import Flask, render_template
import requests


from flask_cors import CORS

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


param = {"page":1, "limit":10}
URL = "https://derbygeneral-sportclark-5002.codio.io/api/posts/pagination"
res = requests.get(URL, params=param)





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
