# pip install flask
# flask run
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("frontend/tela.html")