import json
import requests
import pymongo

def initDatabase(): #function to initialize jukebox
    client = pymongo.MongoClient("mongodb+srv://kilchem182:sabreiitcnj123@sabreii-database-b6sjy.mongodb.net/test?retryWrites=true")
    db = client["database"]
    col = db["jukeBoxCollection"]
    post = {"jukeBox": [{"trackId": 604814341, "artistName": "Daler Mehndi" , "collectionName": "Tunak Tunak Tun", "trackName": "Tunak Tunak Tun", "artworkUrl100": "https://is4-ssl.mzstatic.com/image/thumb/Music/v4/d5/44/17/d54417af-f664-785a-f5cc-48875cdeb843/source/100x100bb.jpg", "vote": 0}]}
    _id = col.insert_one(post)
    return

def getID(): #function that returns jukebox ID
    client = pymongo.MongoClient("mongodb+srv://kilchem182:sabreiitcnj123@sabreii-database-b6sjy.mongodb.net/test?retryWrites=true")
    db = client["database"]
    cursor = db.jukeBoxCollection
    for doc in cursor.find():
        return(doc['_id'])

def dictToJSON(id, dict): #converts jukebox formated dictionary to JSON format
    client = pymongo.MongoClient("mongodb+srv://kilchem182:sabreiitcnj123@sabreii-database-b6sjy.mongodb.net/test?retryWrites=true")
    db = client["database"]
    col = db["jukeBoxCollection"]
    newVals = {"$set" : dict}
    col.update_one({'_id': id}, newVals)
    return

def JSONToDict(id):#converts JSON style data to a jukebox formatted dictionary
    client = pymongo.MongoClient("mongodb+srv://kilchem182:sabreiitcnj123@sabreii-database-b6sjy.mongodb.net/test?retryWrites=true")
    db = client["database"]
    col = db["jukeBoxCollection"]
    query = {'_id': id}
    result = col.find(query)
    for obj in result:
        return {"jukeBox" : obj["jukeBox"]}

def addSongToArray(songList, newSong): #adds song to a jukebox queue
    jukeBox = songList["jukeBox"]
    jukeBox.append(newSong)
    songList["jukeBox"] = jukeBox
    return songList

def getSongInfo(song, artist): #returns song info from apple API
    #wanted keys: trackId, artistName, albumName, songName, albumArt30,60,100, vote
    keys  = ['trackId', 'artistName', 'collectionName', 'trackName', 'artworkUrl100']
    song = song.replace(" ", "+")
    artist = artist.replace(" ", "+")

    response = requests.get('https://itunes.apple.com/search?term={}+{}&limit=1&media=music'.format(song, artist)).json()

    if response['resultCount'] == 0:
        return -1

    bigDict = response['results'][0]
    lilDict = {key:value for key, value in bigDict.items() if key in keys}

    lilDict['vote'] = 0

    return lilDict

def inSongList(songsList, trackIdNum): #function to tell if a song is already in a song list
    result = False

    for val in songsList:
        if(val['trackId'] == trackIdNum):
            result = True
        else:
            continue
    return result

def PrioritizeList(songList):
    jukeBox = songList["jukeBox"]
    orderedJukeBox = sorted(jukeBox, key=lambda k : k['vote'], reverse = True)
    songList["jukeBox"] = orderedJukeBox
    return songList

'''
initDatabase()
id = getID()
print(id)
songList = JSONToDict(id)
print(songList)
songList = addSongToArray(songList, {"Test" : 1})
print(songList)
dictToJSON(id, songList)
songList = JSONToDict(id)
print(songList)
songList = addSongToArray(songList, {"Test2" : 2})
print(songList)
dictToJSON(id, songList)
songList = JSONToDict(id)
print(songList)
songList = addSongToArray(songList, {"Test3" : 3})
print(songList)
dictToJSON(id, songList)
'''
