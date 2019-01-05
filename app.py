from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)

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
        lang = request.args.get("proglang", 0, type=str)
        user_input = str(lang).lower()
        for cities in town_list:
            if cities["city"].lower() == user_input:
                latitude = cities["lat"]
                longitude = cities["lng"]
                API_KEY = "AIzaSyBr59ta9mMfBqCcmIUysOKcGt9uHqgy-Qk"
                url = "https://maps.googleapis.com/maps/api/staticmap?center=" + user_input + "&zoom=12&size=400x400" \
                 "&markers=color:blue%7C"+ latitude + "%7C" + longitude + "key=" + API_KEY
                return jsonify({'output': render_template('index.html', result="this is a french city", mapurl=url)})

        return json.dumps({'output': "nothing found"})

    except Exception as e:
        return str(e)
