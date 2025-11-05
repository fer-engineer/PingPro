import pygame
import math
import random
from utils import Colors, Button, InputBox
from leaderboard import Leaderboard
from network_manager import NetworkManager

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
        
        # Rebotar en los bordes de la pantalla ACTUAL
        if self.x < 0:
            self.x = 0
            self.angle = math.pi - self.angle
        elif self.x > self.width:
            self.x = self.width
            self.angle = math.pi - self.angle
            
        if self.y < 0:
            self.y = 0
            self.angle = -self.angle
        elif self.y > self.height:
            self.y = self.height
            self.angle = -self.angle
            
        # Asegurar que las partículas se mantengan dentro de los límites
        self.x = max(0, min(self.width, self.x))
        self.y = max(0, min(self.height, self.y))
            
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class ModernButton:
    """Botón moderno con efectos hover - VERSIÓN CORREGIDA"""
    def __init__(self, x, y, width, height, text, icon="", primary_color=(0, 100, 200), secondary_color=(0, 150, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = icon
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.current_color = primary_color
        self.hover_progress = 0
        self.glow_intensity = 0
        
        # Fuentes mejoradas para mejor compatibilidad con emojis
        try:
            # Intentar cargar fuentes del sistema que soporten emojis
            font_size = max(24, int(28 * min(width/400, height/70)))
            icon_size = max(30, int(36 * min(width/400, height/70)))
            self.font = pygame.font.SysFont('segoeuiemoji', font_size)
            self.icon_font = pygame.font.SysFont('segoeuiemoji', icon_size)
        except:
            # Fallback a fuentes por defecto
            try:
                font_size = max(24, int(28 * min(width/400, height/70)))
                icon_size = max(30, int(36 * min(width/400, height/70)))
                self.font = pygame.font.SysFont('arial', font_size)
                self.icon_font = pygame.font.SysFont('arial', icon_size)
            except:
                font_size = max(24, int(28 * min(width/400, height/70)))
                icon_size = max(30, int(36 * min(width/400, height/70)))
                self.font = pygame.font.Font(None, font_size)
                self.icon_font = pygame.font.Font(None, icon_size)
        
        # CORRECCIÓN: Asegurarse de que ambas superficies existen
        self.text_surface = self.font.render(text, True, (255, 255, 255))
        
        if icon:
            self.icon_surface = self.icon_font.render(icon, True, (255, 255, 255))
        else:
            self.icon_surface = None
            
    def update(self, mouse_pos):
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Animación suave del hover
        if is_hovered:
            self.hover_progress = min(1, self.hover_progress + 0.1)
            self.glow_intensity = 15
        else:
            self.hover_progress = max(0, self.hover_progress - 0.1)
            self.glow_intensity = max(0, self.glow_intensity - 1)
            
        # Interpolar color
        r = int(self.primary_color[0] * (1 - self.hover_progress) + self.secondary_color[0] * self.hover_progress)
        g = int(self.primary_color[1] * (1 - self.hover_progress) + self.secondary_color[1] * self.hover_progress)
        b = int(self.primary_color[2] * (1 - self.hover_progress) + self.secondary_color[2] * self.hover_progress)
        
        self.current_color = (r, g, b)
        
    def draw(self, screen):
        # Efecto de glow
        if self.glow_intensity > 0:
            glow_surface = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
            for i in range(5):
                alpha = int(self.glow_intensity * (5 - i) / 5)
                pygame.draw.rect(glow_surface, (*self.current_color, alpha), 
                               (10 - i, 10 - i, self.rect.width + 2*i, self.rect.height + 2*i), 
                               border_radius=15, width=2)
            screen.blit(glow_surface, (self.rect.x - 10, self.rect.y - 10))
        
        # Botón principal
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=12)
        
        # Borde resaltado
        border_color = (min(255, self.current_color[0] + 50), 
                       min(255, self.current_color[1] + 50), 
                       min(255, self.current_color[2] + 50))
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=12)
        
        # CORRECCIÓN: Verificar que ambas superficies existen antes de dibujar
        if self.icon_surface:
            # Calcular posición para centrar icono y texto
            total_width = self.icon_surface.get_width() + self.text_surface.get_width() + 15
            start_x = self.rect.centerx - total_width // 2
            
            # Dibujar icono
            icon_y = self.rect.centery - self.icon_surface.get_height() // 2
            screen.blit(self.icon_surface, (start_x, icon_y))
            
            # Dibujar texto
            text_y = self.rect.centery - self.text_surface.get_height() // 2
            screen.blit(self.text_surface, (start_x + self.icon_surface.get_width() + 10, text_y))
        else:
            # Solo texto - centrado
            text_rect = self.text_surface.get_rect(center=self.rect.center)
            screen.blit(self.text_surface, text_rect)
            
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class ModernInputBox:
    """Input box moderno - VERSIÓN MEJORADA"""
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        try:
            font_size = max(24, int(30 * min(width/400, height/60)))
            self.font = pygame.font.SysFont('segoeui', font_size)
        except:
            font_size = max(24, int(30 * min(width/400, height/60)))
            self.font = pygame.font.Font(None, font_size)
        self.txt_surface = self.font.render(text, True, (255, 255, 255))
        self.active = False
        self.hover_progress = 0
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 15:
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, (255, 255, 255))
        return False
        
    def update(self, mouse_pos):
        is_hovered = self.rect.collidepoint(mouse_pos)
        if is_hovered:
            self.hover_progress = min(1, self.hover_progress + 0.1)
        else:
            self.hover_progress = max(0, self.hover_progress - 0.1)
        
    def draw(self, screen):
        # Fondo con gradiente según hover
        r = int(40 + 20 * self.hover_progress)
        g = int(120 + 40 * self.hover_progress)
        b = int(180 + 40 * self.hover_progress)
        
        pygame.draw.rect(screen, (r, g, b), self.rect, border_radius=8)
        
        # Borde con efecto glow si está activo
        border_color = (0, 200, 255) if self.active else (100, 100, 100)
        pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=8)
        
        # Texto - MEJORADO: mejor posicionamiento
        text_x = self.rect.x + 15
        text_y = self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2
        screen.blit(self.txt_surface, (text_x, text_y))
        
        # Cursor parpadeante si está activo
        if self.active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = text_x + self.txt_surface.get_width()
            pygame.draw.line(screen, (255, 255, 255), 
                           (cursor_x, self.rect.y + 10),
                           (cursor_x, self.rect.y + self.rect.height - 10), 2)

class ModernMenu:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        
        # Factores de escala
        self.scale_x = self.WIDTH / 1000
        self.scale_y = self.HEIGHT / 700
        self.scale_factor = min(self.scale_x, self.scale_y)
        
        self.leaderboard = Leaderboard()
        self.network = NetworkManager()
        
        # Partículas de fondo - cantidad escalada
        particle_count = max(20, int(50 * self.scale_x * self.scale_y))
        self.particles = [Particle(self.WIDTH, self.HEIGHT) for _ in range(particle_count)]
        
        # Efectos de animación
        self.time = 0
        self.title_glow = 0
        self.title_direction = 1
        
        # Estados
        self.current_screen = "main"
        self.connection_status = ""
        
        # Crear elementos de UI
        self.create_ui_elements()
        
    def create_ui_elements(self):
        """Crea todos los elementos de la interfaz escalados"""
        button_width = int(400 * self.scale_x)
        button_height = int(70 * self.scale_y)
        center_x = self.WIDTH // 2 - button_width // 2
        
        # Posiciones escaladas
        button_y_start = int(300 * self.scale_y)
        button_spacing = int(90 * self.scale_y)
        
        # MEJORA: Botones principales con iconos más visibles y mejor espaciado
        self.main_buttons = [
            ModernButton(center_x, button_y_start, button_width, button_height, "SOLO vs IA", "🎮", 
                        (0, 100, 200), (0, 150, 255)),
            ModernButton(center_x, button_y_start + button_spacing, button_width, button_height, "PARTIDA ONLINE", "🌐", 
                        (200, 50, 100), (255, 80, 120)),
            ModernButton(center_x, button_y_start + 2 * button_spacing, button_width, button_height, "CLASIFICACIÓN", "🏆", 
                        (50, 180, 100), (80, 220, 120)),
            ModernButton(center_x, button_y_start + 3 * button_spacing, button_width, button_height, "SALIR", "❌", 
                        (150, 50, 50), (200, 80, 80))
        ]
        
        # Botones de red con posiciones escaladas
        network_y_start = int(320 * self.scale_y)
        network_spacing = int(90 * self.scale_y)
        
        self.network_buttons = [
            ModernButton(center_x, network_y_start, button_width, button_height, "CREAR PARTIDA", "🖥️",
                        (0, 100, 200), (0, 150, 255)),
            ModernButton(center_x, network_y_start + network_spacing, button_width, button_height, "UNIRSE A PARTIDA", "🔗",
                        (200, 50, 100), (255, 80, 120)),
            ModernButton(center_x, network_y_start + 2 * network_spacing, button_width, button_height, "VOLVER AL MENÚ", "🔙",
                        (100, 100, 150), (150, 150, 200))
        ]
        
        # Input moderno escalado
        self.ip_input = ModernInputBox(center_x, int(370 * self.scale_y), button_width, int(60 * self.scale_y), "192.168.1.")

    def draw_animated_background(self):
        """Dibuja el fondo animado que ocupa TODA la pantalla"""
        # Fondo sólido que cubre toda el área - CORREGIDO
        self.screen.fill((15, 25, 45))  # Color de fondo base que cubre TODO
        
        # Efecto de gradiente animado que cubre TODA la pantalla
        for y in range(0, self.HEIGHT, 2):  # Paso de 2px para mejor rendimiento
            time_factor = math.sin(self.time * 0.5 + y * 0.01) * 0.1 + 0.9
            r = int(15 * time_factor + 10 * (y / self.HEIGHT))
            g = int(25 * time_factor + 15 * (y / self.HEIGHT))
            b = int(45 * time_factor + 20 * (y / self.HEIGHT))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.WIDTH, y))
        
        # Capa adicional de partículas que cubre toda la pantalla
        for particle in self.particles:
            particle.update()
            particle.draw(self.screen)
            
        # Efecto de scanning beam que cubre TODA la pantalla
        scan_y = (math.sin(self.time * 2) * 0.5 + 0.5) * self.HEIGHT
        scan_height = int(100 * self.scale_y)
        scan_surface = pygame.Surface((self.WIDTH, scan_height), pygame.SRCALPHA)
        
        for i in range(scan_height):
            alpha = int(30 * (1 - abs(i - scan_height//2) / (scan_height//2)))
            pygame.draw.line(scan_surface, (255, 255, 255, alpha), 
                           (0, i), (self.WIDTH, i))
        
        self.screen.blit(scan_surface, (0, scan_y - scan_height//2))

    def draw_main_menu(self):
        """Dibuja el menú principal moderno"""
        self.draw_animated_background()  # Esto debe cubrir TODA la pantalla
        
        # Título principal con efectos
        self.draw_animated_title()
        
        # Subtítulo
        try:
            subtitle_size = int(28 * self.scale_factor)
            subtitle_font = pygame.font.SysFont('segoeui', subtitle_size)
        except:
            subtitle_size = int(28 * self.scale_factor)
            subtitle_font = pygame.font.Font(None, subtitle_size)
        
        subtitle_text = "Control por Gestos • Física Avanzada • Multijugador"
        subtitle = subtitle_font.render(subtitle_text, True, (180, 180, 255))
        subtitle_x = self.WIDTH // 2 - subtitle.get_width() // 2
        subtitle_y = int(220 * self.scale_y)
        
        # Sombra para el subtítulo
        shadow = subtitle_font.render(subtitle_text, True, (0, 0, 0))
        self.screen.blit(shadow, (subtitle_x + 2, subtitle_y + 2))
        self.screen.blit(subtitle, (subtitle_x, subtitle_y))
        
        # Dibujar botones
        mouse_pos = pygame.mouse.get_pos()
        for button in self.main_buttons:
            button.update(mouse_pos)
            button.draw(self.screen)
            
        # Información inferior
        self.draw_footer_info()

    def draw_animated_title(self):
        """Dibuja el título con animaciones - VERSIÓN MEJORADA"""
        # Tamaño de fuente escalado
        title_font_size = int(80 * self.scale_factor)
        glow_font_size = int(82 * self.scale_factor)
        
        try:
            title_font = pygame.font.SysFont('segoeui', title_font_size)
            glow_font = pygame.font.SysFont('segoeui', glow_font_size)
        except:
            title_font = pygame.font.Font(None, title_font_size)
            glow_font = pygame.font.Font(None, glow_font_size)
        
        # Efecto de glow pulsante
        self.title_glow += 0.05 * self.title_direction
        if self.title_glow > 10 or self.title_glow < 0:
            self.title_direction *= -1
            
        # Texto principal
        title_text = "PING PONG PRO"
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.WIDTH//2, int(150 * self.scale_y)))
        
        # Sombra para mejor legibilidad
        shadow_surface = title_font.render(title_text, True, (0, 0, 0))
        self.screen.blit(shadow_surface, (title_rect.x + 3, title_rect.y + 3))
        
        # Efecto de glow
        for i in range(int(self.title_glow)):
            alpha = 10 - i
            glow_surface = glow_font.render(title_text, True, (0, 150, 255, alpha))
            glow_rect = glow_surface.get_rect(center=(self.WIDTH//2, int(150 * self.scale_y)))
            self.screen.blit(glow_surface, glow_rect)
        
        # Texto principal
        self.screen.blit(title_surface, title_rect)

    def draw_network_menu(self):
        """Dibuja el menú de red moderno"""
        self.draw_animated_background()
        
        try:
            title_font_size = int(60 * self.scale_factor)
            title_font = pygame.font.SysFont('segoeui', title_font_size)
        except:
            title_font_size = int(60 * self.scale_factor)
            title_font = pygame.font.Font(None, title_font_size)
            
        title = title_font.render("PARTIDA ONLINE", True, (0, 200, 255))
        title_rect = title.get_rect(center=(self.WIDTH//2, int(120 * self.scale_y)))
        
        # Sombra del título
        shadow = title_font.render("PARTIDA ONLINE", True, (0, 0, 0))
        self.screen.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)
        
        # Contenido según pantalla
        mouse_pos = pygame.mouse.get_pos()
        
        if self.current_screen == "join_game":
            self.draw_join_game_screen(mouse_pos)
        else:
            self.draw_network_options(mouse_pos)
            
        self.draw_footer_info()

    def draw_join_game_screen(self, mouse_pos):
        """Dibuja la pantalla de unirse a partida"""
        try:
            instruction_size = int(28 * self.scale_factor)
            instruction_font = pygame.font.SysFont('segoeui', instruction_size)
        except:
            instruction_size = int(28 * self.scale_factor)
            instruction_font = pygame.font.Font(None, instruction_size)
            
        instruction = instruction_font.render("Ingresa la IP del servidor:", True, (200, 200, 255))
        self.screen.blit(instruction, (self.WIDTH//2 - instruction.get_width()//2, int(300 * self.scale_y)))
        
        # Input de IP
        self.ip_input.update(mouse_pos)
        self.ip_input.draw(self.screen)
        
        # Botón conectar
        connect_button_width = int(400 * self.scale_x)
        connect_button_height = int(60 * self.scale_y)
        connect_button = ModernButton(
            self.WIDTH//2 - connect_button_width//2, 
            int(450 * self.scale_y), 
            connect_button_width, 
            connect_button_height, 
            "CONECTAR AL SERVIDOR", "🚀",
            (0, 180, 100), (0, 220, 150)
        )
        connect_button.update(mouse_pos)
        connect_button.draw(self.screen)
        
        # Estado de conexión
        if self.connection_status:
            try:
                status_size = int(24 * self.scale_factor)
                status_font = pygame.font.SysFont('segoeui', status_size)
            except:
                status_size = int(24 * self.scale_factor)
                status_font = pygame.font.Font(None, status_size)
            status_color = (0, 255, 100) if "conectado" in self.connection_status.lower() else (255, 100, 100)
            status_text = status_font.render(self.connection_status, True, status_color)
            self.screen.blit(status_text, (self.WIDTH//2 - status_text.get_width()//2, int(530 * self.scale_y)))

    def draw_network_options(self, mouse_pos):
        """Dibuja las opciones de red"""
        try:
            instruction_size = int(28 * self.scale_factor)
            instruction_font = pygame.font.SysFont('segoeui', instruction_size)
        except:
            instruction_size = int(28 * self.scale_factor)
            instruction_font = pygame.font.Font(None, instruction_size)
            
        instruction = instruction_font.render("Selecciona una opción para jugar online:", True, (200, 200, 255))
        self.screen.blit(instruction, (self.WIDTH//2 - instruction.get_width()//2, int(200 * self.scale_y)))
        
        for button in self.network_buttons:
            button.update(mouse_pos)
            button.draw(self.screen)

    def draw_footer_info(self):
        """Dibuja la información del footer escalada"""
        try:
            footer_size = int(18 * self.scale_factor)
            version_font = pygame.font.SysFont('segoeui', footer_size)
        except:
            footer_size = int(18 * self.scale_factor)
            version_font = pygame.font.Font(None, footer_size)
        
        # Versión
        version_text = "v2.0 - Física Avanzada • Control por Gestos • Multijugador"
        version = version_font.render(version_text, True, (150, 150, 200))
        self.screen.blit(version, (int(20 * self.scale_x), self.HEIGHT - int(25 * self.scale_y)))
        
        # Controles
        controls_text = "ESC: Menú • F: Física • G: Gestos/Teclado • C: Cámara"
        controls = version_font.render(controls_text, True, (150, 150, 200))
        self.screen.blit(controls, (self.WIDTH - controls.get_width() - int(20 * self.scale_x), self.HEIGHT - int(25 * self.scale_y)))

    def update(self, events):
        """Actualiza las animaciones y maneja los eventos"""
        self.time += 0.016  # Aprox 60 FPS
        
        # Actualizar partículas
        for particle in self.particles:
            particle.update()
            
        return self.handle_events(events)

    def handle_events(self, events):
        """Maneja los eventos del menú - VERSIÓN CORREGIDA CON ESC"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            
            # MANEJO DE TECLA ESC EN TODAS LAS PANTALLAS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_screen == "leaderboard":
                        self.current_screen = "main"
                    elif self.current_screen == "network":
                        self.current_screen = "main"
                    elif self.current_screen == "join_game":
                        self.current_screen = "network"
                    # Si está en el menú principal, ESC cierra el juego
                    elif self.current_screen == "main":
                        return "quit"
            
            if self.current_screen == "main":
                for i, button in enumerate(self.main_buttons):
                    if button.is_clicked(mouse_pos, event):
                        if i == 0:  # Solo vs IA
                            return "start_solo"
                        elif i == 1:  # Partida Online
                            self.current_screen = "network"
                        elif i == 2:  # Clasificación
                            self.current_screen = "leaderboard"
                        elif i == 3:  # Salir
                            return "quit"
                            
            elif self.current_screen == "network":
                for i, button in enumerate(self.network_buttons):
                    if button.is_clicked(mouse_pos, event):
                        if i == 0:  # Crear partida
                            if self.network.start_server():
                                return "wait_for_player"
                            else:
                                self.connection_status = "❌ Error al crear el servidor"
                        elif i == 1:  # Unirse
                            self.current_screen = "join_game"
                        elif i == 2:  # Volver
                            self.current_screen = "main"
                            
            elif self.current_screen == "join_game":
                if hasattr(self, 'ip_input'):
                    if self.ip_input.handle_event(event):
                        self.attempt_connection()
                        
            # MANEJO DE EVENTOS EN LA PANTALLA DE LEADERBOARD
            elif self.current_screen == "leaderboard":
                # Crear botón volver temporal para detectar clics
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

    def attempt_connection(self):
        """Intenta conectarse al servidor"""
        ip_address = self.ip_input.text.strip()
        if ip_address:
            if self.network.connect_to_server(ip_address):
                self.connection_status = "✅ Conectado al servidor!"
                return "start_client"
            else:
                self.connection_status = f"❌ No se pudo conectar a {ip_address}"
        else:
            self.connection_status = "⚠️ Ingresa una dirección IP."
        return "continue"

    def draw(self):
        """Dibuja la pantalla actual con elementos escalados"""
        if self.current_screen == "main":
            self.draw_main_menu()
        elif self.current_screen == "network":
            self.draw_network_menu()
        elif self.current_screen == "leaderboard":
            # Dibujar fondo primero para evitar parches negros
            self.draw_animated_background()
            
            # Dibujar el leaderboard
            self.leaderboard.draw(self.screen)
            
            # Botón volver moderno escalado
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
            
            # Instrucción ESC escalada
            try:
                esc_size = int(20 * self.scale_factor)
                esc_font = pygame.font.SysFont('segoeui', esc_size)
            except:
                esc_size = int(20 * self.scale_factor)
                esc_font = pygame.font.Font(None, esc_size)
            esc_text = esc_font.render("Presiona ESC para volver al menú", True, (150, 150, 200))
            self.screen.blit(esc_text, (self.WIDTH//2 - esc_text.get_width()//2, self.HEIGHT - int(120 * self.scale_y)))
            
            # Footer info también en leaderboard
            self.draw_footer_info()

# Función de utilidad para crear menú responsive
def create_responsive_menu(screen):
    """Crea un menú moderno responsive para la pantalla dada"""
    return ModernMenu(screen)

# Ejemplo de uso
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 700), pygame.RESIZABLE)
    pygame.display.set_caption("Ping Pong Pro - Menú Responsive")
    
    menu = create_responsive_menu(screen)
    clock = pygame.time.Clock()
    
    print("🎮 Menú moderno responsive inicializado")
    print(f"📏 Tamaño de pantalla: {screen.get_size()}")
    
    running = True
    while running:
        action = menu.update()
        
        if action == "quit":
            running = False
        elif action == "start_solo":
            print("🚀 Iniciando juego...")
            # Aquí iría la lógica para iniciar el juego
            pygame.time.wait(1000)  # Simulación
            
        menu.draw()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()