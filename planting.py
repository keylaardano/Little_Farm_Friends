import pygame

class Crop:
    def __init__(
        self,
        tile_x,
        tile_y,
        name,
        image_paths,
        harvest_item,
        seed_price,
        sell_price,
        stage_duration,
        tile_width,
        tile_height
    ):
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.name = name
        self.harvest_item = harvest_item
        self.seed_price = seed_price
        self.sell_price = sell_price
        self.stage_duration = stage_duration

        self.stage = 0
        self.planted_time = pygame.time.get_ticks()

        self.images = self.load_images(
            image_paths,
            tile_width,
            tile_height
        )

    def load_images(self, image_paths, tile_width, tile_height):
        images = []

        for path in image_paths:
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(
                    image,
                    (tile_width, tile_height)
                )
                images.append(image)

            except:
                print("Gambar crop tidak ditemukan:", path)

                fallback = pygame.Surface(
                    (tile_width, tile_height),
                    pygame.SRCALPHA
                )
                fallback.fill((0, 0, 0, 0))

                pygame.draw.rect(
                    fallback,
                    (80, 180, 80),
                    pygame.Rect(
                        4,
                        4,
                        tile_width - 8,
                        tile_height - 8
                    )
                )

                images.append(fallback)

        return images

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.planted_time

        new_stage = elapsed // self.stage_duration

        if new_stage > 3:
            new_stage = 3

        self.stage = int(new_stage)

    def is_ready_to_harvest(self):
        return self.stage == 3

    def get_image(self):
        return self.images[self.stage]

    def get_harvest_item(self):
        return self.harvest_item

    def get_seed_price(self):
        return self.seed_price

    def get_sell_price(self):
        return self.sell_price


class Carrot(Crop):
    def __init__(self, tile_x, tile_y, tile_width, tile_height):
        super().__init__(
            tile_x=tile_x,
            tile_y=tile_y,
            name="Carrot",
            image_paths=[
                "tanaman/carrots_grows/carrot_1.png",
                "tanaman/carrots_grows/carrot_2.png",
                "tanaman/carrots_grows/carrot_3.png",
                "tanaman/carrots_grows/carrot_4.png"
            ],
            harvest_item="Carrot",
            seed_price=5,
            sell_price=8,
            stage_duration=10000,
            tile_width=tile_width,
            tile_height=tile_height
        )


class Cabbage(Crop):
    def __init__(self, tile_x, tile_y, tile_width, tile_height):
        super().__init__(
            tile_x=tile_x,
            tile_y=tile_y,
            name="Cabbage",
            image_paths=[
                "tanaman/cabbage_grows/cabbage_1.png",
                "tanaman/cabbage_grows/cabbage_2.png",
                "tanaman/cabbage_grows/cabbage_3.png",
                "tanaman/cabbage_grows/cabbage_4.png"
            ],
            harvest_item="Cabbage",
            seed_price=10,
            sell_price=15,
            stage_duration=16667,
            tile_width=tile_width,
            tile_height=tile_height
        )


class Strawberry(Crop):
    def __init__(self, tile_x, tile_y, tile_width, tile_height):
        super().__init__(
            tile_x=tile_x,
            tile_y=tile_y,
            name="Strawberry",
            image_paths=[
                "tanaman/strawberry_grows/strawberry_1.png",
                "tanaman/strawberry_grows/strawberry_2.png",
                "tanaman/strawberry_grows/strawberry_3.png",
                "tanaman/strawberry_grows/strawberry_4.png"
            ],
            harvest_item="Strawberry",
            seed_price=20,
            sell_price=30,
            stage_duration=23333,
            tile_width=tile_width,
            tile_height=tile_height
        )


class Pumpkin(Crop):
    def __init__(self, tile_x, tile_y, tile_width, tile_height):
        super().__init__(
            tile_x=tile_x,
            tile_y=tile_y,
            name="Pumpkin",
            image_paths=[
                "tanaman/pumpkin_grows/pumpkin_1.png",
                "tanaman/pumpkin_grows/pumpkin_2.png",
                "tanaman/pumpkin_grows/pumpkin_3.png",
                "tanaman/pumpkin_grows/pumpkin_4.png"
            ],
            harvest_item="Pumpkin",
            seed_price=40,
            sell_price=60,
            stage_duration=30000,
            tile_width=tile_width,
            tile_height=tile_height
        )


class PlantingSystem:
    def __init__(self, tile_width, tile_height):
        self.tile_width = tile_width
        self.tile_height = tile_height

        self.crops = {}

        self.crop_classes = {
            "Carrot": Carrot,
            "Cabbage": Cabbage,
            "Strawberry": Strawberry,
            "Pumpkin": Pumpkin
        }

        self.seed_prices = {
            "Carrot": 5,
            "Cabbage": 10,
            "Strawberry": 20,
            "Pumpkin": 40
        }

        self.sell_prices = {
            "Carrot": 8,
            "Cabbage": 15,
            "Strawberry": 30,
            "Pumpkin": 60
        }

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
        return self.world_to_tile(world_x, world_y)

    def create_crop(self, crop_name, tile_x, tile_y):
        if crop_name not in self.crop_classes:
            return None

        crop_class = self.crop_classes[crop_name]

        return crop_class(
            tile_x,
            tile_y,
            self.tile_width,
            self.tile_height
        )

    def plant_seed(self, tile_x, tile_y, crop_name, tilled_tiles, coin):
        if crop_name not in self.crop_classes:
            return False

        if (tile_x, tile_y) not in tilled_tiles:
            print("Tidak bisa menanam. Tanah belum jadi soil.")
            return False

        if (tile_x, tile_y) in self.crops:
            print("Tile ini sudah ada tanaman.")
            return False

        seed_price = self.seed_prices[crop_name]

        if not coin.spend(seed_price):
            print("Gagal menanam", crop_name, "karena coin tidak cukup.")
            return False

        new_crop = self.create_crop(
            crop_name,
            tile_x,
            tile_y
        )

        if new_crop is None:
            return False

        self.crops[(tile_x, tile_y)] = new_crop

        print(
            crop_name,
            "ditanam di tile:",
            tile_x,
            tile_y,
            "| Harga bibit:",
            seed_price
        )

        return True

    def harvest_crop(self, tile_x, tile_y, inventory):
        if (tile_x, tile_y) not in self.crops:
            return False

        crop = self.crops[(tile_x, tile_y)]

        if not crop.is_ready_to_harvest():
            print("Tanaman belum matang.")
            return False

        harvest_item = crop.get_harvest_item()

        inventory.add_item(harvest_item, 1)

        del self.crops[(tile_x, tile_y)]

        print(harvest_item, "berhasil dipanen dan masuk inventory.")

        return True

    def handle_click(
        self,
        mouse_pos,
        camera,
        selected_item_name,
        tilled_tiles,
        inventory,
        coin
    ):
        tile_x, tile_y = self.screen_to_tile(mouse_pos, camera)

        if (tile_x, tile_y) in self.crops:
            crop = self.crops[(tile_x, tile_y)]

            if crop.is_ready_to_harvest():
                self.harvest_crop(tile_x, tile_y, inventory)
                return False

            print("Tanaman belum siap panen.")
            return False

        if selected_item_name in self.crop_classes:
            return self.plant_seed(
                tile_x,
                tile_y,
                selected_item_name,
                tilled_tiles,
                coin
            )

        return False

    def get_all_crop_tiles(self):
        return list(self.crops.keys())

    def update(self):
        for crop in self.crops.values():
            crop.update()

    def draw(self, screen, camera):
        for crop in self.crops.values():
            image = crop.get_image()

            world_x = crop.tile_x * self.tile_width
            world_y = crop.tile_y * self.tile_height

            screen_x = (world_x - camera.x) * camera.zoom
            screen_y = (world_y - camera.y) * camera.zoom

            scaled_width = int(self.tile_width * camera.zoom)
            scaled_height = int(self.tile_height * camera.zoom)

            scaled_image = pygame.transform.scale(
                image,
                (scaled_width, scaled_height)
            )

            screen.blit(scaled_image, (screen_x, screen_y))