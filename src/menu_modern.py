import pygame
import math
import random
from utils import Colors
from leaderboard import Leaderboard

# Constantes para el menú
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

class Particle:
    """Partículas para el fondo animado - VERSIÓN MEJORADA"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(0.5, 2)
        self.color = random.choice([
            (0, 200, 255),    # Azul
            (255, 50, 150),   # Rosa
            (255, 215, 0),    # Dorado
            (100, 255, 200),  # Verde azulado
            (255, 100, 50)    # Naranja
        ])
        self.angle = random.uniform(0, 2 * math.pi)
        
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        if self.x < 0 or self.x > self.width:
            self.angle = math.pi - self.angle
        if self.y < 0 or self.y > self.height:
            self.angle = -self.angle
            
        self.x = max(0, min(self.width, self.x))
        self.y = max(0, min(self.height, self.y))
            
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class ModernButton:
    """Botón moderno con efectos hover"""
    def __init__(self, x, y, width, height, text, icon="", primary_color=(0, 100, 200), secondary_color=(0, 150, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = icon
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.current_color = primary_color
        self.hover_progress = 0
        self.glow_intensity = 0
        
        try:
            font_size = max(24, int(28 * min(width/400, height/70)))
            icon_size = max(30, int(36 * min(width/400, height/70)))
            self.font = pygame.font.SysFont('segoeuiemoji', font_size)
            self.icon_font = pygame.font.SysFont('segoeuiemoji', icon_size)
        except:
            font_size = max(24, int(28 * min(width/400, height/70)))
            icon_size = max(30, int(36 * min(width/400, height/70)))
            self.font = pygame.font.Font(None, font_size)
            self.icon_font = pygame.font.Font(None, icon_size)
        
        self.text_surface = self.font.render(text, True, (255, 255, 255))
        
        if icon:
            self.icon_surface = self.icon_font.render(icon, True, (255, 255, 255))
        else:
            self.icon_surface = None
            
    def update(self, mouse_pos):
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        if is_hovered:
            self.hover_progress = min(1, self.hover_progress + 0.1)
            self.glow_intensity = 15
        else:
            self.hover_progress = max(0, self.hover_progress - 0.1)
            self.glow_intensity = max(0, self.glow_intensity - 1)
            
        r = int(self.primary_color[0] * (1 - self.hover_progress) + self.secondary_color[0] * self.hover_progress)
        g = int(self.primary_color[1] * (1 - self.hover_progress) + self.secondary_color[1] * self.hover_progress)
        b = int(self.primary_color[2] * (1 - self.hover_progress) + self.secondary_color[2] * self.hover_progress)
        
        self.current_color = (r, g, b)
        
    def draw(self, screen):
        if self.glow_intensity > 0:
            glow_surface = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
            for i in range(5):
                alpha = int(self.glow_intensity * (5 - i) / 5)
                pygame.draw.rect(glow_surface, (*self.current_color, alpha), 
                               (10 - i, 10 - i, self.rect.width + 2*i, self.rect.height + 2*i), 
                               border_radius=15, width=2)
            screen.blit(glow_surface, (self.rect.x - 10, self.rect.y - 10))
        
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=12)
        
        border_color = (min(255, self.current_color[0] + 50), 
                       min(255, self.current_color[1] + 50), 
                       min(255, self.current_color[2] + 50))
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=12)
        
        if self.icon_surface:
            total_width = self.icon_surface.get_width() + self.text_surface.get_width() + 15
            start_x = self.rect.centerx - total_width // 2
            
            icon_y = self.rect.centery - self.icon_surface.get_height() // 2
            screen.blit(self.icon_surface, (start_x, icon_y))
            
            text_y = self.rect.centery - self.text_surface.get_height() // 2
            screen.blit(self.text_surface, (start_x + self.icon_surface.get_width() + 10, text_y))
        else:
            text_rect = self.text_surface.get_rect(center=self.rect.center)
            screen.blit(self.text_surface, text_rect)
            
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class ModernMenu:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        
        self.scale_x = self.WIDTH / 1000
        self.scale_y = self.HEIGHT / 700
        self.scale_factor = min(self.scale_x, self.scale_y)
        
        self.leaderboard = Leaderboard()
        
        particle_count = max(20, int(50 * self.scale_x * self.scale_y))
        self.particles = [Particle(self.WIDTH, self.HEIGHT) for _ in range(particle_count)]
        
        self.time = 0
        self.title_glow = 0
        self.title_direction = 1
        
        self.current_screen = "main"
        
        self.create_ui_elements()
        
    def create_ui_elements(self):
        button_width = int(400 * self.scale_x)
        button_height = int(70 * self.scale_y)
        center_x = self.WIDTH // 2 - button_width // 2
        
        button_y_start = int(300 * self.scale_y)
        button_spacing = int(90 * self.scale_y)
        
        self.main_buttons = [
            ModernButton(center_x, button_y_start, button_width, button_height, "SOLO vs IA", "🎮", 
                        (0, 100, 200), (0, 150, 255)),
            ModernButton(center_x, button_y_start + button_spacing, button_width, button_height, "CLASIFICACIÓN", "🏆", 
                        (50, 180, 100), (80, 220, 120)),
            ModernButton(center_x, button_y_start + 2 * button_spacing, button_width, button_height, "SALIR", "❌", 
                        (150, 50, 50), (200, 80, 80))
        ]

    def draw_animated_background(self):
        self.screen.fill((15, 25, 45))
        
        for y in range(0, self.HEIGHT, 2):
            time_factor = math.sin(self.time * 0.5 + y * 0.01) * 0.1 + 0.9
            r = int(15 * time_factor + 10 * (y / self.HEIGHT))
            g = int(25 * time_factor + 15 * (y / self.HEIGHT))
            b = int(45 * time_factor + 20 * (y / self.HEIGHT))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.WIDTH, y))
        
        for particle in self.particles:
            particle.update()
            particle.draw(self.screen)
            
        scan_y = (math.sin(self.time * 2) * 0.5 + 0.5) * self.HEIGHT
        scan_height = int(100 * self.scale_y)
        scan_surface = pygame.Surface((self.WIDTH, scan_height), pygame.SRCALPHA)
        
        for i in range(scan_height):
            alpha = int(30 * (1 - abs(i - scan_height//2) / (scan_height//2)))
            pygame.draw.line(scan_surface, (255, 255, 255, alpha), 
                           (0, i), (self.WIDTH, i))
        
        self.screen.blit(scan_surface, (0, scan_y - scan_height//2))

    def draw_main_menu(self):
        self.draw_animated_background()
        self.draw_animated_title()
        
        try:
            subtitle_size = int(28 * self.scale_factor)
            subtitle_font = pygame.font.SysFont('segoeui', subtitle_size)
        except:
            subtitle_size = int(28 * self.scale_factor)
            subtitle_font = pygame.font.Font(None, subtitle_size)
        
        subtitle_text = "Control por Gestos • Física Avanzada"
        subtitle = subtitle_font.render(subtitle_text, True, (180, 180, 255))
        subtitle_x = self.WIDTH // 2 - subtitle.get_width() // 2
        subtitle_y = int(220 * self.scale_y)
        
        shadow = subtitle_font.render(subtitle_text, True, (0, 0, 0))
        self.screen.blit(shadow, (subtitle_x + 2, subtitle_y + 2))
        self.screen.blit(subtitle, (subtitle_x, subtitle_y))
        
        mouse_pos = pygame.mouse.get_pos()
        for button in self.main_buttons:
            button.update(mouse_pos)
            button.draw(self.screen)
            
        self.draw_footer_info()

    def draw_animated_title(self):
        title_font_size = int(80 * self.scale_factor)
        glow_font_size = int(82 * self.scale_factor)
        
        try:
            title_font = pygame.font.SysFont('segoeui', title_font_size)
            glow_font = pygame.font.SysFont('segoeui', glow_font_size)
        except:
            title_font = pygame.font.Font(None, title_font_size)
            glow_font = pygame.font.Font(None, glow_font_size)
        
        self.title_glow += 0.05 * self.title_direction
        if self.title_glow > 10 or self.title_glow < 0:
            self.title_direction *= -1
            
        title_text = "PING PONG PRO"
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.WIDTH//2, int(150 * self.scale_y)))
        
        shadow_surface = title_font.render(title_text, True, (0, 0, 0))
        self.screen.blit(shadow_surface, (title_rect.x + 3, title_rect.y + 3))
        
        for i in range(int(self.title_glow)):
            alpha = 10 - i
            glow_surface = glow_font.render(title_text, True, (0, 150, 255, alpha))
            glow_rect = glow_surface.get_rect(center=(self.WIDTH//2, int(150 * self.scale_y)))
            self.screen.blit(glow_surface, glow_rect)
        
        self.screen.blit(title_surface, title_rect)

    def draw_footer_info(self):
        try:
            footer_size = int(18 * self.scale_factor)
            version_font = pygame.font.SysFont('segoeui', footer_size)
        except:
            footer_size = int(18 * self.scale_factor)
            version_font = pygame.font.Font(None, footer_size)
        
        version_text = "v1.0 - Solo Edition"
        version = version_font.render(version_text, True, (150, 150, 200))
        self.screen.blit(version, (int(20 * self.scale_x), self.HEIGHT - int(25 * self.scale_y)))
        
        controls_text = "ESC: Menú • F: Física • G: Gestos/Teclado • C: Cámara"
        controls = version_font.render(controls_text, True, (150, 150, 200))
        self.screen.blit(controls, (self.WIDTH - controls.get_width() - int(20 * self.scale_x), self.HEIGHT - int(25 * self.scale_y)))

    def update(self, events):
        self.time += 0.016
        
        for particle in self.particles:
            particle.update()
            
        return self.handle_events(events)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_screen == "leaderboard":
                        self.current_screen = "main"
                    elif self.current_screen == "main":
                        return "quit"
            
            if self.current_screen == "main":
                for i, button in enumerate(self.main_buttons):
                    if button.is_clicked(mouse_pos, event):
                        if i == 0: return "start_solo"
                        elif i == 1: self.current_screen = "leaderboard"
                        elif i == 2: return "quit"
                            
            elif self.current_screen == "leaderboard":
                back_button_width = int(200 * self.scale_x)
                back_button_height = int(50 * self.scale_y)
                back_button = ModernButton(
                    self.WIDTH//2 - back_button_width//2, 
                    self.HEIGHT - int(80 * self.scale_y), 
                    back_button_width, back_button_height, "VOLVER", "🔙"
                )
                if back_button.is_clicked(mouse_pos, event):
                    self.current_screen = "main"
                
        return "continue"

    def draw(self):
        if self.current_screen == "main":
            self.draw_main_menu()
        elif self.current_screen == "leaderboard":
            self.draw_animated_background()
            self.leaderboard.draw(self.screen)
            
            back_button_width = int(200 * self.scale_x)
            back_button_height = int(50 * self.scale_y)
            back_button = ModernButton(
                self.WIDTH//2 - back_button_width//2, 
                self.HEIGHT - int(80 * self.scale_y), 
                back_button_width, back_button_height, "VOLVER", "🔙"
            )
            mouse_pos = pygame.mouse.get_pos()
            back_button.update(mouse_pos)
            back_button.draw(self.screen)
            
            self.draw_footer_info()

def create_responsive_menu(screen):
    return ModernMenu(screen)