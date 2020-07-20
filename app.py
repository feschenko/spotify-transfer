from flask import Flask, request, redirect, render_template
from modules import Spotify, Vkontakte, VK_AUTH_URL


app = Flask(__name__)

spotify = Spotify()
vk = Vkontakte()


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html', host=request.url_root)


@app.route('/spotify', methods=['GET'])
def generate_spotify_token():
    return redirect(spotify.generate_url(request.base_url))


@app.route('/vkontakte', methods=['GET', 'POST'])
def generate_vk_token():
    error = False
    if request.method == 'POST':
        if request.form.get('link'):
            if vk.set_data(request.form.get('link')):
                return redirect('/playlist')
            else:
                error = 'Ссылка имеет неправильный формат'
        else:
            error = 'Вы не ввели ссылку'
    return render_template('vkontakte.html', auth=VK_AUTH_URL, error=error)


@app.route('/spotify/callback', methods=['GET'])
def get_spotify_token():
    if request.args.get('access_token'):
        spotify.token = request.args.get('access_token')
        return redirect('/vkontakte')
    return render_template('main.html', host=request.url_root)


@app.route('/playlist', methods=['GET'])
def playlist():
    url = spotify.generate_playlist()
    spotify.add_tracks(spotify.search_tracks(vk.get_all_tracks()))
    return render_template('playlist.html', playlist=url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)

