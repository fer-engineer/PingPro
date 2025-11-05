import pygame
import numpy as np

class Dashboard:
    def __init__(self, screen, width, height, position):
        self.screen = screen
        self.width = width
        self.height = height
        self.position = position
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Escalas y fuentes
        self.scale_x = screen.get_width() / 1000
        self.scale_y = screen.get_height() / 700
        self.scale_factor = min(self.scale_x, self.scale_y)

        self.title_font = pygame.font.Font(None, int(28 * self.scale_factor))
        self.header_font = pygame.font.Font(None, int(22 * self.scale_factor))
        self.font = pygame.font.Font(None, int(20 * self.scale_factor))
        
        self.colors = {
            'gravedad': (0, 255, 0),      # Verde
            'velocidad': (255, 0, 0),     # Rojo
            'resistencia_aire': (255, 255, 0), # Amarillo
            'spin': (0, 255, 255),        # Cian
            'resultante': (255, 0, 255)   # Magenta
        }

    def draw(self, forces):
        # Fondo semi-transparente
        self.surface.fill((30, 30, 30, 200))
        
        # Borde
        pygame.draw.rect(self.surface, (100, 100, 255), self.surface.get_rect(), 2)

        # Título
        title_surface = self.title_font.render("Análisis de Físicas", True, (255, 255, 255))
        self.surface.blit(title_surface, (10, 10))

        # Dibujar barras de fuerza
        self.draw_force_bars(forces, 50)

        # Dibujar tabla de detalles
        self.draw_details_table(forces, 250)

        # Dibujar la superficie del dashboard en la pantalla principal
        self.screen.blit(self.surface, self.position)

    def draw_force_bars(self, forces, y_start):
        bar_width = self.width - 20
        bar_height = int(15 * self.scale_factor)
        y = y_start

        for name, data in forces.items():
            if name == 'resultante': continue

            # Etiqueta
            label = self.font.render(name.replace('_', ' ').title(), True, self.colors.get(name, (255, 255, 255)))
            self.surface.blit(label, (10, y))
            y += 20

            # Barra
            magnitude = data['magnitud']
            max_magnitude = 10 # Valor de referencia para la escala de la barra
            normalized_magnitude = min(1, magnitude / max_magnitude)
            
            # Fondo de la barra
            pygame.draw.rect(self.surface, (50, 50, 50), (10, y, bar_width, bar_height))
            # Barra de progreso
            pygame.draw.rect(self.surface, self.colors.get(name, (255, 255, 255)), (10, y, bar_width * normalized_magnitude, bar_height))
            
            # Valor
            value_text = self.font.render(f"{magnitude:.2f} N", True, (255, 255, 255))
            self.surface.blit(value_text, (bar_width - 50, y))

            y += bar_height + 15

    def draw_details_table(self, forces, y_start):
        y = y_start
        
        # Encabezados
        headers = ["Fuerza", "Fx", "Fy", "|F|", "Angle"]
        x_positions = [10, 90, 150, 210, 270]
        for i, header in enumerate(headers):
            header_surface = self.header_font.render(header, True, (200, 200, 255))
            self.surface.blit(header_surface, (x_positions[i], y))
        
        y += 30

        # Datos
        for name, data in forces.items():
            color = self.colors.get(name, (255, 255, 255))
            
            # Nombre de la fuerza
            name_surface = self.font.render(name.replace('_', ' ').title(), True, color)
            self.surface.blit(name_surface, (x_positions[0], y))

            # Valores
            fx = f"{data['vector'][0]:.2f}"
            fy = f"{data['vector'][1]:.2f}"
            mag = f"{data['magnitud']:.2f}"
            angle = f"{data['angulo']:.1f}°"
            
            values = [fx, fy, mag, angle]
            for i, value in enumerate(values):
                value_surface = self.font.render(value, True, (255, 255, 255))
                self.surface.blit(value_surface, (x_positions[i+1], y))

            y += 25