class LevelProgressSystem:
    def __init__(self, level_system, coin):
        self.level_system = level_system
        self.coin = coin

        self.level_targets = {
            1: {
                "target_coin": 75,
                "bonus_coin": 0
            },
            2: {
                "target_coin": 110,
                "bonus_coin": 10
            },
            3: {
                "target_coin": 160,
                "bonus_coin": 20
            }
        }

        self.max_level = 4

    def check_level_progress(self):
        current_level = self.level_system.get_level()

        if current_level >= self.max_level:
            return None

        target_data = self.level_targets.get(current_level)

        if target_data is None:
            return None

        target_coin = target_data["target_coin"]
        bonus_coin = target_data["bonus_coin"]

        if self.coin.amount >= target_coin:
            naik = self.level_system.level_up()

            if naik:
                if bonus_coin > 0:
                    self.coin.add(bonus_coin)
                    return f"Level Up! Bonus +{bonus_coin} coins"

                return "Level Up! New area unlocked"

        return None

    def get_current_target_coin(self):
        current_level = self.level_system.get_level()

        if current_level >= self.max_level:
            return None

        target_data = self.level_targets.get(current_level)

        if target_data is None:
            return None

        return target_data["target_coin"]

    def get_bonus_coin(self):
        current_level = self.level_system.get_level()

        if current_level >= self.max_level:
            return None

        target_data = self.level_targets.get(current_level)

        if target_data is None:
            return None

        return target_data["bonus_coin"]

    def is_max_level(self):
        return self.level_system.get_level() >= self.max_level