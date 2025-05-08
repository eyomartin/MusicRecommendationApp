from flask import Flask, render_template, request
from nlp_model import analyze_mood
from song_recommender import recommend_songs_by_mood
from deezer_api import search_deezer_preview

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

@app.route('/', methods=['GET', 'POST'])
def home():
    mood_input = None
    detected_label = None
    label_type = None
    songs = []

    if request.method == 'POST':
        mood_input = request.form['mood']
        print(f"User said: {mood_input}")

        label_type, detected_label = analyze_mood(mood_input)
        print(f"Detected {label_type}: {detected_label}")

        raw_songs = recommend_songs_by_mood(detected_label, user_prompt=mood_input)
        songs = []

        for song in raw_songs:
            deezer_data = search_deezer_preview(song['track'], song['artist'])

            song_info = {
                'track': song['track'],
                'artist': song['artist'],
                'score': song['score'],
                'preview': deezer_data['preview'] if deezer_data else None,
                'cover': deezer_data['cover'] if deezer_data else None,
                'deezer_url': deezer_data['deezer_url'] if deezer_data else '#'
            }

            songs.append(song_info)

        print(f"Top song: {songs[0]['track']} by {songs[0]['artist']}")

    return render_template('index.html', mood=mood_input, label_type=label_type, emotion=detected_label, songs=songs)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run(debug=True)
