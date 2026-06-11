import pygame

class LevelSystem:
    def __init__(self):
        self.current_level = 1
        self.max_level = 4

        self.level_data = {
            1: {
                "areas": ["area_lvl_1"],
                "items": [
                    "Shovel",
                    "Carrot"
                ],
                "features": [
                    "planting"
                ],
                "message": "Level 1: Lahan awal dan Carrot terbuka."
            },

            2: {
                "areas": [
                    "area_lvl_1",
                    "area_lvl_2"
                ],
                "items": [
                    "Shovel",
                    "Carrot",
                    "Cabbage"
                ],
                "features": [
                    "planting"
                ],
                "message": "Level 2: Lahan baru dan Cabbage terbuka."
            },

            3: {
                "areas": [
                    "area_lvl_1",
                    "area_lvl_2",
                    "area_lvl_3"
                ],
                "items": [
                    "Shovel",
                    "Weapon",
                    "Carrot",
                    "Cabbage",
                    "Strawberry",
                    "Chicken Feed"
                ],
                "features": [
                    "planting",
                    "chicken",
                    "chicken_feed",
                    "enemy",
                    "weapon"
                ],
                "message": "Level 3: Ayam, Chicken Feed, Strawberry, Weapon, dan Enemy terbuka."
            },

            4: {
                "areas": [
                    "area_lvl_1",
                    "area_lvl_2",
                    "area_lvl_3",
                    "area_lvl_4"
                ],
                "items": [
                    "Shovel",
                    "Weapon",
                    "Carrot",
                    "Cabbage",
                    "Strawberry",
                    "Pumpkin",
                    "Chicken Feed",
                    "Cows Feed"
                ],
                "features": [
                    "planting",
                    "chicken",
                    "cow",
                    "chicken_feed",
                    "cow_feed",
                    "enemy",
                    "weapon",
                    "all_features"
                ],
                "message": "Level 4: Sapi, Cows Feed, Pumpkin, dan semua fitur terbuka."
            }
        }

        self.item_required_level = {
            "Shovel": 1,
            "Carrot": 1,

            "Cabbage": 2,

            "Weapon": 3,
            "Strawberry": 3,
            "Chicken Feed": 3,

            "Pumpkin": 4,
            "Cows Feed": 4
        }

        self.area_required_level = {
            "area_lvl_1": 1,
            "area_lvl_2": 2,
            "area_lvl_3": 3,
            "area_lvl_4": 4
        }

        self.feature_required_level = {
            "planting": 1,

            "cabbage": 2,

            "weapon": 3,
            "strawberry": 3,
            "chicken": 3,
            "chicken_feed": 3,
            "enemy": 3,

            "pumpkin": 4,
            "cow": 4,
            "cow_feed": 4,
            "all_features": 4
        }

    def get_level(self):
        return self.current_level

    def set_level(self, level):
        if level < 1:
            self.current_level = 1
        elif level > self.max_level:
            self.current_level = self.max_level
        else:
            self.current_level = level

    def level_up(self):
        if self.current_level < self.max_level:
            self.current_level += 1
            return True

        return False

    def is_item_unlocked(self, item_name):
        required_level = self.item_required_level.get(item_name, 1)
        return self.current_level >= required_level

    def get_item_required_level(self, item_name):
        return self.item_required_level.get(item_name, 1)

    def is_area_unlocked(self, area_name):
        required_level = self.area_required_level.get(area_name, 1)
        return self.current_level >= required_level

    def get_area_required_level(self, area_name):
        return self.area_required_level.get(area_name, 1)

    def is_feature_unlocked(self, feature_name):
        required_level = self.feature_required_level.get(feature_name, 1)
        return self.current_level >= required_level

    def get_feature_required_level(self, feature_name):
        return self.feature_required_level.get(feature_name, 1)

    def get_unlocked_items(self):
        return self.level_data[self.current_level]["items"]

    def get_unlocked_areas(self):
        return self.level_data[self.current_level]["areas"]

    def get_unlocked_features(self):
        return self.level_data[self.current_level]["features"]

    def get_level_message(self):
        return self.level_data[self.current_level]["message"]

    def get_locked_item_message(self, item_name):
        required_level = self.get_item_required_level(item_name)

        return f"{item_name} terbuka di Level {required_level}"

    def get_locked_area_message(self, area_name):
        required_level = self.get_area_required_level(area_name)

        return f"Area ini terbuka di Level {required_level}"