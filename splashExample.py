from flask import Flask, jsonify, make_response, request, render_template, send_file
from flask_cors import CORS
import os
from pprint import pprint
import filter_trips
from mongo_db_client import tiger_rides_db
import user_actions
import trip_actions
import sample_send
import smtplib
app = Flask(__name__)
CORS(app)

@app.route('/splashExample.html')
def return_navbar():
    """
    Returns the Navigation Bar. I'm planning on deprecating this and using the
    app_files dictionary in an app.route() that catches all mismatches.

    """
    return render_template("splashExample.html")
