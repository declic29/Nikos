from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

DUCK_LITE_URL = "https://lite.duckduckgo.com/lite/"

def search_duck_lite(query):
    payload = {"q": query + " langue:fr"}
    r = requests.post(DUCK_LITE_URL, data=payload)
    soup = BeautifulSoup(r.text, "html.parser")
    results = []
    for link in soup.select("a.result-link"):
        url = link.get("href")
        title = link.text.strip()
        try:
            req = requests.get(url, timeout=2)
            if req.status_code != 200:
                url = "https://web.archive.org/web/*/" + url
        except:
            url = "https://web.archive.org/web/*/" + url
        results.append({"title": title, "url": url})
    return results

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q")
    results = []
    if query:
        results = search_duck_lite(query)
    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run()
