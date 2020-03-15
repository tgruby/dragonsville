from flask import Flask, session
from flask import render_template
from flask import make_response
from controller import town
import common
import json

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
    # Inject no-cache commands into the header.
    resp = make_response(render_template("index.html"), 200)
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"  # HTTP 1.1.
    resp.headers["Pragma"] = "no-cache"  # HTTP 1.0.
    resp.headers["Expires"] = "0"  # Proxies.

    # First time loading the site so we need to load up the session.
    our_hero = common.load_hero()  # Load up our hero.  Auto-creates if we need a new one.
    session['controller'] = "town"  # Start in the town.
    session['our_hero'] = json.dumps(our_hero)
    session['view'] = town.init(our_hero)
    session['splash_screen'] = True  # Show the splash screen.

    return resp


# Receive a command from the browser and respond with a json object representing each panel.
@app.route('/command/<command_id>')
def command(command_id):

    # First grab the session state
    our_hero = session["our_hero"]
    controller = session["controller"]



    return {
        "stats_panel": None,
        "view_panel": None,
        "info_panel": None,
        "message_panel": None,
        "commands_panel": None
    }


if __name__ == '__main__':
    app.run()
