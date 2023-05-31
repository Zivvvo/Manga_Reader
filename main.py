from flask import Flask, render_template
from flask import redirect, url_for, request
import requests
import os

app = Flask(__name__)

class Cache():
    search_results = None
    selected_manga = None
    selected_page = None

stored_data = Cache()

@app.route("/", methods = ["POST","GET"])
def home():
    if request.method == 'POST':
      query = request.form['nm']
      url = os.path.join("https://api.consumet.org/manga/mangadex", query).replace("\\","/")
      print(url)
      response = requests.get(url)
      data = response.json()

      stored_data.search_results = data


      return redirect(url_for('success'))
    else:
        return render_template("home.html")

@app.route('/success')
def success():
    #render Manga Pages from search tool
    #print(stored_data.search_results)
    return render_template("success.html", data = stored_data.search_results)


@app.route("/search")
def search():
    return "search engine"

@app.route("/select", methods=['GET'])
def select():
    args = request.args

    url = "https://api.consumet.org/manga/mangadex/info/"+ args.get("id")
    
    print(url)

    response = requests.get(url)
    data = response.json()

    stored_data.selected_manga = data

    print(data)

    return render_template("select.html", data = stored_data.selected_manga)


@app.route("/about", methods= ["GET"])
def about():
    return render_template("about.html")

@app.route("/read", methods=["GET"])
def read():

    args = request.args

    url = "https://api.consumet.org/manga/mangadex/read/"+ args.get("id")
    response = requests.get(url)
    data = response.json()

    stored_data.selected_page = data

    return render_template("read.html", data = enumerate(data), data2 = data)


if __name__ == "__main__":
    app.run(debug = True)

