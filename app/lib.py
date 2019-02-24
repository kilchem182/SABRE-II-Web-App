import json
import requests
import pymongo

def initDatabase():
    client = pymongo.MongoClient("mongodb://heroku_n7kdzn44:f2he7ovbbjm9fiffgu6fn23tfs@ds349455.mlab.com:49455/heroku_n7kdzn44")
    db = client["database"]
    col = db["jukeBoxCollection"]
    post = {"jukeBox": [{"trackId": 290884853, "artistName": "X JAPAN", "collectionName": "Blue Blood", "trackName": "X", "artworkUrl100": "https://is4-ssl.mzstatic.com/image/thumb/Music/v4/a7/5c/81/a75c818e-9f2b-0571-63f0-ec7a3fa7aa86/source/100x100bb.jpg", "vote": 0}]}
    _id = col.insert_one(post)
    return

def getID():
    client = pymongo.MongoClient("mongodb://heroku_n7kdzn44:f2he7ovbbjm9fiffgu6fn23tfs@ds349455.mlab.com:49455/heroku_n7kdzn44")
    db = client["database"]
    cursor = db.jukeBoxCollection
    for doc in cursor.find():
        return(doc['_id'])

def dictToJSON(id, dict): #json.dumps() puts dict in to json, json.loads() puts json in to dict
    client = pymongo.MongoClient("mongodb://heroku_n7kdzn44:f2he7ovbbjm9fiffgu6fn23tfs@ds349455.mlab.com:49455/heroku_n7kdzn44")
    db = client["database"]
    col = db["jukeBoxCollection"]
    newVals = {"$set" : dict}
    col.update_one({'_id': id}, newVals)
    return

def JSONToDict(id):#converts JSON style data to a dictionary
    client = pymongo.MongoClient("mongodb://heroku_n7kdzn44:f2he7ovbbjm9fiffgu6fn23tfs@ds349455.mlab.com:49455/heroku_n7kdzn44")
    db = client["database"]
    col = db["jukeBoxCollection"]
    query = {'_id': id}
    result = col.find(query)
    for obj in result:
        return {"jukeBox" : obj["jukeBox"]}

def addSongToArray(songList, newSong):
    jukeBox = songList["jukeBox"]
    jukeBox.append(newSong)
    songList["jukeBox"] = jukeBox
    return songList

def getSongInfo(song, artist):
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
