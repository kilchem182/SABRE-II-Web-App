import json
import requests

def dictToJSON(file, dict): #json.dumps() puts dict in to json, json.loads() puts json in to dict
    with open(file, 'w') as file:
        json.dump(dict, file)

def JSONToDict(file):#converts JSON style data to a dictionary
    with open(file) as file:
        jsonString = file.read()
        jsonInfo = json.loads(jsonString)
        return jsonInfo

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
songList = [{'Test1': 1, 'Test2': 2}]
newSong = {'Test3': 3, 'Test4': 4}
print(addSongToArray(songList, newSong))

songs = {
            0: 'Party in the U.S.A',
            1: 'Tunak Tunak Tun',
            2: 'Gangnam Style'
}
addSongToQ(songs)
val = loadJSON()
print(val[3])
addSongToQ(val)
'''
