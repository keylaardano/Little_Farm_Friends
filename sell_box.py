import pygame


class SellBasketItem:
    def __init__(self, name, amount=1):
        self.name = name
        self.amount = amount

    def add_amount(self, amount=1):
        self.amount += amount

    def reduce_amount(self, amount=1):
        self.amount -= amount

        if self.amount < 0:
            self.amount = 0


class SellBasket:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, inventory_amount):
        current_amount = self.get_amount(item_name)

        if current_amount >= inventory_amount:
            return False

        if item_name not in self.items:
            self.items[item_name] = SellBasketItem(item_name, 1)
        else:
            self.items[item_name].add_amount(1)

        print(item_name, "masuk keranjang jual.")
        return True

    def remove_item(self, item_name):
        if item_name not in self.items:
            return

        self.items[item_name].reduce_amount(1)

        if self.items[item_name].amount <= 0:
            del self.items[item_name]

        print(item_name, "dikurangi dari keranjang.")

    def clear(self):
        self.items.clear()
        
    def is_empty(self):
        return len(self.items) == 0

    def get_amount(self, item_name):
        if item_name not in self.items:
            return 0

        return self.items[item_name].amount

    def get_items(self):
        return list(self.items.values())

    def calculate_total_price(self, sell_prices):
        total = 0

        for item in self.items.values():
            price = sell_prices.get(item.name, 0)
            total += price * item.amount

        return total


class SellBox:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.is_open = False

        self.font = pygame.font.SysFont(None, 20)
        self.small_font = pygame.font.SysFont(None, 18)
        self.title_font = pygame.font.SysFont(None, 32)

        self.button_size = 64
        self.button_margin_left = 24
        self.button_gap = 18

        self.button_rect = pygame.Rect(
            self.button_margin_left + (self.button_size + self.button_gap) * 2,
            screen_height - self.button_size - 24,
            self.button_size,
            self.button_size
        )

        self.button_pop_timer = 0
        self.button_pop_duration = 8

        self.sell_button_pop_timer = 0
        self.cancel_button_pop_timer = 0
        self.action_button_pop_duration = 8

        self.sell_icon_size = 34
        self.sell_icon = self.load_icon("menu_bar/sell.png")

        self.price_coin_icon_size = 13
        self.price_coin_icon = self.load_price_coin_icon("menu_bar/coin.png")

        self.panel_width = 640
        self.panel_height = 420
        self.panel_x = (screen_width - self.panel_width) // 2
        self.panel_y = (screen_height - self.panel_height) // 2

        self.slot_size = 58
        self.icon_size = 32
        self.gap = 18
        self.cols = 6

        self.sell_prices = {
            "Carrot": 8,
            "Cabbage": 15,
            "Strawberry": 30,
            "Pumpkin": 60,
            "Egg": 12,
            "Milk": 25
        }

        self.basket = SellBasket()
        self.item_pop_timers = {}

    def load_icon(self, path):
        try:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(
                image,
                (self.sell_icon_size, self.sell_icon_size)
            )
            return image

        except:
            print("Icon sell tidak ditemukan:", path)
            return None

    def load_price_coin_icon(self, path):
        try:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(
                image,
                (self.price_coin_icon_size, self.price_coin_icon_size)
            )
            return image

        except:
            print("Icon coin harga tidak ditemukan:", path)
            return None

    def toggle(self):
        self.is_open = not self.is_open
        self.button_pop_timer = self.button_pop_duration

    def handle_event(self, event, inventory, coin):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                if self.button_rect.collidepoint(mouse_pos):
                    self.toggle()

                elif self.is_open:
                    if self.get_close_button_rect().collidepoint(mouse_pos):
                        self.is_open = False

                    elif self.get_sell_button_rect().collidepoint(mouse_pos):
                        self.sell_button_pop_timer = self.action_button_pop_duration
                        self.sell_basket(inventory, coin)

                    elif self.get_cancel_button_rect().collidepoint(mouse_pos):
                        self.cancel_button_pop_timer = self.action_button_pop_duration
                        self.basket.clear()

                    else:
                        self.check_inventory_item_click(mouse_pos, inventory)
                        self.check_basket_item_click(mouse_pos)

    def update(self):
        if self.button_pop_timer > 0:
            self.button_pop_timer -= 1

        if self.sell_button_pop_timer > 0:
            self.sell_button_pop_timer -= 1

        if self.cancel_button_pop_timer > 0:
            self.cancel_button_pop_timer -= 1

        keys_to_delete = []

        for item_name in self.item_pop_timers:
            if self.item_pop_timers[item_name] > 0:
                self.item_pop_timers[item_name] -= 1
            else:
                keys_to_delete.append(item_name)

        for key in keys_to_delete:
            del self.item_pop_timers[key]

    def get_close_button_rect(self):
        return pygame.Rect(
            self.panel_x + self.panel_width - 46,
            self.panel_y + 16,
            30,
            30
        )

    def get_sell_button_rect(self):
        return pygame.Rect(
            self.panel_x + self.panel_width - 150,
            self.panel_y + self.panel_height - 55,
            110,
            36
        )

    def get_cancel_button_rect(self):
        return pygame.Rect(
            self.panel_x + self.panel_width - 275,
            self.panel_y + self.panel_height - 55,
            110,
            36
        )

    def get_inventory_area_start(self):
        return self.panel_x + 45, self.panel_y + 95

    def get_basket_area_start(self):
        return self.panel_x + 45, self.panel_y + 265

    def get_total_price(self):
        return self.basket.calculate_total_price(self.sell_prices)

    def add_to_basket(self, item_name, inventory):
        if item_name not in self.sell_prices:
            print("Item ini tidak bisa dijual:", item_name)
            return

        inventory_amount = inventory.get_item_amount(item_name)

        success = self.basket.add_item(
            item_name,
            inventory_amount
        )

        if success:
            self.item_pop_timers[item_name] = 8

    def remove_from_basket(self, item_name):
        self.basket.remove_item(item_name)

    def sell_basket(self, inventory, coin):
        if self.basket.is_empty():
            print("Selling cart is empty.")
            return

        total_coin = 0

        for basket_item in self.basket.get_items():
            item_name = basket_item.name
            amount = basket_item.amount

            price = self.sell_prices.get(item_name, 0)
            total_price = price * amount

            success = inventory.remove_item(item_name, amount)

            if success:
                total_coin += total_price
            else:
                print("Gagal menjual:", item_name)

        if total_coin > 0:
            coin.add(total_coin)
            print("Item terjual. Coin bertambah:", total_coin)

        self.basket.clear()

    def check_inventory_item_click(self, mouse_pos, inventory):
        start_x, start_y = self.get_inventory_area_start()
        visible_items = inventory.get_visible_items()

        for visible_index, data in enumerate(visible_items):
            real_index, item = data

            if item["name"] not in self.sell_prices:
                continue

            col = visible_index % self.cols
            row = visible_index // self.cols

            x = start_x + col * (self.slot_size + self.gap)
            y = start_y + row * (self.slot_size + 58)

            slot_rect = pygame.Rect(
                x,
                y,
                self.slot_size,
                self.slot_size
            )

            if slot_rect.collidepoint(mouse_pos):
                self.add_to_basket(item["name"], inventory)
                return

    def check_basket_item_click(self, mouse_pos):
        start_x, start_y = self.get_basket_area_start()
        basket_items = self.basket.get_items()

        for i, basket_item in enumerate(basket_items):
            col = i % self.cols
            row = i // self.cols

            x = start_x + col * (self.slot_size + self.gap)
            y = start_y + row * (self.slot_size + 42)

            slot_rect = pygame.Rect(
                x,
                y,
                self.slot_size,
                self.slot_size
            )

            if slot_rect.collidepoint(mouse_pos):
                self.remove_from_basket(basket_item.name)
                return

    def draw_pixel_rect(self, screen, rect, fill_color, border_color, shadow_color=None):
        if shadow_color is not None:
            shadow_rect = pygame.Rect(
                rect.x + 4,
                rect.y + 4,
                rect.width,
                rect.height
            )
            pygame.draw.rect(screen, shadow_color, shadow_rect)

        pygame.draw.rect(screen, border_color, rect)

        inner_rect = pygame.Rect(
            rect.x + 4,
            rect.y + 4,
            rect.width - 8,
            rect.height - 8
        )
        pygame.draw.rect(screen, fill_color, inner_rect)

        pygame.draw.line(
            screen,
            (255, 245, 210),
            (inner_rect.left, inner_rect.top),
            (inner_rect.right - 1, inner_rect.top),
            2
        )

        pygame.draw.line(
            screen,
            (255, 245, 210),
            (inner_rect.left, inner_rect.top),
            (inner_rect.left, inner_rect.bottom - 1),
            2
        )

        pygame.draw.line(
            screen,
            (155, 105, 65),
            (inner_rect.left, inner_rect.bottom - 1),
            (inner_rect.right - 1, inner_rect.bottom - 1),
            2
        )

        pygame.draw.line(
            screen,
            (155, 105, 65),
            (inner_rect.right - 1, inner_rect.top),
            (inner_rect.right - 1, inner_rect.bottom - 1),
            2
        )

    def draw_fallback_sell_icon(self, screen, center):
        x, y = center

        pygame.draw.rect(
            screen,
            (170, 110, 60),
            pygame.Rect(x - 15, y - 8, 30, 22)
        )

        pygame.draw.rect(
            screen,
            (95, 60, 35),
            pygame.Rect(x - 15, y - 8, 30, 22),
            2
        )

        pygame.draw.rect(
            screen,
            (230, 180, 80),
            pygame.Rect(x - 6, y - 16, 12, 8)
        )

        pygame.draw.line(
            screen,
            (95, 60, 35),
            (x - 10, y + 5),
            (x + 10, y + 5),
            2
        )

    def draw_button(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.button_rect.collidepoint(mouse_pos):
            button_color = (255, 230, 170)
        else:
            button_color = (240, 210, 150)

        pop_scale = 1.0

        if self.button_pop_timer > 0:
            pop_scale = 1.08

        width = int(self.button_rect.width * pop_scale)
        height = int(self.button_rect.height * pop_scale)

        draw_rect = pygame.Rect(0, 0, width, height)
        draw_rect.center = self.button_rect.center

        self.draw_pixel_rect(
            screen,
            draw_rect,
            button_color,
            (105, 70, 40),
            shadow_color=(90, 60, 35)
        )

        if self.sell_icon is not None:
            icon_rect = self.sell_icon.get_rect(center=draw_rect.center)
            screen.blit(self.sell_icon, icon_rect)
        else:
            self.draw_fallback_sell_icon(screen, draw_rect.center)

    def draw_close_button(self, screen):
        close_rect = self.get_close_button_rect()

        self.draw_pixel_rect(
            screen,
            close_rect,
            (230, 100, 80),
            (105, 70, 40),
            shadow_color=(80, 45, 35)
        )

        x_text = self.font.render("X", True, (255, 245, 220))
        x_rect = x_text.get_rect(center=close_rect.center)
        screen.blit(x_text, x_rect)

    def draw_action_button(self, screen, rect, text, normal_color, hover_color, pop_timer):
        mouse_pos = pygame.mouse.get_pos()

        if rect.collidepoint(mouse_pos):
            fill_color = hover_color
        else:
            fill_color = normal_color

        pop_scale = 1.0

        if pop_timer > 0:
            pop_scale = 1.08

        width = int(rect.width * pop_scale)
        height = int(rect.height * pop_scale)

        draw_rect = pygame.Rect(0, 0, width, height)
        draw_rect.center = rect.center

        self.draw_pixel_rect(
            screen,
            draw_rect,
            fill_color,
            (105, 70, 40),
            shadow_color=(80, 55, 35)
        )

        label = self.font.render(text, True, (70, 45, 25))
        label_rect = label.get_rect(center=draw_rect.center)
        screen.blit(label, label_rect)

    def draw_section_title(self, screen, text, x, y):
        label = self.font.render(text, True, (70, 45, 25))
        screen.blit(label, (x, y))

    def draw_item_slot(self, screen, item, slot_rect, amount, selected=False):
        mouse_pos = pygame.mouse.get_pos()

        if selected:
            slot_color = (210, 235, 255)
        elif slot_rect.collidepoint(mouse_pos):
            slot_color = (255, 240, 200)
        else:
            slot_color = (255, 230, 185)

        self.draw_pixel_rect(
            screen,
            slot_rect,
            slot_color,
            (130, 90, 50),
            shadow_color=(100, 70, 45)
        )

        if item is not None and item.get("image") is not None:
            icon = item["image"]
            icon_rect = icon.get_rect(center=slot_rect.center)
            screen.blit(icon, icon_rect)

        amount_bg_rect = pygame.Rect(
            slot_rect.right - 24,
            slot_rect.bottom - 17,
            22,
            15
        )

        pygame.draw.rect(screen, (245, 218, 170), amount_bg_rect)
        pygame.draw.rect(screen, (105, 70, 40), amount_bg_rect, 1)

        amount_text = self.small_font.render(
            str(amount),
            True,
            (70, 45, 25)
        )

        amount_rect = amount_text.get_rect(center=amount_bg_rect.center)
        screen.blit(amount_text, amount_rect)

    def draw_inventory_items(self, screen, inventory):
        start_x, start_y = self.get_inventory_area_start()
        visible_items = inventory.get_visible_items()

        if len(visible_items) == 0:
            text = self.small_font.render(
                "Inventory is empty",
                True,
                (80, 55, 35)
            )
            screen.blit(text, (start_x, start_y + 15))
            return

        for visible_index, data in enumerate(visible_items):
            real_index, item = data

            if item["name"] not in self.sell_prices:
                continue

            col = visible_index % self.cols
            row = visible_index // self.cols

            x = start_x + col * (self.slot_size + self.gap)
            y = start_y + row * (self.slot_size + 58)

            slot_rect = pygame.Rect(
                x,
                y,
                self.slot_size,
                self.slot_size
            )

            self.draw_item_slot(
                screen,
                item,
                slot_rect,
                item["amount"]
            )

            name_text = self.small_font.render(
                item["name"],
                True,
                (60, 40, 20)
            )

            name_rect = name_text.get_rect(
                center=(slot_rect.centerx, slot_rect.bottom + 10)
            )

            screen.blit(name_text, name_rect)

            price = self.sell_prices.get(item["name"], 0)

            price_number_text = self.small_font.render(
                str(price),
                True,
                (90, 65, 35)
            )

            price_suffix_text = self.small_font.render(
                "/pcs",
                True,
                (90, 65, 35)
            )

            total_width = price_number_text.get_width()
            total_width += price_suffix_text.get_width()

            if self.price_coin_icon is not None:
                total_width += self.price_coin_icon_size + 4

            price_start_x = slot_rect.centerx - total_width // 2
            price_y = slot_rect.bottom + 24

            screen.blit(
                price_number_text,
                (price_start_x, price_y)
            )

            current_x = price_start_x + price_number_text.get_width() + 2

            if self.price_coin_icon is not None:
                coin_y = price_y + (
                    price_number_text.get_height() - self.price_coin_icon_size
                ) // 2

                screen.blit(
                    self.price_coin_icon,
                    (current_x, coin_y)
                )

                current_x += self.price_coin_icon_size + 2

            screen.blit(
                price_suffix_text,
                (current_x, price_y)
            )

    def draw_basket_items(self, screen, inventory):
        start_x, start_y = self.get_basket_area_start()
        basket_items = self.basket.get_items()

        if len(basket_items) == 0:
            text = self.small_font.render(
                "Selling cart is empty.",
                True,
                (80, 55, 35)
            )
            screen.blit(text, (start_x, start_y + 15))
            return

        for i, basket_item in enumerate(basket_items):
            item = inventory.get_item_by_name(basket_item.name)

            col = i % self.cols
            row = i // self.cols

            x = start_x + col * (self.slot_size + self.gap)
            y = start_y + row * (self.slot_size + 42)

            slot_rect = pygame.Rect(
                x,
                y,
                self.slot_size,
                self.slot_size
            )

            selected = basket_item.name in self.item_pop_timers

            self.draw_item_slot(
                screen,
                item,
                slot_rect,
                basket_item.amount,
                selected=selected
            )

            name_text = self.small_font.render(
                basket_item.name,
                True,
                (60, 40, 20)
            )

            name_rect = name_text.get_rect(
                center=(slot_rect.centerx, slot_rect.bottom + 10)
            )

            screen.blit(name_text, name_rect)

    def draw(self, screen, inventory):
        self.draw_button(screen)

        if not self.is_open:
            return

        overlay = pygame.Surface(
            (self.screen_width, self.screen_height),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 85))
        screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(
            self.panel_x,
            self.panel_y,
            self.panel_width,
            self.panel_height
        )

        self.draw_pixel_rect(
            screen,
            panel_rect,
            (245, 218, 170),
            (105, 70, 40),
            shadow_color=(85, 55, 35)
        )

        title = self.title_font.render("SELLING CART", True, (70, 45, 25))
        title_rect = title.get_rect(
            center=(self.panel_x + self.panel_width // 2, self.panel_y + 40)
        )
        screen.blit(title, title_rect)

        self.draw_close_button(screen)

        self.draw_section_title(
            screen,
            "Inventory Items",
            self.panel_x + 45,
            self.panel_y + 70
        )

        self.draw_inventory_items(screen, inventory)

        self.draw_section_title(
            screen,
            "Selling Cart",
            self.panel_x + 45,
            self.panel_y + 240
        )

        self.draw_basket_items(screen, inventory)

        total_text = self.font.render(
            "Total: " + str(self.get_total_price()) + " coin",
            True,
            (70, 45, 25)
        )

        screen.blit(
            total_text,
            (self.panel_x + 45, self.panel_y + self.panel_height - 48)
        )

        self.draw_action_button(
            screen,
            self.get_cancel_button_rect(),
            "Cancel",
            normal_color=(255, 220, 160),
            hover_color=(255, 235, 185),
            pop_timer=self.cancel_button_pop_timer
        )

        self.draw_action_button(
            screen,
            self.get_sell_button_rect(),
            "Sell",
            normal_color=(210, 235, 190),
            hover_color=(225, 250, 205),
            pop_timer=self.sell_button_pop_timer
        )