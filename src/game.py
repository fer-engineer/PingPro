import pygame
import numpy as np
import sys
import time
from gesture_controller import GestureController
from utils import Colors
from vector_calculator import VectorCalculator
from dashboard import Dashboard

class Table:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.top = int(50 * (height / 700))
        self.bottom = height - int(50 * (height / 700))
        self.center_line_y_start = self.top
        self.center_line_y_end = self.bottom
        self.net_width = int(4 * (width / 1000))
        self.net_height = 20
        
    def draw(self, screen):
        # Dibujar mesa (fondo verde)
        table_rect = pygame.Rect(0, self.top, self.width, self.bottom - self.top)
        pygame.draw.rect(screen, (0, 100, 0), table_rect)
        pygame.draw.rect(screen, Colors.WHITE, table_rect, 2)
        
        # Dibujar línea central
        center_x = self.width // 2
        for y in range(self.center_line_y_start, self.center_line_y_end, 20):
            pygame.draw.rect(screen, Colors.WHITE, 
                           (center_x - 1, y, 2, 10))
        
        # Dibujar red
        net_x = center_x - self.net_width // 2
        pygame.draw.rect(screen, Colors.WHITE, 
                        (net_x, self.top, self.net_width, self.bottom - self.top))
        
        # Dibujar bordes de la mesa
        border_thickness = int(8 * (self.height / 700))
        # Borde superior
        pygame.draw.rect(screen, Colors.WHITE, 
                        (0, self.top - border_thickness, self.width, border_thickness))
        # Borde inferior
        pygame.draw.rect(screen, Colors.WHITE, 
                        (0, self.bottom, self.width, border_thickness))

class Ball:
    def __init__(self, x, y, scale_factor=1.0):
        self.x = x
        self.y = y
        self.radius = int(15 * scale_factor)
        self.color = (255, 255, 255)
        self.velocity_x = 0
        self.velocity_y = 0
        self.spin = 0
        self.trail = []
        self.max_trail_length = 10
        self.collision_effect = 0
        self.ready_to_serve = True
        self.serve_countdown = 0
        self.auto_serve_countdown = 0
        self.scale_factor = scale_factor

    def update(self, table):
        # Saque automático después de countdown
        if self.auto_serve_countdown > 0:
            self.auto_serve_countdown -= 1
            if self.auto_serve_countdown == 0:
                self.serve()
                return
        
        # Si está en countdown de saque, no mover
        if self.serve_countdown > 0:
            self.serve_countdown -= 1
            return
            
        # Guardar posición para el rastro
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Aplicar gravedad REDUCIDA (escalada)
        self.velocity_y += 0.08 * self.scale_factor
        
        # Aplicar resistencia del aire REDUCIDA
        self.velocity_x *= 0.998
        self.velocity_y *= 0.998
        
        # Velocidad mínima garantizada - escalada
        min_speed = 8 * self.scale_factor
        current_speed = np.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if 0 < current_speed < min_speed:
            scale = min_speed / current_speed
            self.velocity_x *= scale
            self.velocity_y *= scale
        
        # Aplicar efecto Magnus
        self.velocity_x += self.spin * 0.01 * self.scale_factor
        
        # Actualizar posición
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Reducir spin gradualmente
        self.spin *= 0.99
        
        # Reducir efecto de colisión
        if self.collision_effect > 0:
            self.collision_effect -= 1
        
        # Rebotes en bordes
        if self.y - self.radius < table.top:
            self.y = table.top + self.radius
            self.velocity_y *= -0.92
            self.spin *= 0.9
            self.collision_effect = 10
        elif self.y + self.radius > table.bottom:
            self.y = table.bottom - self.radius
            self.velocity_y *= -0.92
            self.spin *= 0.9
            self.collision_effect = 10

    def serve(self, direction=1):
        """Realiza un saque controlado"""
        if self.ready_to_serve:
            self.ready_to_serve = False
            self.serve_countdown = 60
            
            # Velocidad inicial CONTROLADA (escalada)
            serve_speed = 12 * self.scale_factor
            angle_variation = np.random.uniform(-0.3, 0.3)
            
            self.velocity_x = direction * serve_speed * np.cos(angle_variation)
            self.velocity_y = serve_speed * np.sin(angle_variation)
            
            return True
        return False

    def reset_for_serve(self, x, y, direction=1):
        """Prepara la pelota para un nuevo saque"""
        self.x = x
        self.y = y
        # Velocidad horizontal mínima garantizada para evitar que se quede atrapada
        self.velocity_x = direction * 2 * self.scale_factor
        self.velocity_y = 0
        self.spin = 0
        self.ready_to_serve = True
        self.trail = []
        # Saque automático después de 2 segundos (120 frames)
        self.auto_serve_countdown = 120

    def draw(self, screen):
        """Dibuja la pelota y sus efectos"""
        # Dibujar rastro de movimiento
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha_ratio = i / len(self.trail)
            gray_value = int(200 * alpha_ratio)
            size = max(2, int(self.radius * alpha_ratio))
            pygame.draw.circle(screen, (gray_value, gray_value, gray_value), 
                             (int(trail_x), int(trail_y)), size)
        
        # Efecto de colisión
        if self.collision_effect > 0:
            wave_radius = self.radius + self.collision_effect * 2
            wave_color = (255, 200, 100)
            pygame.draw.circle(screen, wave_color, 
                             (int(self.x), int(self.y)), 
                             wave_radius, 2)
        
        # Efecto de parpadeo durante countdown de saque
        if self.serve_countdown > 0 or self.auto_serve_countdown > 0:
            if ((self.serve_countdown // 10) % 2 == 0 or 
                (self.auto_serve_countdown // 10) % 2 == 0):
                pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius + 3, 2)
        
        # Pelota principal
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), self.radius, 2)

class Paddle:
    def __init__(self, x, y, color, is_ai=False, is_right_side=True, scale_factor=1.0):
        self.rect = pygame.Rect(x, y, int(20 * scale_factor), int(100 * scale_factor))
        self.color = color
        self.velocity_x = 0
        self.velocity_y = 0
        self.score = 0
        self.is_ai = is_ai
        self.is_right_side = is_right_side
        self.scale_factor = scale_factor
        self.target_x = x
        self.target_y = y
        self.smoothing_factor = 0.5  # Aumentado para mayor respuesta

    def set_target(self, x_pos, y_pos, table):
        """Define la posición objetivo de la raqueta, aplicando límites."""
        # Calcular nueva posición centrada en la mano
        new_x = x_pos - self.rect.width // 2
        new_y = y_pos - self.rect.height // 2
        
        # Límites según el lado de la mesa
        if self.is_right_side:
            min_x = table.width // 2 + int(10 * self.scale_factor)
            max_x = table.width - self.rect.width - int(10 * self.scale_factor)
        else:
            min_x = int(10 * self.scale_factor)
            max_x = table.width // 2 - self.rect.width - int(10 * self.scale_factor)
        
        # Aplicar límites
        self.target_x = max(min_x, min(new_x, max_x))
        self.target_y = max(table.top + int(10 * self.scale_factor), 
                           min(new_y, table.bottom - self.rect.height - int(10 * self.scale_factor)))

    def update(self):
        """Mueve la raqueta suavemente hacia su objetivo."""
        # Interpolar posición para un movimiento suave
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y
        
        # Si la distancia es pequeña, teletransportar para evitar vibraciones
        if abs(dx) < 1 and abs(dy) < 1:
            self.rect.x = self.target_x
            self.rect.y = self.target_y
        else:
            self.rect.x += dx * self.smoothing_factor
            self.rect.y += dy * self.smoothing_factor

        # Calcular velocidades para efectos físicos
        self.velocity_x = dx * self.smoothing_factor
        self.velocity_y = dy * self.smoothing_factor

    def move(self, y_pos, table):
        """Método legacy para movimiento solo vertical (compatibilidad)"""
        if self.is_right_side:
            x_pos = table.width * 3 // 4
        else:
            x_pos = table.width // 4
        self.set_target(x_pos, y_pos, table)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, Colors.WHITE, self.rect, 2, border_radius=5)
        
        # Indicador de posición (punto central)
        center_x = self.rect.x + self.rect.width // 2
        center_y = self.rect.y + self.rect.height // 2
        pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y), 3)

class PingPongGame:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        
        # Factores de escala
        self.scale_x = self.WIDTH / 1000
        self.scale_y = self.HEIGHT / 700
        self.scale_factor = min(self.scale_x, self.scale_y)
        
        # Objetos del juego
        self.table = Table(self.WIDTH, self.HEIGHT)
        self.ball = Ball(self.WIDTH // 2, self.HEIGHT // 2, self.scale_factor)
        
        self.left_paddle = Paddle(
            int(50 * self.scale_x), int(self.HEIGHT / 2 - 50 * self.scale_y), 
            Colors.BLUE, is_ai=True, is_right_side=False, scale_factor=self.scale_factor
        )
        self.right_paddle = Paddle(
            int(self.WIDTH - 70 * self.scale_x), int(self.HEIGHT / 2 - 50 * self.scale_y), 
            Colors.RED, is_ai=False, is_right_side=True, scale_factor=self.scale_factor
        )

        self.gesture_controller = GestureController(self.WIDTH, self.HEIGHT)
        self.control_por_gestos = True
        self.show_physics = False
        self.show_camera_preview = False
        self.game_paused = False
        self.game_over = False
        self.winner = None
        self.final_score = 0
        self.game_started = False
        self.serve_direction = 1
        self.frame_counter = 0
        
        # Fuentes
        self.font = pygame.font.Font(None, int(36 * self.scale_factor))
        self.small_font = pygame.font.Font(None, int(24 * self.scale_factor))
        self.large_font = pygame.font.Font(None, int(48 * self.scale_factor))

        # Dashboard y Vectores
        self.vector_calculator = VectorCalculator(self.WIDTH, self.HEIGHT)
        self.show_dashboard = False
        dashboard_width = int(300 * self.scale_x)
        self.dashboard = Dashboard(self.screen, dashboard_width, self.HEIGHT, (0, 0))

    def start_game(self):
        """Inicia el juego con el primer saque"""
        if not self.game_started:
            self.game_started = True
            self.ball.serve(self.serve_direction)
            self.vector_calculator = VectorCalculator(self.WIDTH, self.HEIGHT)
            self.show_dashboard = True

    def handle_events(self, events):
        """Maneja todos los eventos de entrada"""
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                elif event.key == pygame.K_SPACE:
                    if not self.game_started or self.ball.ready_to_serve:
                        self.start_game()
                    else:
                        self.game_paused = not self.game_paused
                elif event.key == pygame.K_r:
                    self.reset_ball()
                elif event.key == pygame.K_g:
                    self.control_por_gestos = not self.control_por_gestos
                elif event.key == pygame.K_f:
                    self.show_physics = not self.show_physics
                elif event.key == pygame.K_v:
                    self.show_dashboard = not self.show_dashboard
                elif event.key == pygame.K_c:
                    self.show_camera_preview = not self.show_camera_preview
        
        return True

    def update_paddles(self):
        """Actualiza el movimiento de las paletas"""
        if self.control_por_gestos:
            hand_x, hand_y = self.gesture_controller.get_hand_position_2d()
            self.right_paddle.set_target(hand_x, hand_y, self.table)
        else:
            self.update_keyboard_controls_2d()
        
        self.update_ai_paddle_2d()
        self.left_paddle.update()
        self.right_paddle.update()

    def update_keyboard_controls_2d(self):
        """Control por teclado para movimiento 2D con velocidad escalada"""
        keys = pygame.key.get_pressed()
        
        speed = 15 * self.scale_factor
        
        target_x = self.right_paddle.target_x
        target_y = self.right_paddle.target_y
        
        if keys[pygame.K_UP]:
            target_y -= speed
        if keys[pygame.K_DOWN]:
            target_y += speed
        if keys[pygame.K_LEFT]:
            target_x -= speed
        if keys[pygame.K_RIGHT]:
            target_x += speed
            
        self.right_paddle.set_target(target_x + self.right_paddle.rect.width / 2, 
                                     target_y + self.right_paddle.rect.height / 2, 
                                     self.table)

    def update_ai_paddle_2d(self):
        """IA más justa con errores de predicción"""
        ball_coming_toward_ai = self.ball.velocity_x < 0
        
        if ball_coming_toward_ai:
            error = np.random.uniform(0.8, 1.2)
            time_to_reach = abs(self.left_paddle.rect.x - self.ball.x) / max(1, abs(self.ball.velocity_x))
            
            predicted_y = self.ball.y + (self.ball.velocity_y * time_to_reach * error)
            predicted_y = max(self.table.top + int(50 * self.scale_factor), 
                            min(predicted_y, self.table.bottom - int(50 * self.scale_factor)))
            
            target_y = predicted_y + np.random.uniform(-20 * self.scale_factor, 20 * self.scale_factor)
        else:
            target_y = self.table.top + (self.table.bottom - self.table.top) // 2
        
        current_y = self.left_paddle.rect.y + self.left_paddle.rect.height // 2
        
        if abs(current_y - target_y) > 10 * self.scale_factor:
            speed = np.random.uniform(0.06, 0.1)
            new_y = current_y + (target_y - current_y) * speed
            
            target_x = self.WIDTH // 4
            self.left_paddle.set_target(target_x, new_y, self.table)

    def check_collisions(self):
        """Verifica colisiones entre la pelota y las paletas"""
        if self.ball.x - self.ball.radius < self.left_paddle.rect.right and self.ball.x + self.ball.radius > self.left_paddle.rect.left and self.ball.y + self.ball.radius > self.left_paddle.rect.top and self.ball.y - self.ball.radius < self.left_paddle.rect.bottom:
            self.handle_paddle_collision(self.left_paddle, True)
        
        if self.ball.x + self.ball.radius > self.right_paddle.rect.left and self.ball.x - self.ball.radius < self.right_paddle.rect.right and self.ball.y + self.ball.radius > self.right_paddle.rect.top and self.ball.y - self.ball.radius < self.right_paddle.rect.bottom:
            self.handle_paddle_collision(self.right_paddle, False)

    def handle_paddle_collision(self, paddle, is_left_paddle):
        """Maneja la colisión entre la pelota y una paleta"""
        if is_left_paddle:
            self.ball.x = paddle.rect.right + self.ball.radius
        else:
            self.ball.x = paddle.rect.left - self.ball.radius
            
        self.ball.collision_effect = 15
        
        relative_intersect_y = (paddle.rect.centery - self.ball.y) / (paddle.rect.height / 2)
        bounce_angle = relative_intersect_y * (np.pi / 3)
        
        speed = np.sqrt(self.ball.velocity_x**2 + self.ball.velocity_y**2) * 1.22
        speed = min(speed, 25 * self.scale_factor)
        
        self.ball.velocity_x = speed * np.cos(bounce_angle) * (1 if is_left_paddle else -1)
        self.ball.velocity_y = -speed * np.sin(bounce_angle)
        
        self.ball.velocity_x += paddle.velocity_x * 0.1
        self.ball.spin += paddle.velocity_y * 0.3

    def update_game(self):
        """Actualiza el estado del juego"""
        if self.game_paused or self.game_over or not self.game_started:
            return
            
        self.ball.update(self.table)
        self.check_collisions()
        
        if self.ball.x < -50 * self.scale_factor:
            self.right_paddle.score += 1
            self.check_game_over()
            self.reset_ball()
        elif self.ball.x > self.WIDTH + 50 * self.scale_factor:
            self.left_paddle.score += 1
            self.check_game_over()
            self.reset_ball()

    def check_game_over(self):
        """Verifica si algún jugador ha ganado"""
        if self.left_paddle.score >= 5:
            self.game_over = True
            self.winner = "IA"
            self.final_score = self.right_paddle.score
        elif self.right_paddle.score >= 5:
            self.game_over = True
            self.winner = "JUGADOR"
            self.final_score = self.right_paddle.score

    def reset_ball(self):
        """Resetea la pelota para nuevo saque AUTOMÁTICO"""
        if self.ball.x < -50 * self.scale_factor:
            self.ball.reset_for_serve(self.WIDTH // 4, self.HEIGHT // 2, direction=1)
            self.serve_direction = 1
        else:
            self.ball.reset_for_serve(3 * self.WIDTH // 4, self.HEIGHT // 2, direction=-1)
            self.serve_direction = -1

    def draw_physics_vectors(self):
        """Dibuja vectores de fuerza visibles"""
        if not self.show_physics:
            return
            
        speed = np.sqrt(self.ball.velocity_x**2 + self.ball.velocity_y**2)
        if speed > 0:
            scale = 25 * self.scale_factor
            end_x = self.ball.x + (self.ball.velocity_x / speed) * scale
            end_y = self.ball.y + (self.ball.velocity_y / speed) * scale
            
            pygame.draw.line(self.screen, (255, 0, 0), 
                           (self.ball.x, self.ball.y), 
                           (end_x, end_y), 3)
            pygame.draw.circle(self.screen, (255, 0, 0), (int(end_x), int(end_y)), 5)
        
        gravity_end_y = self.ball.y + 20 * self.scale_factor
        pygame.draw.line(self.screen, (0, 100, 255), 
                        (self.ball.x, self.ball.y), 
                        (self.ball.x, gravity_end_y), 2)
        
        if abs(self.ball.spin) > 0.5:
            spin_direction = 1 if self.ball.spin > 0 else -1
            spin_end_x = self.ball.x + spin_direction * 20 * self.scale_factor
            pygame.draw.line(self.screen, (0, 255, 100), 
                           (self.ball.x, self.ball.y), 
                           (spin_end_x, self.ball.y), 2)

    def draw_predicted_trajectory(self):
        """Dibuja la trayectoria futura predicha de forma más fluida"""
        if not self.show_physics or self.game_paused or not self.game_started:
            return
            
        temp_ball = type('TempBall', (), {})()
        temp_ball.x, temp_ball.y, temp_ball.velocity_x, temp_ball.velocity_y, temp_ball.spin, temp_ball.radius = self.ball.x, self.ball.y, self.ball.velocity_x, self.ball.velocity_y, self.ball.spin, self.ball.radius
        points = []
        for _ in range(15):
            temp_ball.velocity_y += 0.08 * self.scale_factor
            temp_ball.velocity_x *= 0.998
            temp_ball.velocity_y *= 0.998
            temp_ball.velocity_x += temp_ball.spin * 0.01 * self.scale_factor
            temp_ball.spin *= 0.99
            temp_ball.x += temp_ball.velocity_x
            temp_ball.y += temp_ball.velocity_y
            if not (self.table.top < temp_ball.y < self.table.bottom): temp_ball.velocity_y *= -0.92
            points.append((temp_ball.x, temp_ball.y))
            if not (-50 * self.scale_factor < temp_ball.x < self.WIDTH + 50 * self.scale_factor): break
        if len(points) > 1: pygame.draw.lines(self.screen, (255, 100, 0), False, points, 2)

    def draw_energy_display(self):
        """Dibuja indicador de energía cinética de forma más eficiente"""
        if not self.game_started:
            return
            
        speed = np.sqrt(self.ball.velocity_x**2 + self.ball.velocity_y**2)
        normalized_energy = min(1, speed / 16.67)
        
        bar_width = int(200 * self.scale_factor)
        bar_height = int(15 * self.scale_factor)
        bar_x = self.WIDTH // 2 - bar_width // 2
        bar_y = self.HEIGHT - int(30 * self.scale_factor)
        
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
        
        energy_bar_width = int(bar_width * normalized_energy)
        if energy_bar_width > 0:
            color = (int(255 * normalized_energy), int(255 * (1 - normalized_energy)), 0)
            pygame.draw.rect(self.screen, color, (bar_x, bar_y, energy_bar_width, bar_height), border_radius=4)
        
        energy_percentage = normalized_energy * 100
        energy_text = self.small_font.render(f"ENERGÍA: {energy_percentage:.0f}%", True, Colors.WHITE)
        self.screen.blit(energy_text, (bar_x, bar_y - int(20 * self.scale_factor)))

    def draw_ui(self):
        """Dibuja la interfaz de usuario escalada"""
        score_text = f"{self.left_paddle.score} - {self.right_paddle.score}"
        score_surface = self.large_font.render(score_text, True, Colors.TEXT)
        self.screen.blit(score_surface, (self.WIDTH // 2 - score_surface.get_width() // 2, int(10 * self.scale_factor)))
        
        if not self.game_started:
            start_font = pygame.font.Font(None, int(40 * self.scale_factor))
            start_text = start_font.render("Presiona ESPACIO para comenzar", True, Colors.ACCENT)
            self.screen.blit(start_text, (self.WIDTH//2 - start_text.get_width()//2, self.HEIGHT//2 - int(50 * self.scale_factor)))
        
        if self.game_paused:
            s = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 200))
            self.screen.blit(s, (0, 0))
            pause_surface = self.large_font.render("PAUSADO", True, Colors.WARNING)
            self.screen.blit(pause_surface, (self.WIDTH // 2 - pause_surface.get_width()//2, self.HEIGHT // 2 - pause_surface.get_height()//2))
        
        if self.game_over:
            s = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 220))
            self.screen.blit(s, (0, 0))
            
            winner_text = f"¡{self.winner} GANA!"
            winner_surface = self.large_font.render(winner_text, True, Colors.SUCCESS)
            self.screen.blit(winner_surface, (self.WIDTH // 2 - winner_surface.get_width() // 2, self.HEIGHT // 2 - int(80 * self.scale_factor)))
            
            score_text_final = f"Puntuación final: {self.final_score}"
            score_surface = self.font.render(score_text_final, True, Colors.ACCENT)
            self.screen.blit(score_surface, (self.WIDTH // 2 - score_surface.get_width() // 2, self.HEIGHT // 2))
            
            continue_text = "Presiona ESC para volver al menú"
            continue_surface = self.small_font.render(continue_text, True, Colors.TEXT)
            self.screen.blit(continue_surface, (self.WIDTH // 2 - continue_surface.get_width() // 2, self.HEIGHT // 2 + int(80 * self.scale_factor)))

    def draw(self):
        self.screen.fill(Colors.BACKGROUND)
        self.table.draw(self.screen)
        self.draw_predicted_trajectory()
        self.ball.draw(self.screen)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.draw_physics_vectors()
        self.draw_energy_display()
        self.draw_ui()

        if self.show_dashboard:
            forces = self.vector_calculator.calculate_force_components(self.ball)
            self.dashboard.draw(forces)

        if self.control_por_gestos and self.show_camera_preview:
            self.draw_camera_preview()
        
        pygame.display.flip()

    def draw_camera_preview(self):
        try:
            camera_surface = self.gesture_controller.get_camera_frame()
            if camera_surface:
                preview_width = int(200 * self.scale_factor)
                preview_height = int(150 * self.scale_factor)
                camera_scaled = pygame.transform.scale(camera_surface, (preview_width, preview_height))
                preview_x = self.WIDTH - preview_width - int(10 * self.scale_x)
                preview_y = int(10 * self.scale_y)
                
                bg_rect = pygame.Rect(preview_x - 5, preview_y - 5, preview_width + 10, preview_height + 10)
                pygame.draw.rect(self.screen, (30, 30, 30, 180), bg_rect, border_radius=8)
                pygame.draw.rect(self.screen, (100, 100, 200), bg_rect, 2, border_radius=8)
                
                self.screen.blit(camera_scaled, (preview_x, preview_y))
        except Exception as e:
            pass

    def run_game(self):
        """Bucle principal del juego"""
        clock = pygame.time.Clock()
        running = True
        print("MODO FISICA ACTIVADO - Tecla F para mostrar/ocultar")
        print("Presiona ESPACIO para comenzar el juego")
        print("Control 2D activado - Mueve tu mano libremente por tu mitad de mesa")
        print("Estadisticas fisicas en tiempo real disponibles")

        while running:
            events = pygame.event.get()
            result = self.handle_events(events)
            if result == "menu" or result is False:
                running = False
                break

            self.update_paddles()
            self.update_game()

            self.draw()
            self.frame_counter += 1
            clock.tick(60)

        self.gesture_controller.cleanup()
        return self.final_score if self.game_over else None