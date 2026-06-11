import pygame
import random
from PIL import Image
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, x, y, produce_time_ms, min_x, max_x, min_y, max_y,
                 gif_path, feed_icon_path, ready_icon_path,
                 stop_left_path=None, stop_right_path=None):
        self.x = x
        self.y = y
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

        self.frames = self.load_gif(gif_path)

        self.stop_left_frames = self.load_gif(stop_left_path) if stop_left_path else self.frames
        self.stop_right_frames = self.load_gif(stop_right_path) if stop_right_path else self.frames
        self.last_direction = "right"

        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.speed = 0.5 
        self.direction = pygame.math.Vector2()
        self.move_timer = 0
        self.move_interval = 1500
        
        self.status = "HUNGRY"
        self.feed_time = 0
        self.produce_duration = produce_time_ms
        
        self.feed_icon = self.load_icon(feed_icon_path)
        self.ready_icon = self.load_icon(ready_icon_path)

    def load_gif(self, filename):
        frames = []
        gif = Image.open(filename)
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = gif.convert("RGBA")
            pygame_image = pygame.image.fromstring(
                frame_image.tobytes(), frame_image.size, frame_image.mode
            ).convert_alpha()
            frames.append(pygame_image)
        return frames

    def load_icon(self, path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (24, 24))
        except:
            return None

    def feed(self):
        if self.status == "HUNGRY":
            self.status = "DIGESTING"
            self.feed_time = pygame.time.get_ticks()
            self.frame_index = 0

    def get_feet_rect(self):
        feet_width = self.rect.width * 0.5
        feet_height = 5
        return pygame.Rect(
            self.rect.centerx - feet_width / 2,
            self.rect.bottom - 5,
            feet_width, feet_height
        )

    def get_bubble_rect(self):
        if self.status in ["HUNGRY", "READY"]:
            bubble_size = 36
            return pygame.Rect(
                self.x - (bubble_size / 2),
                self.rect.top - bubble_size - 8,
                bubble_size, bubble_size
            )
        return None

    def update(self, game_map):
        current_time = pygame.time.get_ticks()

        if self.status == "DIGESTING":
            if current_time - self.feed_time >= self.produce_duration:
                self.status = "READY"
                self.frame_index = 0

        is_moving = False
        
        if self.status == "HUNGRY":
            if current_time - self.move_timer > self.move_interval:
                self.move_timer = current_time
                self.direction.x = random.choice([-1, 0, 1])
                self.direction.y = random.choice([-1, 0, 1])

            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
                is_moving = True

            old_x = self.x
            self.x += self.direction.x * self.speed
            self.rect.center = (self.x, self.y)
            if not game_map.can_player_move(self.get_feet_rect()) or self.x < self.min_x or self.x > self.max_x:
                self.x = old_x

            old_y = self.y
            self.y += self.direction.y * self.speed
            self.rect.center = (self.x, self.y)
            if not game_map.can_player_move(self.get_feet_rect()) or self.y < self.min_y or self.y > self.max_y:
                self.y = old_y

            if self.direction.x < 0:
                self.last_direction = "left"
            elif self.direction.x > 0:
                self.last_direction = "right"

        if self.status == "DIGESTING":
            if self.last_direction == "left":
                active_frames = self.stop_left_frames
            else:
                active_frames = self.stop_right_frames
        else:
            active_frames = self.frames

        if is_moving or self.status == "DIGESTING":
            self.frame_index += self.animation_speed
            if self.frame_index >= len(active_frames):
                self.frame_index = 0
        else:
            self.frame_index = 0
            
        self.image = active_frames[int(self.frame_index)]

    @abstractmethod
    def produce(self): 
        pass

    def harvest(self):
        if self.status == "READY":
            self.status = "HUNGRY"
            return self.produce()
        return None

    def draw(self, screen, camera):
        draw_x = (self.x - camera.x) * camera.zoom
        draw_y = (self.y - camera.y) * camera.zoom 
        
        scaled_width = int(self.image.get_width() * camera.zoom)
        scaled_height = int(self.image.get_height() * camera.zoom)
        scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        
        rect = scaled_image.get_rect(center=(draw_x, draw_y))
        screen.blit(scaled_image, rect)
        
        active_icon = None
        if self.status == "HUNGRY":
            active_icon = self.feed_icon
        elif self.status == "READY":
            active_icon = self.ready_icon
            
        if active_icon:
            bubble_size = int(36 * camera.zoom)
            bubble_x = draw_x - (bubble_size / 2)
            bubble_y = rect.top - bubble_size - int(8 * camera.zoom)
            bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_size, bubble_size)
            
            pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=int(8 * camera.zoom))
            pygame.draw.rect(screen, (150, 150, 150), bubble_rect, width=int(2 * camera.zoom), border_radius=int(8 * camera.zoom))
            
            icon_size = int(24 * camera.zoom)
            scaled_icon = pygame.transform.scale(active_icon, (icon_size, icon_size))
            icon_rect = scaled_icon.get_rect(center=bubble_rect.center)
            screen.blit(scaled_icon, icon_rect)