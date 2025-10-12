from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')

# YouTube API key from environment variable
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

def search_youtube(query, max_results=24):
    """Search YouTube videos using API key"""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "key": "AIzaSyBqQfYpBhEJ9GQfJ2xX9e4Xns1fL5z6ck8",
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

@app.route('/', methods=["GET", "POST"])
def index():
    moods = ["Happy", "Sad", "Energetic", "Relaxed", "Romantic", "Motivational", "Calm", "Focused"]
    return render_template("index.html", moods=moods)

@app.route('/results', methods=["POST"])
def results():
    query = request.form.get("query")
    mood = request.form.get("mood")

    # Use query if provided, else fallback to mood
    search_term = query if query else mood

    videos = search_youtube(search_term)
    return render_template("result.html", videos=videos, mood=mood, query=search_term)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
