import pygame

class Colors:
    """Colores del juego"""
    BACKGROUND = (15, 25, 45)
    PRIMARY = (0, 200, 255)
    SECONDARY = (255, 50, 150)
    ACCENT = (255, 215, 0)
    TEXT = (255, 255, 255)
    BUTTON = (40, 120, 180)
    BUTTON_HOVER = (60, 160, 220)
    SUCCESS = (0, 255, 100)
    WARNING = (255, 150, 0)
    BLUE = (0, 100, 255)
    RED = (255, 50, 50)
    WHITE = (255, 255, 255)

class Button:
    """Botón interactivo para menús"""
    def __init__(self, x, y, width, height, text, color=Colors.BUTTON, hover_color=Colors.BUTTON_HOVER):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 36)
        self.text_surface = self.font.render(text, True, Colors.TEXT)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=12)
        pygame.draw.rect(screen, Colors.PRIMARY, self.rect, 3, border_radius=12)
        screen.blit(self.text_surface, self.text_rect)
        
    def is_hovered(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        self.current_color = self.color
        return False
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class InputBox:
    """Caja de entrada de texto"""
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = Colors.BUTTON
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, Colors.TEXT)
        self.active = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = Colors.BUTTON_HOVER if self.active else Colors.BUTTON
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 20:
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, Colors.TEXT)
        return False
        
    def draw(self, screen):
        bg_color = Colors.BUTTON_HOVER if self.active else Colors.BUTTON
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)
        
        border_color = Colors.PRIMARY if self.active else (100, 100, 100)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=8)
        
        screen.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2))
        
        if self.active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = self.rect.x + 15 + self.txt_surface.get_width() + 2
            pygame.draw.line(screen, Colors.PRIMARY, (cursor_x, self.rect.y + 10), (cursor_x, self.rect.y + self.rect.height - 10), 2)
