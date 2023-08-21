from flask import Flask, render_template
app = Flask(__name__)

@app.route('/alerts')
def alerts():
    return render_template("scraper.html")

@app.route('/')
def index():
    return render_template("index.html")