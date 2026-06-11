import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = "audio/background.mp3"

    def play_background(self, volume=0.5):
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)