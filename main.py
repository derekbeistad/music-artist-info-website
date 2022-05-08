from flask import Flask, render_template, redirect, url_for
from forms import ArtistSearch, SongSearch
from flask_bootstrap import Bootstrap
import requests
import os

'''AudioDB Variables'''
adb_base_url = 'https://theaudiodb.com/api/v1/json/2/'
adb_artist_search_url = 'search.php?s='
adb_artist_data_url = 'artist.php?i='
adb_albums_url = 'album.php?i='
adb_videos_url = 'mvid.php?i='

'''Songsterr Variables'''
songsterr_artist_search_url = 'http://www.songsterr.com/a/ra/songs.json?pattern='
songsterr_tabs_song_url = 'http://www.songsterr.com/a/wa/song?id='
songsterr_tabs_artist_url = 'http://www.songsterr.com/a/wa/artist?id='

'''Functions'''


def search_by_artist_name(artist_name_str):
    '''Returns a dictionary of artist info when passed the artist name as a string'''
    adb_artist_response = requests.get(f"{adb_base_url}{adb_artist_search_url}{artist_name_str}")
    return adb_artist_response.json()['artists'][0]


def get_artist_id(adb_artist_info):
    '''Returns AudioDB Artist ID Number when passed the Artist info dictionary'''
    adb_artist_id = adb_artist_info['idArtist']
    return adb_artist_id


def get_albums_list(adb_artist_id):
    '''Returns list of Albums when passed artist ID'''
    adb_albums_response = requests.get(f"{adb_base_url}{adb_albums_url}{adb_artist_id}")
    return adb_albums_response.json()['album']


def get_videos_list(adb_artist_id):
    '''Returns List of Music videos when passed artist ID'''
    adb_videos_response = requests.get(f"{adb_base_url}{adb_videos_url}{adb_artist_id}")
    return adb_videos_response.json()['mvids']


def get_songsterr_artist_id(artist_name_str):
    '''Returns Songsterr Artist ID when passed artist name as a string'''
    response = requests.get(f"{songsterr_artist_search_url}{artist_name_str}")
    try:
        for n in range(0, 5):
            if (response.json()[n]['artist']['nameWithoutThePrefix'] == artist_name_str) or (
                    response.json()[n]['artist']['name'] == artist_name_str):
                return response.json()[n]['artist']['id']
            else:
                continue
        return None
    except IndexError:
        return None


def construct_artist_tabs_url(artist_songsterr_id):
    '''Returns a URL to the Songsterr page for all tabs for a certain artist when passed the artist ID'''
    if artist_songsterr_id == None:
        return None
    else:
        return f"{songsterr_tabs_artist_url}{artist_songsterr_id}"


'''App'''
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ArtistSearch()
    if form.validate_on_submit():
        artist_str = form.artist_name.data.title()
        return redirect(url_for('results', artist_name=artist_str))
    return render_template('index.html', form=form)


@app.route('/results/<artist_name>')
def results(artist_name):
    artist_info = search_by_artist_name(artist_name)
    artist_id = get_artist_id(artist_info)
    artist_albums = get_albums_list(artist_id)
    artist_videos = get_videos_list(artist_id)
    songsterr_id = get_songsterr_artist_id(artist_name)
    songsterr_url = construct_artist_tabs_url(songsterr_id)
    form = SongSearch()
    return render_template('results.html', form=form, artist_name=artist_name, artist_info=artist_info,
                           artist_albums=artist_albums, songsterr_url=songsterr_url)


if __name__ == '__main__':
    app.run(debug=True)
