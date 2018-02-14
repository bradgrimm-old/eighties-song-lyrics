# Quick hack script to pull down some lyrics and fix songs that could not be found from a list of songs.
import pandas as pd
from lyricwikia import LyricsNotFound

song_list = pd.read_excel('/Users/bgrimm/base/lyrics/Song List.xlsx')
lyrics = []
artist_found = []
for artist, song in zip(song_list['Artist'], song_list['Song']):
    try:
        song_lyrics = lyricwikia.get_lyrics(artist, song)
        print('Found song with {} words'.format(len(song_lyrics.split(' '))))
        lyrics.append(song_lyrics)
        artist_found.append(True)
    except (LyricsNotFound, AttributeError):
        print('Could not found: {} --- {}'.format(artist, song))
        lyrics.append(None)
        artist_found.append(False)

song_list['Lyrics'] = lyrics
song_list['Found'] = artist_found


not_found = song_list[song_list['Found'] == False]
for artist, song in zip(not_found['Artist'], not_found['Song']):
    print('{} --- {}'.format(artist, song))


def pick_one():
    f = song_list[song_list['Found'] == False].iloc[0]
    print(f)
    return f

def set_artist(artist):
    one_found['Artist'] = artist

def set_song(song):
    one_found['Song'] = song

def grab_from_url(url, timeout=None, linesep='\n'):
    response = _requests.get(url, timeout=timeout)
    soup = _BeautifulSoup(response.content, "html.parser")
    lyricboxes = soup.findAll('div', {'class': 'lyricbox'})
    if not lyricboxes:
        raise 'Still not found!'
    for lyricbox in lyricboxes:
        for br in lyricbox.findAll('br'):
            br.replace_with(linesep)
    lyrics = [lyricbox.text.strip() for lyricbox in lyricboxes]
    one_found['Lyrics'] = lyrics[0]
    one_found['Found'] = True
    song_list.at[one_found.name] = one_found
    print('Success')
    return pick_one()

def skip():
    one_found['Found'] = True
    song_list.at[one_found.name] = one_found
    return pick_one()

def check():
    lyrics = lyricwikia.get_lyrics(one_found['Artist'], one_found['Song'])
    one_found['Lyrics'] = lyrics
    one_found['Found'] = True
    song_list.at[one_found.name] = one_found
    print('Success')
    return pick_one()

def save_files(path):
    for artist, song, lyrics, found in zip(song_list['Artist'], song_list['Song'], song_list['Lyrics'], song_list['Found']):
        if not found or not lyrics:
            continue
        print('Saving song: {}'.format(song))
        if '/' in song:
            song = song.replace('/', '_')
        if isinstance(lyrics, list):
            lyrics = lyrics[0]
        file_path = '{}/{}.txt'.format(path, song)
        with open(file_path, 'w') as f:
            f.write(lyrics)

a = set_artist
s = set_song
c = check

one_found = pick_one()

