from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def root():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()