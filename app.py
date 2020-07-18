from flask import Flask, request, redirect, render_template
from modules import Spotify, Vkontakte


app = Flask(__name__)

spotify = Spotify()
vk = Vkontakte()


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/spotify', methods=['GET'])
def generate_spotify_token():
    return redirect(spotify.generate_url())


@app.route('/vkontakte', methods=['GET'])
def generate_vk_token():
    return render_template('vkontakte.html', auth=vk.generate_url())


@app.route('/spotify/callback', methods=['GET'])
def get_spotify_token():
    if request.args.get('access_token'):
        spotify.token = request.args.get('access_token')
        return redirect('/vkontakte')
    return render_template('main.html')


@app.route('/vkontakte/callback', methods=['GET', 'POST'])
def get_vk_token():
    if request.method == 'POST':
        vk.access_token, vk.uid, = request.form.get('access_token'), request.form.get('uid')
    return redirect('/playlist')


@app.route('/playlist', methods=['GET'])
def playlist():
    url = spotify.generate_playlist()
    spotify.add_tracks(spotify.search_tracks(vk.get_tracks()))
    return render_template('playlist.html', playlist=url)


if __name__ == '__main__':
    app.run(host='localhost', port=5555)
    app.debug = True

