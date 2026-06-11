import pygame

class Inventory:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.is_open = False
        self.selected_index = None

        self.font = pygame.font.SysFont(None, 20)
        self.small_font = pygame.font.SysFont(None, 18)
        self.title_font = pygame.font.SysFont(None, 32)

        self.button_size = 64
        self.button_margin_left = 24
        self.button_gap = 18

        self.button_rect = pygame.Rect(
            self.button_margin_left + self.button_size + self.button_gap,
            screen_height - self.button_size - 24,
            self.button_size,
            self.button_size
        )

        self.button_pop_timer = 0
        self.button_pop_duration = 8

        self.button_icon_path = "menu_bar/inventory.png"
        self.button_icon_size = 34
        self.button_icon = None

        self.panel_width = 560
        self.panel_height = 360
        self.panel_x = (screen_width - self.panel_width) // 2
        self.panel_y = (screen_height - self.panel_height) // 2

        self.slot_size = 58
        self.icon_size = 32
        self.gap = 18
        self.cols = 5

        self.item_pop_timers = []

        self.items = [
            {
                "name": "Cabbage",
                "path": "menu_bar/cabbage.png",
                "type": "crop",
                "amount": 0
            },
            {
                "name": "Carrot",
                "path": "menu_bar/carrot.png",
                "type": "crop",
                "amount": 0
            },
            {
                "name": "Pumpkin",
                "path": "menu_bar/pumpkin.png",
                "type": "crop",
                "amount": 0
            },
            {
                "name": "Strawberry",
                "path": "menu_bar/strawberry.png",
                "type": "crop",
                "amount": 0
            },
            {
                "name": "Egg",
                "path": "animal/Egg.png",
                "type": "animal_product",
                "amount": 0
            },
            {
                "name": "Milk",
                "path": "animal/Milk.png",
                "type": "animal_product",
                "amount": 0
            }
        ]

        self.item_pop_timers = [0 for _ in self.items]

        self.load_images()

    def load_images(self):
        try:
            button_icon = pygame.image.load(self.button_icon_path).convert_alpha()
            self.button_icon = pygame.transform.scale(
                button_icon,
                (self.button_icon_size, self.button_icon_size)
            )
        except:
            self.button_icon = None
            print("Gambar button inventory tidak ditemukan:", self.button_icon_path)

        for item in self.items:
            try:
                image = pygame.image.load(item["path"]).convert_alpha()
                image = pygame.transform.scale(
                    image,
                    (self.icon_size, self.icon_size)
                )
                item["image"] = image
            except:
                item["image"] = None
                print("Gambar inventory tidak ditemukan:", item["path"])

    def toggle(self):
        self.is_open = not self.is_open
        self.button_pop_timer = self.button_pop_duration

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                if self.button_rect.collidepoint(mouse_pos):
                    self.toggle()

                elif self.is_open:
                    if self.get_close_button_rect().collidepoint(mouse_pos):
                        self.is_open = False
                    else:
                        self.check_item_click(mouse_pos)

    def update(self):
        if self.button_pop_timer > 0:
            self.button_pop_timer -= 1

        for i in range(len(self.item_pop_timers)):
            if self.item_pop_timers[i] > 0:
                self.item_pop_timers[i] -= 1

    def get_close_button_rect(self):
        return pygame.Rect(
            self.panel_x + self.panel_width - 46,
            self.panel_y + 16,
            30,
            30
        )

    def get_visible_items(self):
        visible_items = []

        for i, item in enumerate(self.items):
            if item["amount"] > 0:
                visible_items.append((i, item))

        return visible_items

    def get_item_by_name(self, item_name):
        for item in self.items:
            if item["name"] == item_name:
                return item

        return None

    def get_item_amount(self, item_name):
        item = self.get_item_by_name(item_name)

        if item is None:
            return 0

        return item["amount"]

    def add_item(self, item_name, amount=1):
        for item in self.items:
            if item["name"] == item_name:
                item["amount"] += amount
                return True

        print("Item not found:", item_name)
        return False

    def remove_item(self, item_name, amount=1):
        item = self.get_item_by_name(item_name)

        if item is None:
            print("Item not found:", item_name)
            return False

        if item["amount"] < amount:
            print("Item's amount are not enough:", item_name)
            return False

        item["amount"] -= amount

        if item["amount"] < 0:
            item["amount"] = 0

        return True

    def check_item_click(self, mouse_pos):
        start_x = self.panel_x + 48
        start_y = self.panel_y + 95

        visible_items = self.get_visible_items()

        for visible_index, data in enumerate(visible_items):
            real_index, item = data

            col = visible_index % self.cols
            row = visible_index // self.cols

            x = start_x + col * (self.slot_size + self.gap)
            y = start_y + row * (self.slot_size + 45)

            slot_rect = pygame.Rect(
                x,
                y,
                self.slot_size,
                self.slot_size
            )

            if slot_rect.collidepoint(mouse_pos):
                self.selected_index = real_index
                self.item_pop_timers[real_index] = 8
                print("Inventory item dipilih:", item["name"])

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

    def draw_inventory_icon(self, screen, center):
        x, y = center

        pygame.draw.rect(
            screen,
            (150, 95, 55),
            pygame.Rect(x - 14, y - 3, 28, 24)
        )
        pygame.draw.rect(
            screen,
            (95, 60, 35),
            pygame.Rect(x - 14, y - 3, 28, 24),
            2
        )

        pygame.draw.rect(
            screen,
            (180, 120, 70),
            pygame.Rect(x - 10, y - 12, 20, 10)
        )
        pygame.draw.rect(
            screen,
            (95, 60, 35),
            pygame.Rect(x - 10, y - 12, 20, 10),
            2
        )

        pygame.draw.rect(
            screen,
            (220, 170, 90),
            pygame.Rect(x - 5, y - 18, 10, 6)
        )

        pygame.draw.rect(
            screen,
            (225, 180, 100),
            pygame.Rect(x - 3, y + 5, 6, 7)
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

        if self.button_icon is not None:
            icon_rect = self.button_icon.get_rect(
                center=(draw_rect.centerx, draw_rect.centery - 2)
            )
            screen.blit(self.button_icon, icon_rect)
        else:
            self.draw_inventory_icon(screen, draw_rect.center)

    def draw_item_label(self, screen, text, center_x, top_y):
        surf = self.small_font.render(text, True, (60, 40, 20))
        rect = surf.get_rect(center=(center_x, top_y + 8))
        screen.blit(surf, rect)

    def draw_placeholder_icon(self, screen, center):
        x, y = center

        pygame.draw.rect(
            screen,
            (210, 180, 130),
            pygame.Rect(x - 12, y - 12, 24, 24)
        )

        pygame.draw.line(
            screen,
            (100, 70, 40),
            (x - 10, y - 10),
            (x + 10, y + 10),
            2
        )

        pygame.draw.line(
            screen,
            (100, 70, 40),
            (x + 10, y - 10),
            (x - 10, y + 10),
            2
        )

    def draw(self, screen):
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

        title = self.title_font.render("INVENTORY", True, (70, 45, 25))
        title_rect = title.get_rect(
            center=(self.panel_x + self.panel_width // 2, self.panel_y + 40)
        )
        screen.blit(title, title_rect)

        self.draw_close_button(screen)
        self.draw_items(screen)

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

    def draw_items(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        visible_items = self.get_visible_items()

        start_x = self.panel_x + 48
        start_y = self.panel_y + 95

        if len(visible_items) == 0:
            empty_text = self.font.render(
                "Inventory still empty",
                True,
                (80, 55, 35)
            )
            empty_rect = empty_text.get_rect(
                center=(self.panel_x + self.panel_width // 2, self.panel_y + 190)
            )
            screen.blit(empty_text, empty_rect)
            return

        for visible_index, data in enumerate(visible_items):
            real_index, item = data

            col = visible_index % self.cols
            row = visible_index // self.cols

            x = start_x + col * (self.slot_size + self.gap)
            y = start_y + row * (self.slot_size + 45)

            base_slot_rect = pygame.Rect(
                x,
                y,
                self.slot_size,
                self.slot_size
            )

            pop_scale = 1.0

            if self.item_pop_timers[real_index] > 0:
                pop_scale = 1.08

            slot_width = int(self.slot_size * pop_scale)
            slot_height = int(self.slot_size * pop_scale)

            slot_rect = pygame.Rect(0, 0, slot_width, slot_height)
            slot_rect.center = base_slot_rect.center

            if self.selected_index == real_index:
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

            if item["image"] is not None:
                icon = item["image"]
                icon_rect = icon.get_rect(center=slot_rect.center)
                screen.blit(icon, icon_rect)
            else:
                self.draw_placeholder_icon(screen, slot_rect.center)

            amount_bg_rect = pygame.Rect(
                base_slot_rect.right - 24,
                base_slot_rect.bottom - 17,
                22,
                15
            )

            pygame.draw.rect(screen, (245, 218, 170), amount_bg_rect)
            pygame.draw.rect(screen, (105, 70, 40), amount_bg_rect, 1)

            amount_text = self.small_font.render(
                str(item["amount"]),
                True,
                (70, 45, 25)
            )

            amount_rect = amount_text.get_rect(center=amount_bg_rect.center)
            screen.blit(amount_text, amount_rect)

            self.draw_item_label(
                screen,
                item["name"],
                base_slot_rect.centerx,
                base_slot_rect.bottom + 7
            )

    def get_selected_item(self):
        if self.selected_index is None:
            return None

        return self.items[self.selected_index]

    def get_selected_item_name(self):
        selected_item = self.get_selected_item()

        if selected_item is None:
            return None

        return selected_item["name"]