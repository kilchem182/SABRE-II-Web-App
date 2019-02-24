from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, SongForm
#from app.lib import JSONToDict
#import json


@app.route('/')
@app.route('/index')
def index():
    ID = 604814341
    track = 'Tunak Tunak Tun'
    artist = 'Daler Mehndi'
    album = 'Tunak Tunak Tun'
    url =  'https://is4-ssl.mzstatic.com/image/thumb/Music/v4/d5/44/17/d54417af-f664-785a-f5cc-48875cdeb843/source/100x100bb.jpg'
    numVotes = 0
    songlist = [{
            'trackId': ID,
            'trackName': track,
            'artistName': artist,
            'collectionName': album,
            'artworkUrl100' : url,
            'votes': numVotes
        }]
    return render_template('index.html', title='Home', posts=songlist)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/addSongToQ', methods=['GET', 'POST'])
def addSongToQ():
    form = SongForm()
    if form.validate_on_submit():
        flash('Song is {}, Artist is {}'.format(
            form.song.data, form.artist.data))
        return redirect("/index")
    return render_template('addSongToQ.html', title='Enter A Song', form=form)
