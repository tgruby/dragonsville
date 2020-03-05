from flask import Flask, session
from flask import render_template

# System Design:
#   Store character in the database as well as the dungeons.
#   Store current state in a cookie.
#   Create a simple Command API.
#   APIs should be called to update the
app = Flask(__name__, static_url_path='/static')
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'garbage_in_garbage_out'


# Draw the initial single page application
@app.route('/')
def root():
    return render_template("index.html")


@app.route('/command')
def root():
    current_controller = session['controller']
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
