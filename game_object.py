from abc import ABC, abstractmethod


class GameObject(ABC):
    @abstractmethod
    def update(self, game_map=None):
        pass

    @abstractmethod
    def draw(self, screen, camera):
        pass