import pygame

class PlantSystem:
    def __init__(self, soil_image_path, tile_width, tile_height):
        self.tile_width = tile_width
        self.tile_height = tile_height

        self.soil_image = pygame.image.load(soil_image_path).convert_alpha()
        self.soil_image = pygame.transform.scale(
            self.soil_image,
            (self.tile_width, self.tile_height)
        )

        self.tilled_tiles = set()

    def screen_to_world(self, mouse_pos, camera):
        mouse_x, mouse_y = mouse_pos

        world_x = mouse_x / camera.zoom + camera.x
        world_y = mouse_y / camera.zoom + camera.y

        return world_x, world_y

    def world_to_tile(self, world_x, world_y):
        tile_x = int(world_x // self.tile_width)
        tile_y = int(world_y // self.tile_height)

        return tile_x, tile_y

    def screen_to_tile(self, mouse_pos, camera):
        world_x, world_y = self.screen_to_world(mouse_pos, camera)

        tile_x, tile_y = self.world_to_tile(world_x, world_y)

        return tile_x, tile_y

    def use_shovel(self, mouse_pos, camera):
        tile_x, tile_y = self.screen_to_tile(mouse_pos, camera)

        if (tile_x, tile_y) in self.tilled_tiles:
            print("Tile ini sudah jadi soil:", tile_x, tile_y)
            return

        self.tilled_tiles.add((tile_x, tile_y))

        print("Grass berubah jadi soil di tile:", tile_x, tile_y)

    def handle_click(self, mouse_pos, camera, selected_item_name):
        if selected_item_name == "Shovel":
            self.use_shovel(mouse_pos, camera)

    def draw(self, screen, camera):
        for tile_x, tile_y in self.tilled_tiles:
            world_x = tile_x * self.tile_width
            world_y = tile_y * self.tile_height

            screen_x = (world_x - camera.x) * camera.zoom
            screen_y = (world_y - camera.y) * camera.zoom

            scaled_width = int(self.tile_width * camera.zoom)
            scaled_height = int(self.tile_height * camera.zoom)

            scaled_soil = pygame.transform.scale(
                self.soil_image,
                (scaled_width, scaled_height)
            )

            screen.blit(scaled_soil, (screen_x, screen_y))