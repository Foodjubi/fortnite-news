from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        nom = request.form['NOM']
        prenom = request.form['PRENOM']
        email = request.form['EMAIL']
        return redirect(url_for(".test", nom=nom, prenom=prenom, email=email))
    except:
        return render_template("index.html", linkbr="/brnews", linkstw="/stwnews", linkmap="/map", linkbanners="/banners", linkgetplayer="/getplayer")


@app.route("/getplayer", methods=["GET", "POST"])
def getplayer():
    try:
        name = request.form['name']
        type = request.form.get('checkbox')
        print(type)
        inttype = int(type)

        if inttype == 1:
            accounttype = "epic"
            return redirect(url_for(".playerstats", name=name, type=accounttype))
        elif inttype == 2:
            accounttype = "psn"
            return redirect(url_for(".playerstats", name=name, type=accounttype))
        elif inttype == 3:
            accounttype = "xbl"
            return redirect(url_for(".playerstats", name=name, type=accounttype))

    except:
        return render_template("getplayer.html")


@app.route("/playerstats", methods=["GET", "POST"])
def playerstats():
    try:
        name = request.args['name']
        accounttype = request.args['type']
        url = 'https://fortnite-api.com/v2/stats/br/v2'
        headers = {
            'Authorization': 'd1341b3c-4723-4ff6-a667-153f6c9f238d'
        }

        params = {
            'name': name,
            'accountType': accounttype
        }
        rep = requests.get(url, headers=headers, params=params)
        jsonn = rep.json()

        all = jsonn['data']['stats']['all']
        minutesPlayed = all['overall']["minutesPlayed"]
        hoursPlayed = minutesPlayed / 60
        daysPlayed = hoursPlayed / 24
        idcount = jsonn["data"]
        # with open("fooddata.json", "w", encoding='utf-8') as jsonfile:
        #     json.dump(jsonn, jsonfile, ensure_ascii=False, indent= 4)
        return render_template("playerstats.html", idcount=idcount, name=name, all=all, solo=jsonn['data']['stats']['all']['trio'] , hoursPlayed=round(hoursPlayed, 1), daysPlayed=round(daysPlayed, 1), battlePass=jsonn['data']["battlePass"])
    except:
        return render_template("errorplayerstats.html", linkgetplayer="/getplayer")


@app.route("/test", methods=["GET", "POST"])
def test():
    nom = request.args['nom']
    prenom = request.args['prenom']
    email = request.args['email']
    return render_template("test.html", nom=nom, prenom=prenom, email=email)


@app.route("/map")
def map():
    url = 'https://fortnite-api.com/v1/map'
    params = {
        'language': 'fr'
    }
    rep = requests.get(url, params=params)
    jsonn = rep.json()
    return render_template("map.html", link_image=jsonn['data']['images']['pois'])


@app.route("/banners")
def banners():
    url = 'https://fortnite-api.com/v1/banners'
    params = {
        'language': 'fr'
    }
    rep = requests.get(url, params=params)
    jsonn = rep.json()
    # embedvar = discord.Embed(title=jsonn["data"][r]["name"], description=f"De : {jsonn['data'][r]['devName']}",
    #                          color=0x00ff00)
    # embedvar.add_field(name="Catégorie : ", value=jsonn['data'][r]['category'])
    # embedvar.set_image(url=jsonn["data"][r]["images"]["icon"])
    return render_template("banner.html", data=jsonn["data"])


@app.route("/stwnews")
def stwNews():
    url = 'https://fortnite-api.com/v2/news/stw'
    params = {
        'language': 'fr'
    }
    rep = requests.get(url, params=params)
    jsonn = rep.json()
    # with open('stw.json', encoding='utf-8') as mon_fichier:
    #     jsonn = json.load(mon_fichier)
    return render_template("stwnews.html", data=jsonn["data"]["messages"], len_data=len(jsonn["data"]["messages"]))


@app.route("/brnews")
def brNews():
    url = 'https://fortnite-api.com/v2/news/br'
    params = {
        'language': 'fr'
    }
    rep = requests.get(url, params=params)
    jsonn = rep.json()
    # with open('example.json', encoding='utf-8') as mon_fichier:
    #     jsonn = json.load(mon_fichier)
    return render_template("brnews.html", data=jsonn["data"]["motds"], len_data=len(jsonn["data"]["motds"]))


if __name__ == "__main__":
    app.run(debug=True)

