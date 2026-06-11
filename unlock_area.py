import pygame


class UnlockAreaSystem:
    def __init__(self, game_map, level_system):
        self.game_map = game_map
        self.level_system = level_system
        self.areas = []

        self.small_font = pygame.font.SysFont(None, 20)

        self.lock_image = pygame.image.load("menu_bar/lock.png").convert_alpha()
        self.lock_image = pygame.transform.scale(self.lock_image, (46, 46))

        self.load_areas_from_tiled()

    def load_areas_from_tiled(self):
        layer = None

        for tiled_layer in self.game_map.tmx_data.layers:
            if tiled_layer.name == "UnlockArea":
                layer = tiled_layer
                break

        if layer is None:
            return

        for obj in layer:
            area_name = obj.name

            required_level = obj.properties.get("required_level", 1)
            required_level = int(required_level)

            rect = pygame.Rect(
                int(obj.x - self.game_map.used_x),
                int(obj.y - self.game_map.used_y),
                int(obj.width),
                int(obj.height)
            )

            self.areas.append({
                "name": area_name,
                "rect": rect,
                "required_level": required_level
            })

    def screen_to_world(self, mouse_pos, camera):
        mouse_x, mouse_y = mouse_pos

        world_x = camera.x + mouse_x / camera.zoom
        world_y = camera.y + mouse_y / camera.zoom

        return world_x, world_y

    def is_area_unlocked(self, area):
        return self.level_system.get_level() >= area["required_level"]

    def get_area_at_mouse(self, mouse_pos, camera):
        world_x, world_y = self.screen_to_world(mouse_pos, camera)

        for area in self.areas:
            if area["rect"].collidepoint(world_x, world_y):
                return area

        return None

    def is_click_blocked(self, mouse_pos, camera):
        area = self.get_area_at_mouse(mouse_pos, camera)

        if area is None:
            return False, ""

        if self.is_area_unlocked(area):
            return False, ""

        message = f"This area unlocks at Level {area['required_level']}"
        return True, message

    def is_rect_blocked(self, rect):
        for area in self.areas:
            if self.is_area_unlocked(area):
                continue

            if rect.colliderect(area["rect"]):
                message = f"This area unlocks at Level {area['required_level']}"
                return True, message

        return False, ""

    def draw(self, screen, camera):
        for area in self.areas:
            if self.is_area_unlocked(area):
                continue

            rect = area["rect"]

            screen_rect = pygame.Rect(
                int((rect.x - camera.x) * camera.zoom),
                int((rect.y - camera.y) * camera.zoom),
                int(rect.width * camera.zoom),
                int(rect.height * camera.zoom)
            )

            if (
                screen_rect.right < 0
                or screen_rect.left > screen.get_width()
                or screen_rect.bottom < 0
                or screen_rect.top > screen.get_height()
            ):
                continue

            overlay = pygame.Surface(
                (screen_rect.width, screen_rect.height),
                pygame.SRCALPHA
            )

            overlay.fill((70, 70, 70, 120))
            screen.blit(overlay, (screen_rect.x, screen_rect.y))

            pygame.draw.rect(
                screen,
                (80, 80, 80),
                screen_rect,
                3,
                border_radius=8
            )

            self.draw_lock(screen, screen_rect, area["required_level"])

    def draw_lock(self, screen, screen_rect, required_level):
        center_x = screen_rect.centerx
        center_y = screen_rect.centery

        lock_rect = self.lock_image.get_rect(
            center=(center_x, center_y)
        )

        screen.blit(self.lock_image, lock_rect)

        level_text = self.small_font.render(
            f"Level {required_level}",
            True,
            (255, 255, 255)
        )

        level_rect = level_text.get_rect(
            center=(center_x, center_y + 38)
        )

        screen.blit(level_text, level_rect)