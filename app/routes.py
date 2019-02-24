from flask import render_template, flash, redirect, request
from app import app
import json
from app.forms import SongForm
from app.lib import getSongInfo, JSONToDict, dictToJSON, addSongToArray, PrioritizeList


@app.route('/')
@app.route('/index')
def index():
    ID = 604814341
    track = 'Tunak Tunak Tun'
    artist = 'Daler Mehndi'
    album = 'Tunak Tunak Tun'
    url =  'https://is4-ssl.mzstatic.com/image/thumb/Music/v4/d5/44/17/d54417af-f664-785a-f5cc-48875cdeb843/source/100x100bb.jpg'
    numVotes = 0
    # songlist = [{
    #         'trackId': ID,
    #         'trackName': track,
    #         'artistName': artist,
    #         'collectionName': album,
    #         'artworkUrl100' : url,
    #         'vote': numVotes
    #     }]

    songlist = JSONToDict('test.json') #MAKE THIS ACCESS THE DATABASE

    return render_template('index.html', title='Home', songs=songlist['jukeBox'])

@app.route('/addSongToQ', methods=['GET', 'POST'])
def addSongToQ():
    form = SongForm()
    if form.validate_on_submit():
        songList = JSONToDict('test.json')
        newSong = getSongInfo(form.song.data, form.artist.data)
        if newSong == -1:
            flash('Song could not be found')
            return redirect("/index")
        songList = addSongToArray(songList, newSong)
        songList = PrioritizeList(songList)
        dictToJSON('test.json', songList)
        return redirect("/index")
    return render_template('addSongToQ.html', title='Enter A Song', form=form)

@app.route('/updateRemoteJukeBox', methods=['GET', 'POST'])
def updateRemoteJukebox():
    if request.method == 'POST':
        songList = JSONToDict('test.json')
        if request.get_json() != {}:
            newSong = request.get_json()
            songList = addSongToArray(songList, newSong)
            songList = PrioritizeList(songList)
            dictToJSON('test.json', songList)

        return json.dumps(songList)

    return None
