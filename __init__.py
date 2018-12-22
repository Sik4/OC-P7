from flask import Flask, render_template, request, jsonify
import json
import wikipedia
# from testapiwiki import wiki
# from testmapurl import mapurl

app = Flask(__name__)

with open('fr.json', 'r') as fp:
    town_list = json.load(fp)


# @app.route('/papybot')
# def do_search():
#   return jsonify(wiki())


@app.route('/background_process')
def background_process():
    try:
        lang = request.args.get("proglang", 0, type=str)
        if str(lang).lower() == 'montpellier':
            return jsonify(result='You are wise!')
        else:
            return jsonify(result='Well, you should change.')
    except Exception as e:
        return str(e)


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
                return jsonify(result="this is a french city", mapurl=url)

        return jsonify(result="nothing found")

    except Exception as e:
        return str(e)


@app.route('/wiki_process')
def wiki_process():
    try:
        lang = request.args.get("proglang", 0, type=str)
        wikipedia.set_lang("fr")
        ville = lang
        pageville = wikipedia.WikipediaPage(ville)
        print(pageville)

        # pop = wikipedia.WikipediaPage(ville)
        try:
            papyoutro = pageville.summary
            # papyoutro = str(re.search('[0-9]* *[0-9]+ habitants',pageville.summary).group())
            return jsonify(result=("D'ailleurs, savais tu que ", papyoutro, "?"))
        except Exception as er:
            return str(er)
    except Exception as e:
        return str(e)


@app.route('/index')
def interactive():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


app.run()
