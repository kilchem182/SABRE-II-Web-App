from flask import render_template, flash, redirect, request, url_for
from app import app
import json
from app.forms import SongForm
from app.lib import getSongInfo, JSONToDict, dictToJSON, addSongToArray, PrioritizeList, getID, initDatabase


@app.route('/')
@app.route('/index')
def index(): #python portion for main index page. Initializes databse and applys that as defaut jukebox
    if getID() == None:
        initDatabase()
    songList = JSONToDict(getID())
    songList['jukeBox'][0]['vote'] = 1000000
    dictToJSON(getID(), songList)
    return render_template('index.html', title='Home', songs=songList['jukeBox'])

@app.route('/addSongToQ', methods=['GET', 'POST'])
def addSongToQ(): #python portion for ading a song to the jukebox
    form = SongForm()
    if form.validate_on_submit():
        songList = JSONToDict(getID())
        newSong = getSongInfo(form.song.data, form.artist.data)
        if newSong == -1:
            flash('ERROR: Song could not be found - Try Again')
            return redirect("/addSongToQ")
        songList = addSongToArray(songList, newSong)
        songList = PrioritizeList(songList)
        dictToJSON(getID(), songList)
        return redirect("/index")
    return render_template('addSongToQ.html', title='Enter A Song', form=form)

@app.route('/updateRemoteJukeBox', methods=['GET', 'POST'])
def updateRemoteJukebox(): #updates jukebox, triggered when user adds or upvotes songs
    if request.method == 'POST':
        if getID() == None:
            initDatabase()
        songList = JSONToDict(getID())
        if request.get_json() != {"jukeBox" : []}:
            newSong = request.get_json()
            for song in newSong["jukeBox"]:
                songList = JSONToDict(getID())
                songList = addSongToArray(songList, song)
                songList = PrioritizeList(songList)
                dictToJSON(getID(), songList)
        return json.dumps(songList)
    return None

@app.route('/upvote', methods=['GET', 'POST'])
def upvote(): #updates values based on user inputeed upvote
    trackID = request.args["trackId"]
    songList = JSONToDict(getID())
    for song in songList['jukeBox']:
        if(str(song["trackId"]) == trackID):
            song["vote"] = song["vote"] + 1

    songList = PrioritizeList(songList)
    updatedVotes = songList
    updatedVotes = dictToJSON(getID(), updatedVotes)

    return redirect(url_for("index"))
