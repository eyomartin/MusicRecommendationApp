import requests

def search_deezer_preview(track, artist):
    
    query = f"{track} {artist}"
    url = f"https://api.deezer.com/search?q={query}"

    try:
        response = requests.get(url)
        data = response.json()

        if data['data']:
            song = data['data'][0]  # Take the top result
            return {
                'preview': song.get('preview'),
                'cover': song['album']['cover_medium'],
                'deezer_url': song['link']
            }
        else:
            return None
    except Exception as e:
        print(f"Deezer API error: {e}")
        return None
