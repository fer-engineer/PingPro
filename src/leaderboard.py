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
        except:
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
        # Ordenar por puntuación (mayor primero)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        # Mantener solo top 10
        self.scores = self.scores[:10]
        self.save_scores()
        
    def draw(self, screen):
        title_font = pygame.font.Font(None, 48)
        font = pygame.font.Font(None, 32)
        small_font = pygame.font.Font(None, 28)
        
        # Fondo
        screen.fill(Colors.BACKGROUND)
        
        # Título
        title = title_font.render("🏆 MEJORES PUNTAJES", True, Colors.ACCENT)
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 80))
        
        # Encabezados
        headers = ["Posición", "Nombre", "Puntuación", "Fecha"]
        header_x_positions = [100, 250, 450, 600]
        
        for i, header in enumerate(headers):
            text = font.render(header, True, Colors.PRIMARY)
            screen.blit(text, (header_x_positions[i], 150))
        
        # Línea separadora
        pygame.draw.line(screen, Colors.PRIMARY, (50, 180), (750, 180), 2)
        
        # Puntuaciones
        for i, score_data in enumerate(self.scores):
            y_pos = 220 + i * 40
            
            # Fondo alternado para filas
            if i % 2 == 0:
                pygame.draw.rect(screen, (30, 40, 60), (50, y_pos-5, 700, 35))
            
            # Posición
            pos_text = font.render(f"{i+1}.", True, Colors.TEXT)
            screen.blit(pos_text, (header_x_positions[0], y_pos))
            
            # Nombre
            name_text = font.render(score_data['name'][:15], True, Colors.TEXT)
            screen.blit(name_text, (header_x_positions[1], y_pos))
            
            # Puntuación
            score_text = font.render(str(score_data['score']), True, Colors.ACCENT)
            screen.blit(score_text, (header_x_positions[2], y_pos))
            
            # Fecha
            date_text = small_font.render(score_data['date'], True, Colors.TEXT)
            screen.blit(date_text, (header_x_positions[3], y_pos))
        
        # Instrucción
        instruction = font.render("Presiona ESC para volver al menú", True, Colors.SECONDARY)
        screen.blit(instruction, (screen.get_width()//2 - instruction.get_width()//2, 550))