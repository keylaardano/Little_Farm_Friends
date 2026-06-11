class Camera:
    def __init__(self, screen_width, screen_height, map_width, map_height, zoom):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.map_width = map_width
        self.map_height = map_height

        self.min_zoom = self.get_cover_zoom()

        self.zoom = max(zoom, self.min_zoom)
        self.max_zoom = 2.5

        self.x = 0
        self.y = 0

        self.dragging = False
        self.last_mouse_pos = (0, 0)

        self.clamp()

    def get_cover_zoom(self):
        zoom_x = self.screen_width / self.map_width
        zoom_y = self.screen_height / self.map_height

        return max(zoom_x, zoom_y)

    def clamp(self):
        visible_width = self.screen_width / self.zoom
        visible_height = self.screen_height / self.zoom

        max_x = max(0, self.map_width - visible_width)
        max_y = max(0, self.map_height - visible_height)

        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))

    def handle_event(self, event, pygame):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.dragging = True
                self.last_mouse_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        if event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                last_x, last_y = self.last_mouse_pos

                dx = mouse_x - last_x
                dy = mouse_y - last_y

                self.x -= dx / self.zoom
                self.y -= dy / self.zoom

                self.last_mouse_pos = event.pos
                self.clamp()

        if event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            before_zoom_x = self.x + mouse_x / self.zoom
            before_zoom_y = self.y + mouse_y / self.zoom

            if event.y > 0:
                new_zoom = self.zoom + 0.1
            else:
                new_zoom = self.zoom - 0.1

            self.zoom = max(self.min_zoom, min(new_zoom, self.max_zoom))

            self.x = before_zoom_x - mouse_x / self.zoom
            self.y = before_zoom_y - mouse_y / self.zoom

            self.clamp()

    def update(self, pygame):
        keys = pygame.key.get_pressed()
        speed = 6 / self.zoom

        if keys[pygame.K_a]:
            self.x -= speed

        if keys[pygame.K_d]:
            self.x += speed

        if keys[pygame.K_w]:
            self.y -= speed

        if keys[pygame.K_s]:
            self.y += speed

        self.clamp()

    def center_on(self, target_x, target_y):
        self.x = target_x - (self.screen_width / self.zoom) / 2
        self.y = target_y - (self.screen_height / self.zoom) / 2
        self.clamp()