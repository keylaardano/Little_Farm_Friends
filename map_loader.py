import pygame
from pytmx.util_pygame import load_pygame


class MapLoader:
    def __init__(self, map_path):
        self.tmx_data = load_pygame(map_path)

        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight

        self.map_width = self.tmx_data.width * self.tile_width
        self.map_height = self.tmx_data.height * self.tile_height

        self.used_x = 0
        self.used_y = 0
        self.used_width = self.map_width
        self.used_height = self.map_height

        self.calculate_used_area()

    def calculate_used_area(self):
        data = {
            "min_x": self.tmx_data.width,
            "min_y": self.tmx_data.height,
            "max_x": 0,
            "max_y": 0,
            "found_tile": False
        }

        for layer in self.tmx_data.visible_layers:
            self.check_layer_used_area(layer, data)

        if data["found_tile"]:
            self.used_x = data["min_x"] * self.tile_width
            self.used_y = data["min_y"] * self.tile_height
            self.used_width = (data["max_x"] - data["min_x"] + 1) * self.tile_width
            self.used_height = (data["max_y"] - data["min_y"] + 1) * self.tile_height

    def check_layer_used_area(self, layer, data):
        layer_name = layer.name.lower().strip()

        if layer_name == "collision":
            return

        if hasattr(layer, "data"):
            for y in range(layer.height):
                for x in range(layer.width):
                    gid = layer.data[y][x]

                    if gid != 0:
                        data["found_tile"] = True
                        data["min_x"] = min(data["min_x"], x)
                        data["min_y"] = min(data["min_y"], y)
                        data["max_x"] = max(data["max_x"], x)
                        data["max_y"] = max(data["max_y"], y)

        elif hasattr(layer, "layers"):
            for sub_layer in layer.layers:
                self.check_layer_used_area(sub_layer, data)

    def get_layer_by_name(self, layer_name):
        target_name = layer_name.lower().strip()

        def search_layer(layers):
            for layer in layers:
                current_name = layer.name.lower().strip()

                if current_name == target_name:
                    return layer

                if hasattr(layer, "layers"):
                    result = search_layer(layer.layers)
                    if result:
                        return result

            return None

        return search_layer(self.tmx_data.layers)

    def is_grid_filled(self, layer, tile_x, tile_y):
        """
        Mengecek apakah grid/tile tertentu berisi collision.

        tile_x = posisi kolom grid
        tile_y = posisi baris grid

        Jika ada tile pada layer Collision, berarti tidak bisa dilewati.
        """

        if layer is None:
            return False

        if tile_x < 0 or tile_y < 0:
            return True

        if tile_x >= layer.width or tile_y >= layer.height:
            return True

        gid = layer.data[tile_y][tile_x]

        return gid != 0

    def is_collision(self, feet_rect):
        collision_layer = self.get_layer_by_name("Collision")

        if collision_layer is None:
            return False

        row_offset = -1

        left = int((feet_rect.left + self.used_x) // self.tile_width)
        right = int((feet_rect.right - 1 + self.used_x) // self.tile_width)
        top = int((feet_rect.top + self.used_y) // self.tile_height) + row_offset
        bottom = int((feet_rect.bottom - 1 + self.used_y) // self.tile_height) + row_offset

        for tile_y in range(top, bottom + 1):
            for tile_x in range(left, right + 1):
                if self.is_grid_filled(collision_layer, tile_x, tile_y):
                    return True

        return False

    def can_player_move(self, feet_rect):
        return not self.is_collision(feet_rect)

    def get_animated_gid(self, gid, current_time):
        if gid == 0:
            return 0

        properties = self.tmx_data.get_tile_properties_by_gid(gid)

        if properties and "frames" in properties:
            frames = properties["frames"]
            total_duration = sum(frame.duration for frame in frames)

            if total_duration == 0:
                return gid

            time = current_time % total_duration
            elapsed = 0

            for frame in frames:
                elapsed += frame.duration

                if time <= elapsed:
                    return frame.gid

        return gid

    def draw_tile_layer_to_surface(self, target_surface, layer, parent_opacity=1):
        layer_name = layer.name.lower().strip()

        if layer_name == "collision":
            return

        layer_opacity = getattr(layer, "opacity", 1)
        final_opacity = parent_opacity * layer_opacity

        if layer_name == "shadows":
            final_opacity = 0.25

        layer_surface = pygame.Surface(
            (self.used_width, self.used_height),
            pygame.SRCALPHA
        ).convert_alpha()

        current_time = pygame.time.get_ticks()

        for y in range(layer.height):
            for x in range(layer.width):
                gid = layer.data[y][x]

                if gid == 0:
                    continue

                gid = self.get_animated_gid(gid, current_time)
                image = self.tmx_data.get_tile_image_by_gid(gid)

                if image:
                    draw_x = x * self.tile_width - self.used_x
                    draw_y = y * self.tile_height - self.used_y

                    layer_surface.blit(
                        image.convert_alpha(),
                        (draw_x, draw_y)
                    )

        layer_surface.set_alpha(int(final_opacity * 255))
        target_surface.blit(layer_surface, (0, 0))

    def draw_layer_to_surface(self, target_surface, layer, parent_opacity=1):
        layer_name = layer.name.lower().strip()

        if layer_name == "collision":
            return

        if hasattr(layer, "data"):
            self.draw_tile_layer_to_surface(
                target_surface,
                layer,
                parent_opacity
            )

        elif hasattr(layer, "layers"):
            group_opacity = getattr(layer, "opacity", 1)
            new_parent_opacity = parent_opacity * group_opacity

            for sub_layer in layer.layers:
                self.draw_layer_to_surface(
                    target_surface,
                    sub_layer,
                    new_parent_opacity
                )

    def render_map_surface(self):
        map_surface = pygame.Surface(
            (self.used_width, self.used_height),
            pygame.SRCALPHA
        ).convert_alpha()

        map_surface.fill((0, 0, 0, 0))

        for layer in self.tmx_data.visible_layers:
            self.draw_layer_to_surface(map_surface, layer)

        return map_surface

    def draw(self, screen, camera):
        map_surface = self.render_map_surface()

        scaled_width = int(self.used_width * camera.zoom)
        scaled_height = int(self.used_height * camera.zoom)

        scaled_map = pygame.transform.scale(
            map_surface,
            (scaled_width, scaled_height)
        )

        screen.blit(
            scaled_map,
            (
                -camera.x * camera.zoom,
                -camera.y * camera.zoom
            )
        )