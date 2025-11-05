# import pygame
# import math
# import random
# from utils import Colors, Button, InputBox
# from leaderboard import Leaderboard
# from network_manager import NetworkManager

# # Constantes para el menú
# SCREEN_WIDTH = 1000
# SCREEN_HEIGHT = 700

# class Particle:
#     """Partículas para el fondo animado"""
#     def __init__(self, width, height):
#         self.x = random.randint(0, width)
#         self.y = random.randint(0, height)
#         self.size = random.randint(2, 5)
#         self.speed = random.uniform(0.5, 2)
#         self.color = random.choice([
#             (0, 200, 255),    # Azul
#             (255, 50, 150),   # Rosa
#             (255, 215, 0),    # Dorado
#             (100, 255, 200),  # Verde azulado
#             (255, 100, 50)    # Naranja
#         ])
#         self.angle = random.uniform(0, 2 * math.pi)
        
#     def update(self):
#         self.x += math.cos(self.angle) * self.speed
#         self.y += math.sin(self.angle) * self.speed
        
#         # Rebotar en los bordes
#         if self.x < 0 or self.x > SCREEN_WIDTH:
#             self.angle = math.pi - self.angle
#         if self.y < 0 or self.y > SCREEN_HEIGHT:
#             self.angle = -self.angle
            
#     def draw(self, screen):
#         pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# class ModernButton:
#     """Botón moderno con efectos hover - VERSIÓN CORREGIDA"""
#     def __init__(self, x, y, width, height, text, icon="", primary_color=(0, 200, 255), secondary_color=(255, 50, 150)):
#         self.rect = pygame.Rect(x, y, width, height)
#         self.text = text
#         self.icon = icon
#         self.primary_color = primary_color
#         self.secondary_color = secondary_color
#         self.current_color = primary_color
#         self.hover_progress = 0
#         self.glow_intensity = 0
        
#         # Fuentes CORREGIDAS - asegurar que se cargan correctamente
#         try:
#             self.font = pygame.font.Font(None, 32)
#             self.icon_font = pygame.font.Font(None, 40)
#         except:
#             # Fallback si hay problemas con la fuente
#             self.font = pygame.font.SysFont('arial', 32)
#             self.icon_font = pygame.font.SysFont('arial', 40)
        
#         # Pre-renderizar textos para mejor rendimiento
#         self.text_surface = self.font.render(text, True, (255, 255, 255))
#         if icon:
#             self.icon_surface = self.icon_font.render(icon, True, (255, 255, 255))
#         else:
#             self.icon_surface = None
            
#     def update(self, mouse_pos):
#         is_hovered = self.rect.collidepoint(mouse_pos)
        
#         # Animación suave del hover
#         if is_hovered:
#             self.hover_progress = min(1, self.hover_progress + 0.1)
#             self.glow_intensity = 15
#         else:
#             self.hover_progress = max(0, self.hover_progress - 0.1)
#             self.glow_intensity = max(0, self.glow_intensity - 1)
            
#         # Interpolar color
#         r = int(self.primary_color[0] * (1 - self.hover_progress) + self.secondary_color[0] * self.hover_progress)
#         g = int(self.primary_color[1] * (1 - self.hover_progress) + self.secondary_color[1] * self.hover_progress)
#         b = int(self.primary_color[2] * (1 - self.hover_progress) + self.secondary_color[2] * self.hover_progress)
#         self.current_color = (r, g, b)
        
#     def draw(self, screen):
#         # Efecto de glow
#         if self.glow_intensity > 0:
#             glow_surface = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
#             for i in range(10):
#                 alpha = int(self.glow_intensity * (10 - i) / 10)
#                 radius = 10 + i
#                 pygame.draw.rect(glow_surface, (*self.current_color, alpha), 
#                                (10 - i, 10 - i, self.rect.width + 2*i, self.rect.height + 2*i), 
#                                border_radius=15, width=2)
#             screen.blit(glow_surface, (self.rect.x - 10, self.rect.y - 10))
        
#         # Botón principal
#         pygame.draw.rect(screen, self.current_color, self.rect, border_radius=12)
#         pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=12)
        
#         # Sombra interior
#         shadow_rect = self.rect.inflate(-10, -10)
#         pygame.draw.rect(screen, (255, 255, 255, 30), shadow_rect, border_radius=8)
        
#         # Texto e icono - VERSIÓN CORREGIDA
#         if self.icon_surface:
#             # Calcular posición para centrar icono y texto
#             total_width = self.icon_surface.get_width() + self.text_surface.get_width() + 15
#             start_x = self.rect.centerx - total_width // 2
            
#             # Dibujar icono
#             icon_y = self.rect.centery - self.icon_surface.get_height() // 2
#             screen.blit(self.icon_surface, (start_x, icon_y))
            
#             # Dibujar texto
#             text_y = self.rect.centery - self.text_surface.get_height() // 2
#             screen.blit(self.text_surface, (start_x + self.icon_surface.get_width() + 10, text_y))
#         else:
#             # Solo texto - centrado perfectamente
#             text_rect = self.text_surface.get_rect(center=self.rect.center)
#             screen.blit(self.text_surface, text_rect)
            
#     def is_clicked(self, pos, event):
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             return self.rect.collidepoint(pos)
#         return False

# class ModernInputBox:
#     """Input box moderno - VERSIÓN CORREGIDA"""
#     def __init__(self, x, y, width, height, text=''):
#         self.rect = pygame.Rect(x, y, width, height)
#         self.text = text
#         try:
#             self.font = pygame.font.Font(None, 32)
#         except:
#             self.font = pygame.font.SysFont('arial', 32)
#         self.txt_surface = self.font.render(text, True, (255, 255, 255))
#         self.active = False
#         self.hover_progress = 0
        
#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             self.active = self.rect.collidepoint(event.pos)
#         if event.type == pygame.KEYDOWN:
#             if self.active:
#                 if event.key == pygame.K_RETURN:
#                     return True
#                 elif event.key == pygame.K_BACKSPACE:
#                     self.text = self.text[:-1]
#                 else:
#                     if len(self.text) < 15:
#                         self.text += event.unicode
#                 self.txt_surface = self.font.render(self.text, True, (255, 255, 255))
#         return False
        
#     def update(self, mouse_pos):
#         is_hovered = self.rect.collidepoint(mouse_pos)
#         if is_hovered:
#             self.hover_progress = min(1, self.hover_progress + 0.1)
#         else:
#             self.hover_progress = max(0, self.hover_progress - 0.1)
        
#     def draw(self, screen):
#         # Fondo con gradiente según hover
#         r = int(40 + 20 * self.hover_progress)
#         g = int(120 + 40 * self.hover_progress)
#         b = int(180 + 40 * self.hover_progress)
        
#         pygame.draw.rect(screen, (r, g, b), self.rect, border_radius=8)
        
#         # Borde con efecto glow si está activo
#         border_color = (0, 200, 255) if self.active else (100, 100, 100)
#         pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=8)
        
#         # Texto - CORREGIDO: mejor posicionamiento
#         text_x = self.rect.x + 15
#         text_y = self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2
#         screen.blit(self.txt_surface, (text_x, text_y))
        
#         # Cursor parpadeante si está activo
#         if self.active and pygame.time.get_ticks() % 1000 < 500:
#             cursor_x = text_x + self.txt_surface.get_width()
#             pygame.draw.line(screen, (255, 255, 255), 
#                            (cursor_x, self.rect.y + 10),
#                            (cursor_x, self.rect.y + self.rect.height - 10), 2)

# class ModernMenu:
#     def __init__(self, screen):
#         self.screen = screen
#         self.WIDTH, self.HEIGHT = screen.get_size()
#         self.leaderboard = Leaderboard()
#         self.network = NetworkManager()
        
#         # Partículas de fondo
#         self.particles = [Particle(self.WIDTH, self.HEIGHT) for _ in range(50)]
        
#         # Efectos de animación
#         self.time = 0
#         self.title_glow = 0
#         self.title_direction = 1
        
#         # Estados
#         self.current_screen = "main"
#         self.connection_status = ""
        
#         # Crear elementos de UI
#         self.create_ui_elements()
        
#     def create_ui_elements(self):
#         """Crea todos los elementos de la interfaz"""
#         button_width, button_height = 400, 70
#         center_x = self.WIDTH // 2 - button_width // 2
        
#         # Botones principales con colores vibrantes
#         self.main_buttons = [
#             ModernButton(center_x, 300, button_width, button_height, "SOLO vs IA", "🎮", 
#                         (0, 100, 200), (0, 150, 255)),
#             ModernButton(center_x, 390, button_width, button_height, "PARTIDA ONLINE", "🌐", 
#                         (200, 50, 100), (255, 80, 120)),
#             ModernButton(center_x, 480, button_width, button_height, "CLASIFICACIÓN", "🏆", 
#                         (50, 180, 100), (80, 220, 120)),
#             ModernButton(center_x, 570, button_width, button_height, "SALIR", "❌", 
#                         (150, 50, 50), (200, 80, 80))
#         ]
        
#         # Botones de red
#         self.network_buttons = [
#             ModernButton(center_x, 320, button_width, button_height, "CREAR PARTIDA", "🖥️",
#                         (0, 100, 200), (0, 150, 255)),
#             ModernButton(center_x, 410, button_width, button_height, "UNIRSE A PARTIDA", "🔗",
#                         (200, 50, 100), (255, 80, 120)),
#             ModernButton(center_x, 500, button_width, button_height, "VOLVER AL MENÚ", "🔙",
#                         (100, 100, 150), (150, 150, 200))
#         ]
        
#         # Input moderno
#         self.ip_input = ModernInputBox(center_x, 370, button_width, 60, "192.168.1.")

#     def draw_animated_background(self):
#         """Dibuja el fondo animado con partículas y efectos"""
#         # Fondo gradiente animado más oscuro para mejor contraste
#         for y in range(self.HEIGHT):
#             time_factor = math.sin(self.time * 0.5) * 0.1 + 0.9
#             r = int(15 * time_factor + 10 * (y / self.HEIGHT))
#             g = int(25 * time_factor + 15 * (y / self.HEIGHT))
#             b = int(45 * time_factor + 20 * (y / self.HEIGHT))
#             pygame.draw.line(self.screen, (r, g, b), (0, y), (self.WIDTH, y))
        
#         # Dibujar partículas
#         for particle in self.particles:
#             particle.update()
#             particle.draw(self.screen)
            
#         # Efecto de scanning beam más sutil
#         scan_y = (math.sin(self.time * 2) * 0.5 + 0.5) * self.HEIGHT
#         scan_surface = pygame.Surface((self.WIDTH, 100), pygame.SRCALPHA)
#         for i in range(100):
#             alpha = int(20 * (1 - abs(i - 50) / 50))
#             pygame.draw.line(scan_surface, (255, 255, 255, alpha), (0, i), (self.WIDTH, i))
#         self.screen.blit(scan_surface, (0, scan_y - 50))

#     def draw_main_menu(self):
#         """Dibuja el menú principal moderno"""
#         self.draw_animated_background()
        
#         # Título principal con efectos
#         self.draw_animated_title()
        
#         # Subtítulo
#         try:
#             subtitle_font = pygame.font.Font(None, 28)
#         except:
#             subtitle_font = pygame.font.SysFont('arial', 28)
#         subtitle = subtitle_font.render("Control por Gestos • Física Avanzada • Multijugador", True, (180, 180, 255))
#         self.screen.blit(subtitle, (self.WIDTH//2 - subtitle.get_width()//2, 220))
        
#         # Dibujar botones
#         mouse_pos = pygame.mouse.get_pos()
#         for button in self.main_buttons:
#             button.update(mouse_pos)
#             button.draw(self.screen)
            
#         # Información inferior
#         self.draw_footer_info()

#     def draw_animated_title(self):
#         """Dibuja el título con animaciones - VERSIÓN CORREGIDA"""
#         try:
#             title_font = pygame.font.Font(None, 80)
#             glow_font = pygame.font.Font(None, 82)
#         except:
#             title_font = pygame.font.SysFont('arial', 80)
#             glow_font = pygame.font.SysFont('arial', 82)
        
#         # Efecto de glow pulsante
#         self.title_glow += 0.05 * self.title_direction
#         if self.title_glow > 10 or self.title_glow < 0:
#             self.title_direction *= -1
            
#         # Texto principal sólido y visible
#         title_text = "PING PONG PRO"
#         title_surface = title_font.render(title_text, True, (255, 255, 255))
#         title_rect = title_surface.get_rect(center=(self.WIDTH//2, 150))
        
#         # Sombra para mejor legibilidad
#         shadow_surface = title_font.render(title_text, True, (0, 0, 0))
#         self.screen.blit(shadow_surface, (title_rect.x + 3, title_rect.y + 3))
        
#         # Efecto de glow
#         for i in range(int(self.title_glow)):
#             alpha = 10 - i
#             glow_surface = glow_font.render(title_text, True, (0, 150, 255, alpha))
#             glow_rect = glow_surface.get_rect(center=(self.WIDTH//2, 150))
#             self.screen.blit(glow_surface, glow_rect)
        
#         # Texto principal
#         self.screen.blit(title_surface, title_rect)

#     def draw_network_menu(self):
#         """Dibuja el menú de red moderno"""
#         self.draw_animated_background()
        
#         try:
#             title_font = pygame.font.Font(None, 60)
#         except:
#             title_font = pygame.font.SysFont('arial', 60)
            
#         title = title_font.render("PARTIDA ONLINE", True, (0, 200, 255))
#         title_rect = title.get_rect(center=(self.WIDTH//2, 120))
        
#         # Sombra del título
#         shadow = title_font.render("PARTIDA ONLINE", True, (0, 0, 0))
#         self.screen.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
#         self.screen.blit(title, title_rect)
        
#         # Contenido según pantalla
#         mouse_pos = pygame.mouse.get_pos()
        
#         if self.current_screen == "join_game":
#             self.draw_join_game_screen(mouse_pos)
#         else:
#             self.draw_network_options(mouse_pos)
            
#         self.draw_footer_info()

#     def draw_join_game_screen(self, mouse_pos):
#         """Dibuja la pantalla de unirse a partida"""
#         try:
#             instruction_font = pygame.font.Font(None, 28)
#         except:
#             instruction_font = pygame.font.SysFont('arial', 28)
            
#         instruction = instruction_font.render("Ingresa la IP del servidor:", True, (200, 200, 255))
#         self.screen.blit(instruction, (self.WIDTH//2 - instruction.get_width()//2, 300))
        
#         # Input de IP
#         self.ip_input.update(mouse_pos)
#         self.ip_input.draw(self.screen)
        
#         # Botón conectar
#         connect_button = ModernButton(self.WIDTH//2 - 200, 450, 400, 60, "CONECTAR AL SERVIDOR", "🚀",
#                                     (0, 180, 100), (0, 220, 150))
#         connect_button.update(mouse_pos)
#         connect_button.draw(self.screen)
        
#         # Estado de conexión
#         if self.connection_status:
#             status_font = pygame.font.Font(None, 24) if hasattr(pygame.font, 'Font') else pygame.font.SysFont('arial', 24)
#             status_color = (0, 255, 100) if "conectado" in self.connection_status.lower() else (255, 100, 100)
#             status_text = status_font.render(self.connection_status, True, status_color)
#             self.screen.blit(status_text, (self.WIDTH//2 - status_text.get_width()//2, 530))

#     def draw_network_options(self, mouse_pos):
#         """Dibuja las opciones de red"""
#         try:
#             instruction_font = pygame.font.Font(None, 28)
#         except:
#             instruction_font = pygame.font.SysFont('arial', 28)
            
#         instruction = instruction_font.render("Selecciona una opción para jugar online:", True, (200, 200, 255))
#         self.screen.blit(instruction, (self.WIDTH//2 - instruction.get_width()//2, 200))
        
#         for button in self.network_buttons:
#             button.update(mouse_pos)
#             button.draw(self.screen)

#     def draw_footer_info(self):
#         """Dibuja la información del footer"""
#         try:
#             version_font = pygame.font.Font(None, 18)
#         except:
#             version_font = pygame.font.SysFont('arial', 18)
        
#         # Versión
#         version = version_font.render("v2.0 - Física Avanzada • Control por Gestos • Multijugador", True, (150, 150, 200))
#         self.screen.blit(version, (20, self.HEIGHT - 25))
        
#         # Controles
#         controls = version_font.render("ESC: Menú • F: Física • G: Gestos/Teclado", True, (150, 150, 200))
#         self.screen.blit(controls, (self.WIDTH - controls.get_width() - 20, self.HEIGHT - 25))

#     def update(self):
#         """Actualiza las animaciones"""
#         self.time += 0.016  # Aprox 60 FPS
        
#         # Actualizar partículas
#         for particle in self.particles:
#             particle.update()
            
#         return self.handle_events()

#     def handle_events(self):
#         """Maneja los eventos del menú"""
#         mouse_pos = pygame.mouse.get_pos()
        
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 return "quit"
                
#             if self.current_screen == "main":
#                 for i, button in enumerate(self.main_buttons):
#                     if button.is_clicked(mouse_pos, event):
#                         if i == 0:  # Solo vs IA
#                             return "start_solo"
#                         elif i == 1:  # Partida Online
#                             self.current_screen = "network"
#                         elif i == 2:  # Clasificación
#                             self.current_screen = "leaderboard"
#                         elif i == 3:  # Salir
#                             return "quit"
                            
#             elif self.current_screen == "network":
#                 for i, button in enumerate(self.network_buttons):
#                     if button.is_clicked(mouse_pos, event):
#                         if i == 0:  # Crear partida
#                             if self.network.start_server():
#                                 self.connection_status = "✅ Servidor creado. Esperando jugadores..."
#                                 return "start_host"
#                             else:
#                                 self.connection_status = "❌ Error al crear el servidor"
#                         elif i == 1:  # Unirse
#                             self.current_screen = "join_game"
#                         elif i == 2:  # Volver
#                             self.current_screen = "main"
                            
#             elif self.current_screen == "join_game":
#                 if hasattr(self, 'ip_input'):
#                     if self.ip_input.handle_event(event):
#                         self.attempt_connection()
                        
#         return "continue"

#     def attempt_connection(self):
#         """Intenta conectarse al servidor"""
#         if hasattr(self.ip_input, 'text') and self.ip_input.text.strip():
#             if self.network.connect_to_server(self.ip_input.text.strip()):
#                 self.connection_status = "✅ Conectado al servidor exitosamente!"
#                 return "start_client"
#             else:
#                 self.connection_status = "❌ Error conectando al servidor. Verifica la IP."
#         else:
#             self.connection_status = "⚠️ Ingresa una dirección IP válida"
#         return "continue"

#     def draw(self):
#         """Dibuja la pantalla actual"""
#         if self.current_screen == "main":
#             self.draw_main_menu()
#         elif self.current_screen == "network":
#             self.draw_network_menu()
#         elif self.current_screen == "leaderboard":
#             self.leaderboard.draw(self.screen)
#             # Botón volver moderno
#             back_button = ModernButton(self.WIDTH//2 - 100, self.HEIGHT - 80, 200, 50, "VOLVER", "🔙")
#             mouse_pos = pygame.mouse.get_pos()
#             back_button.update(mouse_pos)
#             back_button.draw(self.screen)