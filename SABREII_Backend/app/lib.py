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
