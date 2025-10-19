from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')

# YouTube API Key (replace with your own or keep as env variable)
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY") or "AIzaSyBqQfYpBhEJ9GQfJ2xX9e4Xns1fL5z6ck8"


def search_youtube(query, max_results=60):
    """Search YouTube videos using the Data API v3"""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "key": YOUTUBE_API_KEY,
        "maxResults": max_results,
        "order": "relevance"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        videos = []
        for item in data.get("items", []):
            video_id = item.get("id", {}).get("videoId")
            snippet = item.get("snippet")
            if video_id and snippet:
                videos.append({
                    "title": snippet.get("title"),
                    "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url"),
                    "videoId": video_id
                })
        return videos
    else:
        print("YouTube API Error:", response.status_code, response.text)
        return []


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/results', methods=["GET", "POST"])
def results():
    # Handle both POST (from index) and GET (from results page search)
    query = request.form.get("query") if request.method == "POST" else request.args.get("query")
    if not query:
        return render_template("result.html", videos=[], query="")

    videos = search_youtube(query)
    return render_template("result.html", videos=videos, query=query)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

