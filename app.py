from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from song_find import find_song_from_lyrics

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/find-song", methods=["POST"])
def find_song():
    try:
        lyrics = request.form.get("lyrics", "").strip()
        if not lyrics:
            return jsonify({"error": "Lyrics cannot be empty."}), 400

        print(f"Received lyrics: {lyrics}")

        title, artist = find_song_from_lyrics(lyrics)

        print(f"Found song: Title={title}, Artist={artist}")
        return jsonify({"title": title, "artist": artist})

    except ValueError as e:
        print(f"ValueError: {e}")
        return jsonify({"error": f"ValueError: {e}"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
