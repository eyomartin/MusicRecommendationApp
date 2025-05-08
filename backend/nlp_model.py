import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download NLTK resources (only needs to run once)
nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Define custom keyword banks for moods and scenarios
CUSTOM_KEYWORDS = {
    # Moods
    'love': ['love', 'in love', 'adore', 'crush', 'romantic', 'falling for', 'loved'],
    'heartbreak': ['heartbroken', 'broken heart', 'crying', 'tears', 'sad breakup', 'left me', 'goodbye','brokeup','broke up'],
    'nostalgia': ['remember', 'missing old days', 'good old times', 'memory', 'memories', 'long ago', 'past', 'good old days'],
    'motivational': ['you can do it', 'never give up', 'believe', 'rise up', 'keep going', 'chase dreams', 'overcome'],
    'loneliness': ['alone', 'lonely', 'nobody', 'empty', 'isolated', 'missing someone'],
    'angry': ['angry', 'mad', 'furious', 'pissed off'],
    'relaxed': ['calm', 'relaxed', 'chill', 'easygoing', 'laid back'],
    'energetic': ['hype', 'excited', 'energetic', 'party', 'pumped', 'hyped'],
    'sad': ['sad', 'sorrow', 'depressed', 'down', 'miserable', 'melancholy', 'blue'],
    'hopeful': ['hopeful', 'looking forward', 'bright future', 'optimistic', 'new beginnings',"I feel good"],
    'confident': ['confident', 'self-assured', 'fearless', 'bold', 'powerful'],
    'playful': ['playful', 'fun', 'mischievous', 'lighthearted', 'joking around', 'teasing'],


    # Scenarios
    'car_trip': ['car','car trip', 'road trip', 'long drive', 'driving', 'highway', 'cruise control', 'traveling by car',
                 'driving all night', 'on the road', 'freeway'],
    'birthday': ['birthday', 'birthday party', 'cake', 'candles', 'celebration', 'turning a year older'],
    'workout': ['gym', 'workout', 'exercise', 'lifting', 'running', 'fitness', 'sweat session'],
    'study_session': ['studying', 'study', 'library', 'homework', 'focus time', 'revision', 'exam prep'],
    'beach_day': ['beach', 'waves', 'ocean', 'sand', 'surf', 'sunbathing', 'coastal vibes'],
    'festival': ['festival', 'music festival', 'open air', 'crowd', 'live music', 'festival vibes'],
    'cooking': ['cooking', 'baking', 'kitchen', 'recipe', 'home cooked', 'meal prep', 'chef mode'],
    'rainy_day': ['rainy day', 'rain', 'storm', 'drizzle', 'cozy inside', 'thunderstorm', 'wet weather'],
    'morning_routine': ['morning','morning routine', 'waking up', 'rise and shine', 'fresh start', 'breakfast time','woke up'],
    'night_drive': ['night drive', 'midnight ride', 'late night cruising', 'empty streets', 'stars above'],

}


def analyze_mood(prompt_text):
    """
    this analyses the user input and returns a tuple (type, label):
    for exmaple: ("mood", "happy") or ("scenario", "car_trip")
    """
    lowered = prompt_text.lower()
    # list of some scenarios
    SCENARIOS = [
        'car_trip', 'birthday', 'workout', 'study_session', 'beach_day',
        'festival', 'cooking', 'rainy_day', 'morning_routine', 'night_drive',
        'house_party', 'coffee_shop_study', 'lazy_sunday', 'city_walk', 'sunset_viewing', 'hiking_adventure', 'snowy_day', 'after_work_relaxation', 'gaming_session', 'cleaning_day', 'airport_wait', 'romantic_dinner', 'picnic_in_the_park'
    ]

    # First check for strong custom keywords
    for label, keywords in CUSTOM_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lowered:
                if label in SCENARIOS:
                    return ('scenario', label)
                else:
                    return ('mood', label)

    #  no strong keywords then fallback to sentiment analysis (only for moods)
    sentiment = sia.polarity_scores(prompt_text)

    if sentiment['compound'] >= 0.5:
        return ('mood', 'happy')
    elif sentiment['compound'] <= -0.5:
        return ('mood', 'sad')
    else:
        return ('mood', 'neutral')
