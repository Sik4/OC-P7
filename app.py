from flask import Flask, request, render_template, jsonify
import json
import wikipedia
import re
from functions import __parser__


app = Flask(__name__)

# put an ico icon for favicon error
# with open('fr.json', 'r') as fp:
#   town_list = json.load(fp)


@app.route('/')
def index():
    """Function to return the main template"""
    return render_template('base.html')


@app.route('/town_list_process')
def town_list_process():
    with open('fr.json', 'r') as fp:
        town_list = json.load(fp)

    try:
        lang = request.args.get("proglang", type=str)
        input = str(lang).lower()
        user_input = __parser__(input)
        for cities in town_list:
            print(cities["city"])
            handel = __parser__(cities["city"].lower())
            if re.match(r".*" + handel + ".*", user_input):
                latitude = cities["lat"]
                longitude = cities["lng"]
                wikipedia.set_lang("fr")
                ville = cities["city"]  # or lang but wiki is case sensitive for OpenClassrooms
                pageville = wikipedia.WikipediaPage(ville)
                API_KEY = "AIzaSyBkKrzwEFfXOQfGR46Qn1KZoUjN7oZ8Sg0"
                url = "https://maps.googleapis.com/maps/api/staticmap?center=" + user_input + "&zoom=12&size=400x400" \
                "&maptype=roadmap&markers=color:blue%7C"+ latitude + "," + longitude + "&key=" + API_KEY
                wikiresult = pageville.summary
                return jsonify(result=("D'ailleurs, savais tu que ", wikiresult, "?"), mapurl=url)
                # return jsonify({'output': render_template('index.html', result="this is a french city", mapurl=url)})

    except:
        print('Error')


