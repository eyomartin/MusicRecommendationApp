import requests
from bs4 import BeautifulSoup

# Define lyric-based emotion keyword banks
LYRIC_KEYWORDS = {
    'happy': [
        'happy', 'joyful', 'smiling', 'laughing', 'good vibes', 'cheerful', 'carefree', 'feeling good',
        'walking on sunshine', 'dancing', 'singing out loud', 'yay', 'ecstatic', 'overjoyed', 'bubbly',
        'bright days', 'warm heart', 'pure bliss', 'good day', 'celebrate life', 'heart full', 'grateful',
        'high spirits', 'sunshine', 'good times'
    ],
    'sad': [
        'sad', 'sorrow', 'tears', 'crying', 'breaking down', 'feeling blue', 'lost', 'alone', 'downhearted',
        'lonely nights', 'pain', 'heartache', 'grieving', 'miss you', 'broken dreams', 'heavy heart',
        'cry myself to sleep', 'fading away', 'hurt inside', 'numb', 'melancholy', 'aching', 'sleepless nights',
        'yearning', 'emptiness'
    ],
    'relaxed': [
        'relaxed', 'easy', 'slow dance', 'chill out', 'soothing', 'take it easy', 'calm sea', 'swaying',
        'serene', 'gentle', 'peaceful', 'soft breeze', 'smooth ride', 'cool vibes', 'laid back', 'quiet time',
        'easy living', 'deep breath', 'unwind', 'slow motion', 'still waters', 'tranquil', 'mellow', 'carefree moments',
        'lounge around'
    ],
    'angry': [
        'angry', 'rage', 'fuming', 'pissed off', 'fight', 'screaming', 'breaking free', 'no control',
        'fire inside', 'furious', 'mad', 'revenge', 'storming out', 'slam the door', 'burn it down',
        'tempest', 'grit teeth', 'lose it', 'exploding', 'red mist', 'cant take it', 'bitter', 'lashing out',
        'boiling point', 'chaos'
    ],
    'energetic': [
        'energy', 'hyped', 'let’s go', 'turn up', 'pumped', 'rush', 'nonstop', 'unstoppable', 'wild night',
        'move your body', 'electric', 'get up', 'fast lane', 'crazy vibe', 'headbanging', 'party all night',
        'feel the beat', 'heartbeat racing', 'take off', 'adrenaline', 'fast and loud', 'nonstop motion',
        'full throttle', 'power up', 'jump around'
    ],
    'neutral': [
        'neutral', 'in between', 'plain', 'gray skies', 'nothing much', 'everyday life', 'average day',
        'so-so', 'feeling fine', 'normal day', 'meh', 'whatever', 'no big deal', 'middle ground', 'same old',
        'routine', 'unremarkable', 'simple day', 'not bad', 'okay', 'moving along', 'basic', 'mundane',
        'unspectacular', 'plain sailing'
    ],
    'love': [
        'love you', 'in love', 'adore you', 'kiss you', 'forever yours', 'honey', 'sweetheart', 'darling',
        'baby', 'my boo', 'always together', 'only you', 'cuddle', 'hand in hand', 'soulmate', 'true love',
        'eternal flame', 'my heart', 'endless love', 'beautiful girl', 'crazy in love', 'love story',
        'sweet romance', 'loving you', 'sealed with a kiss'
    ],
    'heartbreak': [
        'broken heart', 'crying', 'goodbye', 'left me', 'hurts', 'tears', 'lost you', 'missing you', 'cant move on',
        'empty bed', 'gone forever', 'hurting inside', 'shattered dreams', 'goodbye letter', 'regret',
        'aching heart', 'tear drops', 'sad songs', 'forgotten', 'lonely world', 'cold nights', 'what we had',
        'walking away', 'painful memories', 'farewell'
    ],
    'nostalgia': [
        'remember', 'back then', 'good old days', 'once upon', 'memories', 'long ago', 'flashback', 'yesterday',
        'faded photo', 'childhood dreams', 'sweet memory', 'time machine', 'rewind', 'sentimental', 'growing up',
        'miss those times', 'looking back', 'past lives', 'olden times', 'worn out shoes', 'simpler times',
        'sweet yesterdays', 'memory lane', 'throwback', 'time flies'
    ],
    'motivational': [
        'rise up', 'fight back', 'believe in yourself', 'keep going', 'never give up', 'stronger', 'stand tall',
        'chase dreams', 'break free', 'overcome', 'win it all', 'unstoppable', 'push through', 'make it happen',
        'never surrender', 'aim high', 'reach for the stars', 'stay strong', 'beat the odds', 'fearless',
        'unstoppable force', 'dream big', 'success story', 'go for it', 'born to win'
    ],
    'loneliness': [
        'alone', 'lonely', 'nobody there', 'silence', 'empty room', 'missing someone', 'forgotten', 'in the dark',
        'cold bed', 'silent tears', 'solitude', 'deserted', 'no one calls', 'waiting alone', 'feeling empty',
        'abandoned', 'despair', 'solitary', 'heart aching', 'dark nights', 'alone again', 'longing',
        'lost connection', 'invisible', 'craving love'
    ],
    'hopeful': [
        'hope', 'brighter days', 'light ahead', 'sunrise', 'better tomorrow', 'new dawn', 'dream again',
        'healing', 'fresh start', 'uplift', 'never lose hope', 'believing', 'keep dreaming', 'new chapter',
        'rebirth', 'breakthrough', 'hopeful heart', 'ray of light', 'hold on', 'promise of tomorrow',
        'new horizons', 'better future', 'resilient', 'up and up', 'faith restored'
    ],
    'confident': [
        'confidence', 'own it', 'fearless', 'boss up', 'in control', 'on top', 'no fear', 'unstoppable',
        'victorious', 'conqueror', 'dare to win', 'alpha energy', 'stronger than ever', 'queen energy',
        'standing tall', 'power pose', 'shine bright', 'winning streak', 'number one', 'believe it',
        'take charge', 'own the moment', 'unbreakable', 'limitless', 'fear nothing'
    ],
    'playful': [
        'playful', 'messing around', 'having fun', 'joking', 'giggles', 'teasing', 'fun times', 'lighthearted',
        'jester', 'pranking', 'silly', 'wacky', 'laugh riot', 'mischievous', 'rolling on the floor',
        'goofing off', 'fun and games', 'cheeky', 'just for laughs', 'play around', 'clowning', 'good humor',
        'tickled pink', 'laughing out loud', 'wild and free'
    ],
    'car_trip': [
        'road trip', 'highway', 'cruising', 'driving fast', 'open road', 'wind in hair', 'long drive',
        'road ahead', 'map out', 'endless journey', 'driving all night', 'miles to go', 'pit stop',
        'car karaoke', 'fuel up', 'scenic route', 'city lights', 'riding along', 'cross country',
        'adventure awaits', 'no destination', 'passing by', 'freeway', 'engine roaring', 'journey on'
    ],
    'birthday': [
        'birthday', 'cake and candles', 'celebrate', 'another year', 'party time', 'blow out candles',
        'gift wrapped', 'balloons', 'cheers', 'birthday song', 'make a wish', 'growing older',
        'birthday bash', 'celebrating life', 'party hats', 'birthday toast', 'special day', 'birthday dance',
        'turning older', 'surrounded by friends', 'birthday vibes', 'joyful day', 'festivities',
        'birthday surprise', 'birthday memories'
    ],
    'workout': [
        'workout', 'gym life', 'beast mode', 'fitness goals', 'breaking sweat', 'pump it up', 'get ripped',
        'cardio session', 'deadlifts', 'burn calories', 'train hard', 'no pain no gain', 'push limits',
        'heavy lifting', 'sprint', 'work hard', 'train insane', 'be stronger', 'muscle up', 'hit the gym',
        'sweat session', 'personal best', 'power through', 'stay fit', 'grind never stops'
    ],
    'study_session': [
        'study', 'homework grind', 'library days', 'focus mode', 'hitting the books', 'knowledge hunt',
        'exam ready', 'all-nighter', 'brain food', 'mental marathon', 'note taking', 'study sesh',
        'coffee and books', 'quiet time', 'flashcards', 'study zone', 'deadline rush', 'bookworm life',
        'ace the test', 'focus up', 'mind sharp', 'exam stress', 'pencils ready', 'brain workout',
        'smart work'
    ],
    'beach_day': [
        'beach', 'sand between toes', 'ocean waves', 'surfs up', 'sunscreen time', 'seashells', 'sea breeze',
        'under the sun', 'sandy feet', 'beach ball', 'sunkissed', 'coastal chill', 'tanning', 'salty air',
        'summer splash', 'sunbathing', 'island vibes', 'beach bonfire', 'surfing', 'palm trees', 'coastal escape',
        'bikini season', 'endless summer', 'tide rolling', 'wave rider'
    ],
    'festival': [
        'festival', 'crowd surfing', 'music blast', 'festival grounds', 'open air vibe', 'party people',
        'all night long', 'colorful lights', 'live music', 'good vibrations', 'festival season', 'headliner',
        'dance like crazy', 'sing along', 'camping out', 'festival fever', 'beating drums', 'food trucks',
        'electric nights', 'glow sticks', 'music madness', 'jump around', 'mosh pit', 'wild crowd',
        'epic nights'
    ],
    'cooking': [
        'cooking', 'baking love', 'home kitchen', 'stir it up', 'recipe magic', 'spice it up', 'home cooked meals',
        'chopping veggies', 'flipping pancakes', 'secret sauce', 'simmering pot', 'sizzling', 'mealtime joy',
        'taste buds', 'family dinner', 'sunday roast', 'fresh ingredients', 'sweet treats', 'oven magic',
        'kitchen dance', 'chef hat', 'plating up', 'dinner is served', 'home chef', 'culinary vibes'
    ],
    'rainy_day': [
        'rain', 'storm outside', 'drizzle', 'wet roads', 'umbrella days', 'gray sky', 'cozy corner', 'stay indoors',
        'pitter-patter', 'rainy mood', 'hot cocoa', 'thunder', 'lightning strikes', 'soaked shoes', 'window watching',
        'melancholy rain', 'splashing puddles', 'cold rain', 'chilly vibes', 'blanket day', 'quiet rain',
        'gloomy day', 'rainy reflection', 'misty morning', 'under the clouds'
    ],
    'morning_routine': [
        'morning rise', 'sunrise view', 'early bird', 'coffee first', 'alarm clock', 'morning jog', 'fresh start',
        'waking up', 'stretching out', 'first light', 'breakfast vibes', 'toothbrush time', 'morning shower',
        'daylight breaking', 'new day', 'good morning', 'hustle start', 'motivated mornings', 'new beginnings',
        'wake up call', 'rise and shine', 'morning commute', 'to-do list', 'getting ready', 'grabbing coffee'
    ],
    'night_drive': [
        'midnight cruise', 'empty roads', 'streetlights', 'city asleep', 'late night drive', 'moonlight drive',
        'headlights', 'quiet streets', 'driving alone', 'starry sky', 'midnight thoughts', 'calm night',
        'after dark', 'road silence', 'slow cruise', 'late escape', 'cool breeze', 'night tunes',
        'under the stars', 'no traffic', 'neon lights', 'city skyline', 'cruising', 'lone drive', 'dark road'
    ]
}


GENIUS_SEARCH_URL = "https://genius.com/api/search/multi"

def get_lyrics(track, artist):
    """
    Try to fetch song lyrics from Genius using track and artist names.
    Returns the lyrics text if found, or None.
    """
    query = f"{track} {artist}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        # Search Genius
        response = requests.get(GENIUS_SEARCH_URL, params={'q': query}, headers=headers)
        data = response.json()

        # Find song hit
        for section in data['response']['sections']:
            if section['type'] == 'song':
                hits = section['hits']
                if hits:
                    song_url = hits[0]['result']['url']
                    break
        else:
            return None

        # Fetch song page
        song_page = requests.get(song_url, headers=headers)
        soup = BeautifulSoup(song_page.text, 'html.parser')

        # Genius puts lyrics in <div data-lyrics-container="true">
        lyrics_divs = soup.find_all('div', attrs={"data-lyrics-container": "true"})
        lyrics = "\n".join(div.get_text(separator="\n") for div in lyrics_divs)

        return lyrics.strip()

    except Exception as e:
        print(f"Error fetching lyrics: {e}")
        return None

def detect_emotion_from_lyrics(lyrics):
    """
    Scan the lyrics and return a detected emotion (love, heartbreak, etc.)
    Returns 'neutral' if nothing strong is found.
    """
    lowered_lyrics = lyrics.lower()

    emotion_scores = {emotion: 0 for emotion in LYRIC_KEYWORDS}

    for emotion, keywords in LYRIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lowered_lyrics:
                emotion_scores[emotion] += 1

    # Find the emotion with most matches
    best_emotion = max(emotion_scores, key=emotion_scores.get)

    if emotion_scores[best_emotion] > 0:
        return best_emotion
    else:
        return 'neutral'

if __name__ == "__main__":
    track = "Someone Like You"
    artist = "Adele"
    lyrics = get_lyrics(track, artist)

    if lyrics:
        emotion = detect_emotion_from_lyrics(lyrics)
        print(f"Detected emotion: {emotion}")
    else:
        print("Lyrics not found.")
