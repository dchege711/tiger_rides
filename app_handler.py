"""
Implements an API to access the healthKenya database
Adding a line so that I can re-deploy. Heeeeroku!!!!!!
How much information do we give provide? Everything since it's in public domain?
"""

#_______________________________________________________________________________

from flask import Flask, jsonify, make_response, request, Response, render_template
from flask_cors import CORS, cross_origin
import os

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
def search_doctors():
    if request.method == 'POST':
        # list_of_attendees = {}
        # with open("people_coming.txt", "r") as attendee_list:
        #     for attendee in attendee_list:
        #         list_of_attendees.append(attendee)
        """
        attendees = {
            "CA": {
                "Don": 
            }
        }
        """
        
        list_of_attendees = [
            {
                "name": "Don",
                "location": "California",
                "size": "2"
            },
            {
                "name": "Pamela",
                "location": "New Jersey",
                "size": "4"
            },
        ]
                
        results_in_html = []
        for result in list_of_attendees:
            results_in_html.append(tiger_cards(result))
        
        return jsonify(results_in_html)
    
    elif request.method == 'GET':
        return "OK", 200

def tiger_cards(attendee_details):
    """
    Example: 
    <div class="w3-card w3-light-gray">        
        <p>Name<br>Location<br>Size<br></p>
    </div>
    """
    return ''.join([
        '<div class="w3-card w3-padding-16 w3-light-gray"><p>',
        attendee_details["name"], "<br>", attendee_details["location"],
        "<br>", attendee_details["size"], "<br></p></div>"
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
