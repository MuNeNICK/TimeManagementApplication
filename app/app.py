from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "開発頑張ろう"
