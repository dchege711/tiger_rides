"""
Implements an API to access the healthKenya database
Adding a line so that I can re-deploy. Heeeeroku!!!!!!
How much information do we give provide? Everything since it's in public domain?
"""

#_______________________________________________________________________________

from flask import Flask, jsonify, make_response, request, Response, render_template, send_file
from flask_cors import CORS, cross_origin
import os
from pprint import pprint

import filter_trips
from mongo_db_client import tiger_rides_db
import user_actions
import trip_actions

app = Flask(__name__)
CORS(app)   # This allows Cross-Origin-Resource-Sharing on all methods

#_______________________________________________________________________________

@app.route('/')
def index():
    """
    URLs directed to the homepage will land here
    """
    # return "Working on the REST API!"
    return render_template("index.html")

@app.route('/search/', methods=['POST', 'GET'])
def search_trips():
    if request.method == 'POST':
        state = request.get_json()["origin_state"]        
        list_of_attendees = filter_trips.get_travellers_from_state(state)
                
        results_in_html = """
        <div class='w3-responsive'><table class='w3-table-all'>
            <tr>
                <th>Name</th><th>Number of People Coming</th>
                <th>City</th><th>State</th>
            </tr>
        """
        for result in list_of_attendees:
            results_in_html = "".join([results_in_html, tiger_cards(result)])
            
        results_in_html = "".join([results_in_html, "</table></div>"])
        
        return jsonify(results_in_html)
    
    elif request.method == 'GET':
        return "OK", 200
    
@app.route('/static/img/logo/logo_cropped.png', methods=["GET"])
def get_logo():
    return send_file("./static/img/logo/logo_cropped.png", mimetype="image/png")

def tiger_cards(attendee_details):
    return ''.join([
        "<tr><td>", attendee_details["name"], "</td>",
        "<td>", attendee_details["size"], "</td>",
        "<td>", attendee_details["city"], "</td>",
        "<td>", attendee_details["state_abbr"], "</td>", "</tr>"
    ])
    
@app.route('/register/', methods=["POST", "GET"])
def register_new_users():
    if request.method == "GET":
        return render_template("new_member_registration.html")
    elif request.method == "POST":
        payload = request.get_json()
        
        found_duplicate = user_actions.is_in_db({"email_address": payload["email_address"]})
        if (found_duplicate):
            return jsonify({
                "registration_status": False,
                "registration_message": "That email address has already been taken."
            })
        
        successfully_registered_user = user_actions.register_user(payload)[0]
        if successfully_registered_user:
            return jsonify({
                "registration_status": True,
                "registration_message": "Successful registration. Now log in with your email address and password"
            })
        else:
            return jsonify({
                "registration_status": False,
                "registration_message": "Unsuccessful registration. Please try again after a few minutes."
            })
            
@app.route('/login/', methods=["GET", "POST"])
def handle_login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        payload = request.get_json()
        account = user_actions.get_user({
            "email_address": payload["email_address"],
            "password": payload["password"]
        })
        
        if account is None:
            return jsonify({
                "login_successful": False,
                "login_payload": "Incorrect password or email. Did you want to <a href='\register'>register</a>?"
            })
            
        else:
            results = {}
            results["first_name"] = account["first_name"]
            results["trips_owned"] = account["trips_owned"]
            results["trips_joined"] = account["trips_owned"]
            return jsonify({
                "login_successful": True,
                "login_payload": results
            })
            
@app.route('/read_trips/', methods=["POST"])
def read_trips():
    if request.method == "POST":
        try:
            payload = request.get_json()
            print("Payload:")
            print(payload)
            
            trip_ids = []
            
            if "trip_ids" in payload:
                trip_ids = payload["trip_ids"]
            
            elif "user_id" in payload:
                user_trips = user_actions.get_trips(payload["user_id"])
                if payload["get_user_owned"]:
                    trip_ids = user_trips["trips_owned"]
                else:
                    trip_ids = user_trips["trips_joined"]
                    
            relevant_trips = trip_actions.get_trips(trip_ids)
            
            print("Response:")
            pprint(relevant_trips)
            return jsonify(relevant_trips)
             
        except KeyError as e:
            print("Error:")
            print(e.message)
            return {}
        
@app.route("/update_trip/", methods=["POST"])
def update_trip():
    if request.method == "POST":
        payload = request.get_json()
        print("Payload:")
        pprint(payload)
        
        results = trip_actions.update_trip(payload)
        
        print("Response:")
        pprint(results)
        return jsonify(results)

#_______________________________________________________________________________

@app.route('/navigation.html')
def return_navbar():
    return render_template("navigation.html")

@app.errorhandler(404)
def notFoundError(error):
    # This probably isn't API friendly, but ¯\_(ツ)_/¯
    return make_response("Oh no... Page Not Found (︶︹︺)", 404)

#_______________________________________________________________________________

if __name__ == '__main__':
    app.run()

#_______________________________________________________________________________
