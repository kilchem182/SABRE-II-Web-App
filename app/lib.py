import json
import requests
import json

def dictToJSON(dict): #json.dumps() puts dict in to json, json.loads() puts json in to dict
    with open('room', 'w') as file:
        json.dump(dict, file)

def JSONToDict():
    with open('room') as file:
        jsonString = file.read()
        jsonInfo = json.loads(jsonString)
        return jsonInfo

def inJSON():
    length = len(jsonInfo)
    jsonInfo[length] = input #length

def addSongToArray(songList, newSong):
    songList.append(newSong)
    return songList

def getSongInfo(song, artist):
    #wanted keys: trackId, artistName, albumName, songName, albumArt30,60,100, vote
    keys  = ['trackId', 'artistName', 'collectionName', 'trackName', 'artworkUrl30', 'artworkUrl60', 'artworkUrl100']
    song = song.replace(" ", "+")
    artist = artist.replace(" ", "+")

    check = requests.get('https://itunes.apple.com/search?term={}+{}&limit=1&media=music'.format(song, artist))
    if not check.ok:
        return -1

    response = requests.get('https://itunes.apple.com/search?term={}+{}&limit=1&media=music'.format(song, artist)).json()

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
    return songList.sort(key=lambda k : k['votes'], reverse = True)


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
