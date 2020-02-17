import pygame
import time
import json
from enum import Enum

class playerStatus(Enum):
    playing = 1
    paused = 2

playList = [4,1,5]
file = 'music/3337-aces-high-by-kevin-macleod.mp3'

songInfo1 = {
			"id": 1,
      		"length" : 201,
			"title" : "Funkorama",
			"fileName" : "3788-funkorama-by-kevin-macleod.mp3",
			"genre" : ["funk"]}

songInfo4 = {
			"id": 4,
      		"length" : 96,
			"title" : "Heartbreaking",
			"fileName" : "3863-heartbreaking-by-kevin-macleod.mp3",
			"genre" : ["contemporary", "piano"]}

songInfo5 = {
            "id": 5,
      		"length" : 286,
			"title" : "Inspired",
			"fileName" : "3918-inspired-by-kevin-macleod.mp3",
			"genre" : ["electronica","experimental"]}

class Iot_radio():
    status = ""
    skipNext = False

    def songIsPlaying(self):
        return pygame.mixer.music.get_busy()

    def playMusic(self,fileName):
        pygame.mixer.music.load(fileName)
        pygame.mixer.music.play()
        time.sleep(2)
        pygame.mixer.music.pause()
        # pygame.mixer.music.play()

    def getSongPath(self,id):
        path = "music/"
        # TODO Find filePath from JSON

        if id is 1:
            path = path + songInfo1["fileName"]
        elif id is 4:
            path = path + songInfo4["fileName"]
        elif id is 5:
            path = path + songInfo5["fileName"]



        return path

    def playNextSong(self):
        # TODO API GET request for playlist values
        # Get next song from playlist

        filePath = file
        if playList is not []:
            songId= playList[0]
            filePath = self.getSongPath(songId)

            # If song was from playlist, remove it from list
            playList.pop(0)
        else:
            # TODO Randomize song if list is empty
            #randomize song
            pass

        # Play song
        self.playMusic(filePath)
        pass

    def determineNextStatus(self):
        # TODO API GET request, find skipped value and playing/paused value
        self.skipNext = False
        nextStatus = playerStatus.playing

        if self.skipNext is True:
            self.playNextSong()
        else:
            if nextStatus is playerStatus.playing:
                if self.status is playerStatus.paused:
                    # TODO resume song playback
                    pass
                else:
                    if self.songIsPlaying():
                        # Resume playback
                        pass
                    else:
                        # Play next song
                        self.playNextSong()
            else:
                if self.status is playerStatus.playing:
                    # TODO Stop playback
                    pass
                else:
                    # Playback remains paused
                    pass


        self.status = nextStatus

    def uploadCurrentStatus(self):
        # TODO API POST request, save currentlyPlaying id & duration
        duration = pygame.mixer.music.get_pos()
        print(duration)

    def mainLoop(self):
        self.determineNextStatus()
        time.sleep(4)
        self.uploadCurrentStatus()

    def start(self):
        self.status = playerStatus.playing
        pygame.mixer.init()
        while True:
            self.mainLoop()

def main():
    app = Iot_radio()
    pygame.init()
    Iot_radio.start(app)

if __name__ == "__main__":
    main()