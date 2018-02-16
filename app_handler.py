"""
Implements an API to access the healthKenya database
Adding a line so that I can re-deploy. Heeeeroku!!!!!!
How much information do we give provide? Everything since it's in public domain?
"""

#_______________________________________________________________________________

from flask import Flask, jsonify, make_response, request, Response, render_template, send_file
from flask_cors import CORS, cross_origin
import os
import filter_trips

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
