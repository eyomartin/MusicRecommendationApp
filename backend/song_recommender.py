import pandas as pd
from lyrics_analyzer import get_lyrics, detect_emotion_from_lyrics

# Load and clean the dataset
df = pd.read_csv('dataset/spotify_songs.csv')

print("Actual column names from CSV:")
print(df.columns)

# genres completely excluded based on preferences
EXCLUDED_GENRES = [
    "cantopop", "children", "comedy", "detroit-techno",
    "indian", "iranian", "j-pop", "j-rock", "kids",
    "mandopop", "ska", "turkish"
]

##  cleaning
df = df.dropna(subset=['track_name', 'artists', 'valence', 'energy', 'tempo', 'track_genre'])
df = df.drop_duplicates(subset=['track_name', 'artists'])
df = df[df['tempo'] < 250]
df = df[~df['track_genre'].str.lower().isin(EXCLUDED_GENRES)]  # exclude some of the genres that are not ideal

print("Dataset loaded successfully.")
print("Number of songs after cleaning:", len(df))


TITLE_KEYWORDS = {
    'love': ["love", "fall in love", "crazy love", "loving you", "forever love", "adore", "ily", "i love you", "i love her"],
    'heartbreak': ["broken heart", "heartbreak", "tears", "lost love", "goodbye", "crying"],
    'nostalgia': ["memory", "memories", "yesterday", "old days", "remember"],
    'loneliness': ["alone", "lonely", "without you", "nobody", "empty"],
    'motivational': ["rise up", "dream big", "fight on", "never give up", "keep going"],
    'sad': ["sad", "tears", "sorrow", "miserable", "melancholy", "crying", "depression", "leave me alone", "unhappy"],
    'hopeful': ["hope", "bright future", "optimistic", "new beginning", "hopeful heart"],
    'confident': ["confident", "self-assured", "fearless", "bold", "unstoppable", "stronger"],
    'playful': ["playful", "fun", "mischievous", "lighthearted", "teasing", "game"],
    'happy': ["happy", "joy", "sunshine", "smile"],
    'energetic': ["party", "dance", "hype", "excited"],
    'relaxed': ["chill", "relax", "breeze", "easy"],
    'angry': ["rage", "angry", "fight", "battle"],
    'car_trip': ["drive", "ride", "road", "highway", "freeway", "wheels", "journey", "trip", "cruise", "travel",
                 "miles", "destination", "motion", "escape", "car", "traffic", "route", "gasoline", "speed",
                 "horizon", "on the road", "hit the road", "drive all night", "highway dreams", "open road",
                 "cruise control", "fast lane", "lost highway", "long drive home", "endless highway", "riding shotgun",
                 "road trip anthem", "adventure", "driving", "pedal"],
    'birthday': ["birthday", "cake", "candles", "celebrate", "birthday party", "birthday song", "happy birthday", "birthday hat",],
    'workout': ["workout", "gym", "lift", "run", "sweat", "fitness", "exercise", "training", "Phonk","phonk", "rage phonk", "adrenaline", "phonk"],
    'study_session': ["study", "library", "focus", "homework", "exam", "revision", "learning"],
    'beach_day': ["beach", "waves", "ocean", "sand", "surf", "sunbathing", "seaside"],
    'festival': ["festival", "music festival", "open air", "live concert", "crowd", "festival vibes", "firework", "fireworks"],
    'cooking': ["cooking", "baking", "kitchen", "recipe", "homemade", "meal prep"],
    'rainy_day': ["rain", "storm", "rainy day", "thunder", "drizzle", "cozy inside"],
    'morning_routine': ["morning", "wake up", "fresh start", "breakfast", "new day", "sunrise"],
    'night_drive': ["night drive", "midnight ride", "empty streets", "stars above", "cruise at night"]
}

ALLOWED_GENRES_FOR_TITLE_MATCH = [
    'acoustic', 'country', 'heavy-metal', 'hip-hop', 'jazz', 'pop', 'r-n-b', 'rock-n-roll'
]

PROFILES = {
    'happy':        {'valence': 0.7, 'energy': 0.6, 'danceability': 0.7, 'loudness': -6.5,  'liveness': 0.2},
    'sad':          {'valence': 0.25, 'energy': 0.3, 'danceability': 0.4, 'loudness': -12.0, 'liveness': 0.15},
    'relaxed':      {'valence': 0.6, 'energy': 0.2, 'danceability': 0.5, 'loudness': -9.0,  'liveness': 0.25},
    'angry':        {'valence': 0.2, 'energy': 0.8, 'danceability': 0.6, 'loudness': -5.0,  'liveness': 0.3},
    'energetic':    {'valence': 0.8, 'energy': 0.9, 'danceability': 0.8, 'loudness': -4.0,  'liveness': 0.4},
    'neutral':      {'valence': 0.5, 'energy': 0.5, 'danceability': 0.5, 'loudness': -8.0,  'liveness': 0.2},
    'love':         {'valence': 0.8, 'energy': 0.4, 'danceability': 0.6, 'loudness': -7.0,  'liveness': 0.2},
    'heartbreak':   {'valence': 0.2, 'energy': 0.3, 'danceability': 0.3, 'loudness': -13.0, 'liveness': 0.15},
    'nostalgia':    {'valence': 0.5, 'energy': 0.4, 'danceability': 0.5, 'loudness': -10.0, 'liveness': 0.25},
    'motivational': {'valence': 0.7, 'energy': 0.7, 'danceability': 0.75,'loudness': -5.0,  'liveness': 0.3},
    'loneliness':   {'valence': 0.3, 'energy': 0.2, 'danceability': 0.35,'loudness': -14.0, 'liveness': 0.2},
    'hopeful':      {'valence': 0.65,'energy': 0.5, 'danceability': 0.65,'loudness': -7.0,  'liveness': 0.2},
    'confident':    {'valence': 0.75,'energy': 0.7, 'danceability': 0.7, 'loudness': -4.5,  'liveness': 0.25},
    'playful':      {'valence': 0.8, 'energy': 0.7, 'danceability': 0.8, 'loudness': -5.5,  'liveness': 0.3},
    'car_trip':     {'valence': 0.7, 'energy': 0.6, 'danceability': 0.7, 'loudness': -6.5,  'liveness': 0.25},
    'birthday':     {'valence': 0.85,'energy': 0.7, 'danceability': 0.8, 'loudness': -5.0,  'liveness': 0.3},
    'workout':      {'valence': 0.7, 'energy': 0.85,'danceability': 0.8, 'loudness': -3.0,  'liveness': 0.35},
    'study_session':{'valence': 0.5, 'energy': 0.4, 'danceability': 0.4, 'loudness': -13.0, 'liveness': 0.15},
    'beach_day':    {'valence': 0.8, 'energy': 0.6, 'danceability': 0.7, 'loudness': -6.0,  'liveness': 0.4},
    'festival':     {'valence': 0.9, 'energy': 0.9, 'danceability': 0.9, 'loudness': -2.5,  'liveness': 0.5},
    'cooking':      {'valence': 0.6, 'energy': 0.4, 'danceability': 0.5, 'loudness': -10.0, 'liveness': 0.2},
    'rainy_day':    {'valence': 0.4, 'energy': 0.3, 'danceability': 0.4, 'loudness': -12.5, 'liveness': 0.15},
    'morning_routine': {'valence': 0.7,'energy': 0.5,'danceability': 0.65,'loudness': -8.0,'liveness': 0.25},
    'night_drive':  {'valence': 0.5, 'energy': 0.4, 'danceability': 0.5, 'loudness': -9.0,  'liveness': 0.2}
}

def recommend_songs_by_mood(mood, limit=10, user_prompt=""):

    profile = PROFILES.get(mood, PROFILES['neutral'])
    user_prompt_lower = user_prompt.lower()

    
    df['match_score'] = df.apply(lambda row:
            1 - (
                    abs(profile['valence'] - row['valence']) * 0.25 +
                    abs(profile['energy'] - row['energy']) * 0.25 +
                    abs(profile['danceability'] - row['danceability']) * 0.2 +
                    abs(profile['loudness'] - row['loudness']) * 0.15 +
                    abs(profile['liveness'] - row['liveness']) * 0.15
            ), axis=1)

    
    title_matches = []
    picked_song_ids = set()

    title_keywords = TITLE_KEYWORDS.get(mood, [])
    all_possible_titles = []

    for _, row in df.iterrows():
        track = row['track_name']
        artist = row['artists']
        genre = row['track_genre'].lower()
        score = row['match_score']
        track_lower = track.lower()

        if genre not in ALLOWED_GENRES_FOR_TITLE_MATCH:
            continue
        if score < 0.68:
            continue
        for keyword in title_keywords:
            if keyword in track_lower:
                all_possible_titles.append({
                    'track': track,
                    'artist': artist,
                    'genre': genre,
                    'score': round((score + 0.15) * 100, 1),
                    'badge': '🎯 Title Match'
                })
                picked_song_ids.add((track, artist))
                break

    
    all_possible_titles = sorted(all_possible_titles, key=lambda x: x['score'], reverse=True)
    title_matches = all_possible_titles[:4]

    
    recommendations = []

    sorted_candidates = df.sort_values(by='match_score', ascending=False)

    for _, row in sorted_candidates.iterrows():
        track = row['track_name']
        artist = row['artists']
        genre = row['track_genre'].lower()
        score = row['match_score']

        if (track, artist) in picked_song_ids:
            continue  # Skip title-matched songs

        
        lyrics = get_lyrics(track, artist)

        if lyrics:
            detected_lyric_emotion = detect_emotion_from_lyrics(lyrics)
            if detected_lyric_emotion == mood:
                score += 0.1  # 10% boost for matching lyrics mood

        recommendations.append({
            'track': track,
            'artist': artist,
            'genre': genre,
            'score': round(score * 100, 1),
            'badge': '🎵 Audio+Lyrics Match'
        })

        if len(recommendations) >= (limit - len(title_matches)):
            break

    
    final_list = title_matches + recommendations
    final_list = sorted(final_list, key=lambda x: x['score'], reverse=True)

    
    final_simplified = []
    for song in final_list[:limit]:
        final_simplified.append({
            'track': song['track'],
            'artist': song['artist'],
            'score': song['score'],
            'badge': song.get('badge', '')
        })

    return final_simplified
