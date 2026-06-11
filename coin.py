import pygame

class Coin:
    def __init__(self, starting_amount=50):
        self.amount = starting_amount

        self.font = pygame.font.SysFont(None, 24)

        self.x = 20
        self.y = 20
        self.width = 130
        self.height = 42

        
        self.coin_icon_size = 24
        self.coin_icon = self.load_coin_icon("menu_bar/coin.png")

    def load_coin_icon(self, path):
        try:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(
                image,
                (self.coin_icon_size, self.coin_icon_size)
            )
            return image

        except:
            print("Gambar coin tidak ditemukan:", path)
            return None

    def can_afford(self, price):
        return self.amount >= price

    def spend(self, price):
        if self.can_afford(price):
            self.amount -= price
            print("Coin berkurang:", price, "| Sisa coin:", self.amount)
            return True

        print("Coin tidak cukup. Butuh:", price, "| Coin kamu:", self.amount)
        return False

    def add(self, amount):
        self.amount += amount
        print("Coin bertambah:", amount, "| Total coin:", self.amount)

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

    def draw_fallback_coin_icon(self, screen, center):
        x, y = center

        pygame.draw.rect(
            screen,
            (230, 180, 70),
            pygame.Rect(x - 8, y - 8, 16, 16)
        )

        pygame.draw.rect(
            screen,
            (130, 90, 40),
            pygame.Rect(x - 8, y - 8, 16, 16),
            2
        )

        pygame.draw.rect(
            screen,
            (255, 220, 110),
            pygame.Rect(x - 4, y - 4, 8, 8)
        )

    def draw(self, screen):
        coin_rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

        self.draw_pixel_rect(
            screen,
            coin_rect,
            (245, 218, 170),
            (105, 70, 40),
            shadow_color=(85, 55, 35)
        )

        icon_center = (
            coin_rect.x + 24,
            coin_rect.centery
        )

        if self.coin_icon is not None:
            icon_rect = self.coin_icon.get_rect(center=icon_center)
            screen.blit(self.coin_icon, icon_rect)
        else:
            self.draw_fallback_coin_icon(screen, icon_center)

        text = self.font.render(
            str(self.amount),
            True,
            (70, 45, 25)
        )

        text_rect = text.get_rect(
            midleft=(coin_rect.x + 48, coin_rect.centery)
        )

        screen.blit(text, text_rect)