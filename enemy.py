import pygame
import random
from PIL import Image

from game_object import GameObject


class Enemy(GameObject):
    def __init__(self, x, y, gif_path):
        self.frames = self.load_gif(gif_path)

        self.frame_index = 0
        self.animation_speed = 8
        self.counter = 0

        self.hp = 1

        self.rect = self.frames[0].get_rect(center=(x, y))

    def load_gif(self, path):
        frames = []

        try:
            gif = Image.open(path)

            for i in range(gif.n_frames):
                gif.seek(i)
                frame = gif.convert("RGBA")

                image = pygame.image.fromstring(
                    frame.tobytes(),
                    frame.size,
                    "RGBA"
                ).convert_alpha()

                image = pygame.transform.scale(
                    image,
                    (64, 64)
                )

                frames.append(image)

        except:
            print("Gambar enemy tidak ditemukan:", path)

            fallback = pygame.Surface(
                (64, 64),
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                fallback,
                (180, 50, 50),
                pygame.Rect(0, 0, 64, 64)
            )

            frames.append(fallback)

        return frames

    def take_damage(self, damage=1):
        self.hp -= damage

        if self.hp <= 0:
            return True

        return False

    def update(self, game_map=None):
        self.counter += 1

        if self.counter >= self.animation_speed:
            self.counter = 0
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

    def draw(self, screen, camera):
        image = self.frames[self.frame_index]

        size = int(64 * camera.zoom)

        scaled = pygame.transform.scale(
            image,
            (size, size)
        )

        screen_x = (self.rect.x - camera.x) * camera.zoom
        screen_y = (self.rect.y - camera.y) * camera.zoom

        screen.blit(scaled, (screen_x, screen_y))


def spawn_enemy_around_plants(crop_tiles, tile_size, gif_path):
    if not crop_tiles:
        return None

    min_x = min(tile[0] for tile in crop_tiles)
    max_x = max(tile[0] for tile in crop_tiles)
    min_y = min(tile[1] for tile in crop_tiles)
    max_y = max(tile[1] for tile in crop_tiles)

    sisi = random.choice([
        "atas",
        "bawah",
        "kiri",
        "kanan"
    ])

    jarak = 2

    if sisi == "atas":
        tile_x = random.randint(min_x, max_x)
        tile_y = min_y - jarak

    elif sisi == "bawah":
        tile_x = random.randint(min_x, max_x)
        tile_y = max_y + jarak

    elif sisi == "kiri":
        tile_x = min_x - jarak
        tile_y = random.randint(min_y, max_y)

    else:
        tile_x = max_x + jarak
        tile_y = random.randint(min_y, max_y)

    world_x = tile_x * tile_size + tile_size // 2
    world_y = tile_y * tile_size + tile_size // 2

    return Enemy(
        world_x,
        world_y,
        gif_path
    )