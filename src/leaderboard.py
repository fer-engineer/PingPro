import json
import datetime
import pygame
from utils import Colors

class Leaderboard:
    def __init__(self):
        self.scores = self.load_scores()
        
    def load_scores(self):
        try:
            with open('assets/scores.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
            
    def save_scores(self):
        try:
            with open('assets/scores.json', 'w') as f:
                json.dump(self.scores, f, indent=2)
        except Exception as e:
            print(f"Error guardando puntuaciones: {e}")
            
    def add_score(self, name, score):
        if not name.strip():
            name = "Jugador Anónimo"
            
        self.scores.append({
            'name': name,
            'score': score,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:10]
        self.save_scores()
        
    def draw(self, screen):
        try:
            title_font = pygame.font.SysFont('segoeui', 48, bold=True)
            header_font = pygame.font.SysFont('segoeui', 32, bold=True)
            font = pygame.font.SysFont('segoeui', 30)
            small_font = pygame.font.SysFont('segoeui', 26)
        except:
            title_font = pygame.font.Font(None, 52)
            header_font = pygame.font.Font(None, 36)
            font = pygame.font.Font(None, 34)
            small_font = pygame.font.Font(None, 30)

        # Título
        title = title_font.render("Mejores Puntajes", True, Colors.PRIMARY)
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 80))
        
        # Contenedor principal
        container_rect = pygame.Rect(screen.get_width()//2 - 350, 150, 700, 400)
        pygame.draw.rect(screen, (20, 40, 70, 180), container_rect, border_radius=15)
        pygame.draw.rect(screen, Colors.PRIMARY, container_rect, 2, border_radius=15)

        # Encabezados
        headers = ["#", "Nombre", "Puntuación", "Fecha"]
        header_x_positions = [container_rect.x + 40, container_rect.x + 120, container_rect.x + 350, container_rect.x + 500]
        
        for i, header in enumerate(headers):
            text = header_font.render(header, True, Colors.ACCENT)
            screen.blit(text, (header_x_positions[i], container_rect.y + 20))
        
        # Línea separadora
        pygame.draw.line(screen, Colors.PRIMARY, (container_rect.left + 20, container_rect.y + 60), (container_rect.right - 20, container_rect.y + 60), 1)
        
        # Puntuaciones
        for i, score_data in enumerate(self.scores):
            y_pos = container_rect.y + 80 + i * 32
            
            # Posición
            pos_text = font.render(f"{i+1}", True, Colors.WHITE)
            screen.blit(pos_text, (header_x_positions[0], y_pos))
            
            # Nombre
            name_text = font.render(score_data['name'][:15], True, Colors.WHITE)
            screen.blit(name_text, (header_x_positions[1], y_pos))
            
            # Puntuación
            score_text = font.render(str(score_data['score']), True, Colors.SUCCESS)
            screen.blit(score_text, (header_x_positions[2], y_pos))
            
            # Fecha
            date_text = small_font.render(score_data['date'], True, (150, 150, 180))
            screen.blit(date_text, (header_x_positions[3], y_pos))