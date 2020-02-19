import pygame
import time
import json
import requests
import random
import os
from enum import Enum

class playerStatus(Enum):
    playing = 1
    paused = 2



##Start of app class
class Iot_radio():
    status = ""
    skipNext = False
    apiDomain = ""
    currentlyPlayingId = 2

    def songIsPlaying(self):
        return pygame.mixer.music.get_busy()

    def pausePlayback(self):
        pygame.mixer.music.pause()

    def resumePlayback(self):
        pygame.mixer.music.unpause()

    def stopPlayback(self):
        pygame.mixer.music.stop()

    def playMusic(self,fileName):
        pygame.mixer.music.load(fileName)
        pygame.mixer.music.play()

    def getSongPath(self,id):
        path = "music/"
        with open('db.json') as json_file:
            data = json.load(json_file)
            songs = data["musicDB"]
            for song in songs:
                if id is song["id"]:
                    path = path + song["fileName"]
                    #print("Found")
        return path

    def requestNextSong(self):
        playlistAPI = self.apiDomain + '/playlist/'
        r = requests.get(playlistAPI, data="")
        data = r.json()
        nextSong = data['Item']['songList']['L'][0]['S']
        print(nextSong)
        return nextSong

    def removeFromPlaylist(self):
        playlistAPI = self.apiDomain + '/playlist/'
        r = requests.delete(playlistAPI, data="")

    def playNextSong(self):

        # TODO API GET request for playlist values
        # Get next song from playlist

        nextSong = self.requestNextSong()
        filePath = ""
        if nextSong:
            filePath = self.getSongPath(int(nextSong))
            self.currentlyPlayingId = nextSong

            # If song was from playlist, remove it from list
            # TODO API DELETE request, remove from playlist
            self.removeFromPlaylist()
        else:
            nextSong = random.randint(1, 82)
            filePath = self.getSongPath(nextSong)
            self.currentlyPlayingId = nextSong
            print("Randomized song", nextSong)

        self.playMusic(filePath)

    def determineNextStatus(self):
        # TODO API GET request, find skipped value and playing/paused value
        self.skipNext = False
        nextStatus = playerStatus.playing

        if self.skipNext is True:
            # TODO API PUT REQUEST, set skipped value to false
            self.playNextSong()

        else:
            if nextStatus is playerStatus.playing:
                if self.status is playerStatus.paused:
                    self.resumePlayback()
                else:
                    if self.songIsPlaying():
                        # Resume playback
                        pass
                    else:
                        # Play next song
                        self.playNextSong()
            else:
                if self.status is playerStatus.playing:
                    self.pausePlayback()
                else:
                    # Playback remains paused
                    pass

        self.status = nextStatus

    def uploadCurrentStatus(self):
        currentlyPlayingIdAPI = self.apiDomain + '/currentlyplaying/' + str(self.currentlyPlayingId)
        r = requests.put(currentlyPlayingIdAPI, data="")

        duration = pygame.mixer.music.get_pos()
        durationUpdateAPI = self.apiDomain + '/durationupdate/' + str(duration)
        r = requests.put(durationUpdateAPI, data="")
        print(duration)

    def mainLoop(self):
        self.determineNextStatus()
        time.sleep(4)
        self.uploadCurrentStatus()

    def start(self):
        self.status = playerStatus.playing
        self.apiDomain = os.getenv('IOTRADIO_API_DOMAIN')
        pygame.mixer.init()
        while True:
            self.mainLoop()
## End of app class

def main():
    app = Iot_radio()
    pygame.init()
    Iot_radio.start(app)

if __name__ == "__main__":
    main()