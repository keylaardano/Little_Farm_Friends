import pygame


class MenuBar:
    def __init__(self, screen_width, screen_height, level_system=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_system = level_system

        self.is_open = False
        self.selected_index = None

        self.font = pygame.font.SysFont(None, 20)
        self.label_font = pygame.font.SysFont(None, 17)
        self.lock_font = pygame.font.SysFont(None, 18)

        self.message = None

        self.menu_lift = 0

        self.button_size = 64
        self.button_rect = pygame.Rect(
            24,
            screen_height - self.button_size - 24 - self.menu_lift,
            self.button_size,
            self.button_size
        )

        self.button_pop_timer = 0
        self.button_pop_duration = 8

        self.slot_size = 54
        self.icon_size = 28
        self.gap = 14

        self.panel_width = 560
        self.panel_height = 145

        self.panel_x = (screen_width - self.panel_width) // 2
        self.panel_y_open = screen_height - self.panel_height - 18 - self.menu_lift
        self.panel_y_closed = screen_height + 20
        self.current_panel_y = self.panel_y_closed

        self.slide_speed = 34

        self.scroll_x = 0
        self.target_scroll_x = 0
        self.scroll_speed = 0.22

        self.items = [
            {
                "name": "Shovel",
                "path": "menu_bar/shovel.png",
                "type": "tool",
                "required_level": 1
            },
            {
                "name": "Weapon",
                "path": "menu_bar/weapon.png",
                "type": "weapon",
                "required_level": 3
            },
            {
                "name": "Carrot",
                "path": "menu_bar/carrot.png",
                "type": "crop",
                "price": 5,
                "required_level": 1
            },
            {
                "name": "Cabbage",
                "path": "menu_bar/cabbage.png",
                "type": "crop",
                "price": 10,
                "required_level": 2
            },
            {
                "name": "Strawberry",
                "path": "menu_bar/strawberry.png",
                "type": "crop",
                "price": 20,
                "required_level": 3
            },
            {
                "name": "Pumpkin",
                "path": "menu_bar/pumpkin.png",
                "type": "crop",
                "price": 40,
                "required_level": 4
            },
            {
                "name": "Chicken Feed",
                "path": "menu_bar/chicken_feed.png",
                "type": "chicken_feed",
                "price": 10,
                "required_level": 3
            },
            {
                "name": "Cows Feed",
                "path": "menu_bar/cows_feed.png",
                "type": "cows_feed",
                "price": 20,
                "required_level": 4
            }
        ]

        self.item_pop_timers = [0 for _ in self.items]

        self.load_images()
        self.load_coin_image()
        self.load_lock_image()

    def load_images(self):
        for item in self.items:
            image = pygame.image.load(item["path"]).convert_alpha()
            image = pygame.transform.scale(
                image,
                (self.icon_size, self.icon_size)
            )
            item["image"] = image

    def load_coin_image(self):
        self.coin_image = pygame.image.load("menu_bar/coin.png").convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (14, 14))

    def load_lock_image(self):
        self.lock_image = pygame.image.load("menu_bar/lock.png").convert_alpha()
        self.lock_image = pygame.transform.scale(self.lock_image, (20, 20))

    def consume_message(self):
        message = self.message
        self.message = None
        return message

    def is_item_unlocked(self, item):
        if self.level_system is None:
            return True

        item_name = item["name"]
        return self.level_system.is_item_unlocked(item_name)

    def get_locked_message(self, item):
        required_level = item.get("required_level", 1)
        return f"{item['name']} unlocks at Level {required_level}"

    def get_panel_rect(self):
        return pygame.Rect(
            self.panel_x,
            self.current_panel_y,
            self.panel_width,
            self.panel_height
        )

    def get_viewport_rect(self):
        panel_rect = self.get_panel_rect()

        return pygame.Rect(
            panel_rect.x + 38,
            panel_rect.y + 8,
            panel_rect.width - 76,
            panel_rect.height - 16
        )

    def get_left_scroll_rect(self):
        panel_rect = self.get_panel_rect()

        return pygame.Rect(
            panel_rect.x + 8,
            panel_rect.y + 44,
            24,
            36
        )

    def get_right_scroll_rect(self):
        panel_rect = self.get_panel_rect()

        return pygame.Rect(
            panel_rect.right - 32,
            panel_rect.y + 44,
            24,
            36
        )

    def get_content_width(self):
        if len(self.items) == 0:
            return 0

        return (
            len(self.items) * self.slot_size +
            (len(self.items) - 1) * self.gap
        )

    def get_max_scroll(self):
        viewport_rect = self.get_viewport_rect()
        content_width = self.get_content_width()

        return max(0, content_width - (viewport_rect.width - 20))

    def get_page_scroll_amount(self):
        viewport_rect = self.get_viewport_rect()
        return viewport_rect.width - 40

    def clamp_target_scroll(self):
        max_scroll = self.get_max_scroll()

        if self.target_scroll_x < 0:
            self.target_scroll_x = 0
        elif self.target_scroll_x > max_scroll:
            self.target_scroll_x = max_scroll

    def clamp_scroll(self):
        max_scroll = self.get_max_scroll()

        if self.scroll_x < 0:
            self.scroll_x = 0
        elif self.scroll_x > max_scroll:
            self.scroll_x = max_scroll

    def scroll_left(self):
        self.target_scroll_x -= self.get_page_scroll_amount()
        self.clamp_target_scroll()

    def scroll_right(self):
        self.target_scroll_x += self.get_page_scroll_amount()
        self.clamp_target_scroll()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                if self.button_rect.collidepoint(mouse_pos):
                    self.is_open = not self.is_open
                    self.button_pop_timer = self.button_pop_duration

                elif self.is_open:
                    if self.get_left_scroll_rect().collidepoint(mouse_pos):
                        self.scroll_left()

                    elif self.get_right_scroll_rect().collidepoint(mouse_pos):
                        self.scroll_right()

                    else:
                        self.check_item_click(mouse_pos)

    def select_item(self, index):
        if 0 <= index < len(self.items):
            item = self.items[index]

            if not self.is_item_unlocked(item):
                self.selected_index = None
                self.item_pop_timers[index] = 8
                self.message = self.get_locked_message(item)
                return

            if self.selected_index == index:
                self.selected_index = None
                self.item_pop_timers[index] = 8
            else:
                self.selected_index = index
                self.item_pop_timers[index] = 8

    def check_item_click(self, mouse_pos):
        viewport_rect = self.get_viewport_rect()

        start_x = viewport_rect.x + 10 - self.scroll_x
        slot_y = viewport_rect.y + 2

        for i, item in enumerate(self.items):
            slot_x = start_x + i * (self.slot_size + self.gap)

            slot_rect = pygame.Rect(
                slot_x,
                slot_y,
                self.slot_size,
                self.slot_size
            )

            if slot_rect.collidepoint(mouse_pos):
                self.select_item(i)
                break

    def update(self):
        if self.is_open:
            target_y = self.panel_y_open
        else:
            target_y = self.panel_y_closed

        if self.current_panel_y < target_y:
            self.current_panel_y += self.slide_speed

            if self.current_panel_y > target_y:
                self.current_panel_y = target_y

        elif self.current_panel_y > target_y:
            self.current_panel_y -= self.slide_speed

            if self.current_panel_y < target_y:
                self.current_panel_y = target_y

        if self.button_pop_timer > 0:
            self.button_pop_timer -= 1

        for i in range(len(self.item_pop_timers)):
            if self.item_pop_timers[i] > 0:
                self.item_pop_timers[i] -= 1

        difference = self.target_scroll_x - self.scroll_x

        if abs(difference) < 0.5:
            self.scroll_x = self.target_scroll_x
        else:
            self.scroll_x += difference * self.scroll_speed

        self.clamp_scroll()

    def draw(self, screen):
        self.draw_button(screen)

        if self.current_panel_y < self.screen_height:
            self.draw_panel(screen)

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

    def draw_farmer_button_icon(self, screen, center):
        x, y = center

        icon_size = self.icon_size
        left = x - icon_size // 2
        top = y - icon_size // 2 - 2

        outline = (45, 35, 30)
        skin = (236, 191, 154)
        hair = (97, 58, 42)
        hair_dark = (73, 42, 31)
        shirt = (35, 148, 95)
        shirt_dark = (25, 110, 72)
        shirt_light = (65, 180, 122)

        pygame.draw.rect(screen, outline, pygame.Rect(left + 8, top + 5, 12, 11))
        pygame.draw.rect(screen, skin, pygame.Rect(left + 9, top + 6, 10, 9))

        pygame.draw.rect(screen, hair, pygame.Rect(left + 7, top + 3, 14, 5))
        pygame.draw.rect(screen, hair, pygame.Rect(left + 6, top + 5, 4, 6))
        pygame.draw.rect(screen, hair, pygame.Rect(left + 18, top + 5, 4, 6))

        pygame.draw.rect(screen, hair_dark, pygame.Rect(left + 10, top + 7, 2, 2))
        pygame.draw.rect(screen, hair_dark, pygame.Rect(left + 16, top + 7, 2, 2))
        pygame.draw.rect(screen, hair_dark, pygame.Rect(left + 8, top + 10, 2, 2))
        pygame.draw.rect(screen, hair_dark, pygame.Rect(left + 18, top + 10, 2, 2))

        pygame.draw.rect(screen, outline, pygame.Rect(left + 11, top + 11, 1, 1))
        pygame.draw.rect(screen, outline, pygame.Rect(left + 16, top + 11, 1, 1))

        pygame.draw.rect(screen, skin, pygame.Rect(left + 12, top + 16, 4, 2))

        pygame.draw.rect(screen, outline, pygame.Rect(left + 7, top + 18, 14, 7))
        pygame.draw.rect(screen, shirt, pygame.Rect(left + 8, top + 19, 12, 5))

        pygame.draw.rect(screen, outline, pygame.Rect(left + 5, top + 19, 3, 5))
        pygame.draw.rect(screen, shirt_dark, pygame.Rect(left + 6, top + 20, 2, 3))

        pygame.draw.rect(screen, outline, pygame.Rect(left + 20, top + 19, 3, 5))
        pygame.draw.rect(screen, shirt_dark, pygame.Rect(left + 20, top + 20, 2, 3))

        pygame.draw.rect(screen, shirt_light, pygame.Rect(left + 9, top + 20, 3, 2))

    def split_label(self, text):
        words = text.split()

        if len(words) <= 1:
            return [text]

        if len(words) == 2:
            return [words[0], words[1]]

        return [" ".join(words[:-1]), words[-1]]

    def draw_item_label(self, screen, text, center_x, top_y, locked=False):
        lines = self.split_label(text)

        if locked:
            color = (115, 105, 95)
        else:
            color = (60, 40, 20)

        if len(lines) == 1:
            surf = self.label_font.render(lines[0], True, color)
            rect = surf.get_rect(center=(center_x, top_y + 8))
            screen.blit(surf, rect)
            return 1

        surf1 = self.label_font.render(lines[0], True, color)
        surf2 = self.label_font.render(lines[1], True, color)

        rect1 = surf1.get_rect(center=(center_x, top_y + 4))
        rect2 = surf2.get_rect(center=(center_x, top_y + 18))

        screen.blit(surf1, rect1)
        screen.blit(surf2, rect2)

        return 2

    def draw_price_coin(self, screen, price, center_x, top_y, locked=False):
        if locked:
            text_color = (115, 105, 95)
        else:
            text_color = (70, 45, 25)

        price_text = self.label_font.render(
            str(price),
            True,
            text_color
        )

        coin_icon = self.coin_image.copy()

        if locked:
            coin_icon.set_alpha(120)
        else:
            coin_icon.set_alpha(255)

        gap = 4
        total_width = price_text.get_width() + gap + coin_icon.get_width()

        text_x = center_x - total_width // 2
        text_y = top_y

        coin_x = text_x + price_text.get_width() + gap
        coin_y = text_y + price_text.get_height() // 2 - coin_icon.get_height() // 2

        screen.blit(price_text, (text_x, text_y))
        screen.blit(coin_icon, (coin_x, coin_y))

    def draw_scroll_button(self, screen, rect, direction, enabled):
        if enabled:
            fill = (240, 210, 150)
            border = (105, 70, 40)
            arrow_color = (70, 45, 25)
        else:
            fill = (210, 190, 160)
            border = (130, 110, 90)
            arrow_color = (120, 100, 85)

        self.draw_pixel_rect(screen, rect, fill, border)

        cx, cy = rect.center

        if direction == "left":
            points = [
                (cx + 4, cy - 9),
                (cx - 5, cy),
                (cx + 4, cy + 9)
            ]
        else:
            points = [
                (cx - 4, cy - 9),
                (cx + 5, cy),
                (cx - 4, cy + 9)
            ]

        pygame.draw.polygon(screen, arrow_color, points)

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

        self.draw_farmer_button_icon(screen, draw_rect.center)

    def draw_panel(self, screen):
        panel_rect = self.get_panel_rect()

        self.draw_pixel_rect(
            screen,
            panel_rect,
            (245, 218, 170),
            (105, 70, 40),
            shadow_color=(85, 55, 35)
        )

        max_scroll = self.get_max_scroll()

        can_scroll_left = self.scroll_x > 0
        can_scroll_right = self.scroll_x < max_scroll

        self.draw_scroll_button(
            screen,
            self.get_left_scroll_rect(),
            "left",
            can_scroll_left
        )

        self.draw_scroll_button(
            screen,
            self.get_right_scroll_rect(),
            "right",
            can_scroll_right
        )

        self.draw_items(screen)

    def draw_lock_icon(self, screen, slot_rect):
        lock_rect = self.lock_image.get_rect(
            center=(
                slot_rect.right - 11,
                slot_rect.y + 11
            )
        )

        screen.blit(self.lock_image, lock_rect)

    def draw_locked_overlay(self, screen, slot_rect):
        overlay = pygame.Surface(
            (slot_rect.width, slot_rect.height),
            pygame.SRCALPHA
        )

        overlay.fill((90, 90, 90, 120))

        screen.blit(
            overlay,
            (slot_rect.x, slot_rect.y)
        )

        self.draw_lock_icon(screen, slot_rect)

    def draw_items(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        viewport_rect = self.get_viewport_rect()

        start_x = viewport_rect.x + 10 - self.scroll_x
        slot_y = viewport_rect.y + 2

        old_clip = screen.get_clip()
        screen.set_clip(viewport_rect)

        for i, item in enumerate(self.items):
            slot_x = start_x + i * (self.slot_size + self.gap)

            base_slot_rect = pygame.Rect(
                slot_x,
                slot_y,
                self.slot_size,
                self.slot_size
            )

            unlocked = self.is_item_unlocked(item)

            pop_scale = 1.0

            if self.item_pop_timers[i] > 0:
                pop_scale = 1.08

            slot_width = int(self.slot_size * pop_scale)
            slot_height = int(self.slot_size * pop_scale)

            slot_rect = pygame.Rect(0, 0, slot_width, slot_height)
            slot_rect.center = base_slot_rect.center

            if not unlocked:
                slot_color = (205, 195, 180)
            elif self.selected_index == i:
                slot_color = (210, 235, 255)
            elif base_slot_rect.collidepoint(mouse_pos):
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

            icon = item["image"]

            if self.item_pop_timers[i] > 0:
                icon_size = int(self.icon_size * 1.12)
                icon = pygame.transform.scale(
                    item["image"],
                    (icon_size, icon_size)
                )

            icon_rect = icon.get_rect(center=slot_rect.center)
            screen.blit(icon, icon_rect)

            if not unlocked:
                self.draw_locked_overlay(screen, slot_rect)

            number_text = self.font.render(
                str(i + 1),
                True,
                (70, 45, 25) if unlocked else (120, 110, 100)
            )

            screen.blit(
                number_text,
                (base_slot_rect.x + 5, base_slot_rect.y + 3)
            )

            label_top_y = base_slot_rect.bottom + 5

            total_label_lines = self.draw_item_label(
                screen,
                item["name"],
                base_slot_rect.centerx,
                label_top_y,
                locked=not unlocked
            )

            if "price" in item:
                if total_label_lines == 1:
                    price_y = label_top_y + 22
                else:
                    price_y = label_top_y + 34

                self.draw_price_coin(
                    screen,
                    item["price"],
                    base_slot_rect.centerx,
                    price_y,
                    locked=not unlocked
                )

        screen.set_clip(old_clip)

    def get_selected_item(self):
        if self.selected_index is None:
            return None

        item = self.items[self.selected_index]

        if not self.is_item_unlocked(item):
            return None

        return item

    def get_selected_item_name(self):
        selected_item = self.get_selected_item()

        if selected_item is None:
            return None

        return selected_item["name"]

    def get_selected_item_type(self):
        selected_item = self.get_selected_item()

        if selected_item is None:
            return None

        return selected_item["type"]