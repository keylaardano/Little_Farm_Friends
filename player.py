import pygame
from PIL import Image
from inventory import Inventory
from game_object import GameObject


class Player(GameObject):
    def __init__(self, x, y, map_width, map_height):

        self._x = x
        self._y = y

        self._map_width = map_width
        self._map_height = map_height

        self._speed = 4
        self._scale = 2

        self._direction = "depan"
        self._is_moving = False
        self._current_tool = None

        self._frame_index = 0
        self._animation_speed = 0.75

        self._is_attacking = False
        self._attack_timer = 0
        self._attack_duration = 8
        self._attack_range = 65
        self._attack_size = 50
        self._attack_damage = 1

        self._inventory = []

        self._animations = {
            "jalan_depan": self.load_gif("karakter/jalan depan.gif"),
            "jalan_belakang": self.load_gif("karakter/jalan belakang.gif"),
            "jalan_kiri": self.load_gif("karakter/jalan kiri.gif"),
            "jalan_kanan": self.load_gif("karakter/jalan kanan.gif"),

            "berhenti_depan": self.load_gif("karakter/berhenti depan.gif"),
            "berhenti_belakang": self.load_gif("karakter/berhenti belakang.gif"),
            "berhenti_kiri": self.load_gif("karakter/berhenti kiri.gif"),
            "berhenti_kanan": self.load_gif("karakter/berhenti kanan.gif"),

            "serang_depan": self.load_gif("karakter/serang depan.gif"),
            "serang_belakang": self.load_gif("karakter/serang belakang.gif"),
            "serang_kiri": self.load_gif("karakter/serang kiri.gif"),
            "serang_kanan": self.load_gif("karakter/serang kanan.gif"),
        }

        self._image = self._animations["berhenti_depan"][0]
        self._rect = self._image.get_rect(center=(self._x, self._y))


    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def rect(self):
        return self._rect

    @property
    def image(self):
        return self._image

    @property
    def direction(self):
        return self._direction

    @property
    def is_moving(self):
        return self._is_moving

    @property
    def current_tool(self):
        return self._current_tool

    @property
    def attack_damage(self):
        return self._attack_damage

    def load_gif(self, filename):
        frames = []
        gif = Image.open(filename)

        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = gif.convert("RGBA")

            pygame_image = pygame.image.fromstring(
                frame_image.tobytes(),
                frame_image.size,
                "RGBA"
            ).convert_alpha()

            pygame_image = pygame.transform.scale(
                pygame_image,
                (
                    pygame_image.get_width() * self._scale,
                    pygame_image.get_height() * self._scale
                )
            )

            frames.append(pygame_image)

        return frames


    def set_current_tool(self, tool_name):
        self._current_tool = tool_name

    def get_current_tool(self):
        return self._current_tool

    def get_position(self):
        return self._x, self._y

    def get_center(self):
        return self._rect.centerx, self._rect.centery

    def get_rect(self):
        return self._rect

    def get_rect_copy(self):
        return self._rect.copy()

    def get_attack_damage(self):
        return self._attack_damage

    def get_attack_range(self):
        return self._attack_range

    def is_player_moving(self):
        return self._is_moving

    def distance_to(self, target_x, target_y):
        dx = self._x - target_x
        dy = self._y - target_y
        return (dx ** 2 + dy ** 2) ** 0.5

    def restore_position(self, old_x, old_y, old_rect):
        self._x = old_x
        self._y = old_y
        self._rect = old_rect

    def update_rect(self):
        self._rect = self._image.get_rect(center=(self._x, self._y))

    def get_feet_rect(self):
        feet_width = self._rect.width * 0.22
        feet_height = 5

        return pygame.Rect(
            self._rect.centerx - feet_width / 2,
            self._rect.bottom - 5,
            feet_width,
            feet_height
        )

    def handle_input(self, game_map):
        keys = pygame.key.get_pressed()
        self._is_moving = False

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT]:
            dx = -self._speed
            self._direction = "kiri"
            self._is_moving = True

        elif keys[pygame.K_RIGHT]:
            dx = self._speed
            self._direction = "kanan"
            self._is_moving = True

        elif keys[pygame.K_UP]:
            dy = -self._speed
            self._direction = "belakang"
            self._is_moving = True

        elif keys[pygame.K_DOWN]:
            dy = self._speed
            self._direction = "depan"
            self._is_moving = True

        old_x = self._x
        self._x += dx
        self.update_rect()

        if not game_map.can_player_move(self.get_feet_rect()):
            self._x = old_x
            self.update_rect()

        old_y = self._y
        self._y += dy
        self.update_rect()

        if not game_map.can_player_move(self.get_feet_rect()):
            self._y = old_y
            self.update_rect()

        self.limit_area()

    def limit_area(self):
        player_width = self._image.get_width()
        player_height = self._image.get_height()

        if self._x < player_width // 2:
            self._x = player_width // 2

        if self._x > self._map_width - player_width // 2:
            self._x = self._map_width - player_width // 2

        if self._y < player_height // 2:
            self._y = player_height // 2

        if self._y > self._map_height - player_height // 2:
            self._y = self._map_height - player_height // 2

        self.update_rect()

    def update_animation(self):

        if self._is_attacking:
            animation_key = "serang_" + self._direction

        elif self._is_moving:
            animation_key = "jalan_" + self._direction

        else:
            animation_key = "berhenti_" + self._direction

        frames = self._animations[animation_key]

        if self._is_attacking or self._is_moving:
            self._frame_index += self._animation_speed

            if self._frame_index >= len(frames):
                self._frame_index = 0
        else:
            self._frame_index = 0

        self._image = frames[int(self._frame_index)]
        self.update_rect()

    def attack(self):
        if self._current_tool != "Weapon":
            return False

        self._is_attacking = True
        self._attack_timer = self._attack_duration
        self._frame_index = 0

        print("Player menyerang dengan Weapon!")
        return True

    def get_attack_rect(self):
        if self._direction == "depan":
            return pygame.Rect(
                self._rect.centerx - self._attack_size // 2,
                self._rect.bottom - 10,
                self._attack_size,
                self._attack_range
            )

        if self._direction == "belakang":
            return pygame.Rect(
                self._rect.centerx - self._attack_size // 2,
                self._rect.top - self._attack_range + 10,
                self._attack_size,
                self._attack_range
            )

        if self._direction == "kiri":
            return pygame.Rect(
                self._rect.left - self._attack_range + 10,
                self._rect.centery - self._attack_size // 2,
                self._attack_range,
                self._attack_size
            )

        if self._direction == "kanan":
            return pygame.Rect(
                self._rect.right - 10,
                self._rect.centery - self._attack_size // 2,
                self._attack_range,
                self._attack_size
            )

        return pygame.Rect(self._rect.centerx, self._rect.centery, 0, 0)

    def interact_with_animal(self, animal_object, active_item, ui_inventory: Inventory, coin=None):
        if animal_object.status == "HUNGRY":
            if active_item == animal_object.required_feed:
                animal_object.feed()
                print(f"Berhasil memberi makan dengan {active_item}!")
            else:
                print(f"Gagal! Hewan ini butuh {animal_object.required_feed}, tapi kamu memegang {active_item}.")

        elif animal_object.status == "DIGESTING":
            print("Sabar ya, hewannya masih ngunyah dan memproses hasil panen!")

        elif animal_object.status == "READY":
            item = animal_object.harvest()

            if item:
                if item == "Telur":
                    ui_inventory.add_item("Egg", 1)

                elif item == "Susu":
                    ui_inventory.add_item("Milk", 1)

                print(f"Panen sukses! {item} berhasil masuk ke UI Inventory.")

    def update(self, game_map=None):
        if game_map is None:
            return

        self.handle_input(game_map)

        if self._attack_timer > 0:
            self._attack_timer -= 1
        else:
            self._is_attacking = False

        self.update_animation()

    def draw(self, screen, camera):
        draw_x = (self._x - camera.x) * camera.zoom
        draw_y = (self._y - camera.y) * camera.zoom

        scaled_width = int(self._image.get_width() * camera.zoom)
        scaled_height = int(self._image.get_height() * camera.zoom)

        scaled_image = pygame.transform.scale(
            self._image,
            (scaled_width, scaled_height)
        )

        rect = scaled_image.get_rect(center=(draw_x, draw_y))
        screen.blit(scaled_image, rect)