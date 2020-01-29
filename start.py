import pygame
import time
from enum import Enum

class playerStatus(Enum):
    playing = 1
    paused = 2


file = 'music/3337-aces-high-by-kevin-macleod.mp3'



status = playerStatus.playing

def songIsPlaying():
    return pygame.mixer.music.get_busy()

def playMusic(fileName):
    pygame.mixer.music.load(fileName)
    pygame.mixer.music.play()
    time.sleep(2)
    pygame.mixer.music.pause()
    #pygame.mixer.music.play()

def playNextSong():
    #Get next song from playlist
    #If song was from playlist, remove it from list
    #If playlist is empty, randomize next song
    #Play song
    playMusic(file)
    pass

def determineNextStatus(currentStatus=status):
    #Hae rajapinnasta tilat
    skipNext = False
    nextStatus = playerStatus.playing
    if skipNext is True:
        pass
    else:
        if nextStatus is playerStatus.playing:
            if currentStatus is playerStatus.paused:
                pass
            else:
                if songIsPlaying():
                    print("soi")
                else:
                    playNextSong()
        else:
            pass

    status = nextStatus

def uploadCurrentStatus():
    #Tallenna currentlyPlaying id ja duration
    duration = pygame.mixer.music.get_pos()
    print(duration)

def main():
    pygame.init()
    pygame.mixer.init()
    laskuri = 0
    while True:
        mainLoop()

def mainLoop():
    determineNextStatus()
    time.sleep(4)
    uploadCurrentStatus()


if __name__ == "__main__":
	main()