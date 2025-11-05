import numpy as np
import pygame

class VectorCalculator:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Factores de escala basados en resolución de referencia (1000x700)
        self.scale_x = screen_width / 1000
        self.scale_y = screen_height / 700
        self.scale_factor = min(self.scale_x, self.scale_y)  # Usamos el mínimo para mantener proporciones
        
        self.forces = {}
        self.history = []
        
        # Fuentes escaladas
        self.font = pygame.font.Font(None, int(24 * self.scale_factor))
        self.small_font = pygame.font.Font(None, int(20 * self.scale_factor))
        self.title_font = pygame.font.Font(None, int(28 * self.scale_factor))
        
    def calculate_force_components(self, ball, paddle_collision=None):
        """Calcula todas las componentes de fuerza actuando sobre la pelota"""
        # Masa asumida de la pelota (para cálculo de fuerzas)
        mass = 0.0027  # kg (masa típica pelota ping pong)
        
        # 1. FUERZA DE GRAVEDAD
        gravity_force = mass * 9.8 * 100 * self.scale_factor  # Escalado para pixels
        gravity_vector = [0, gravity_force]
        
        # 2. FUERZA DE VELOCIDAD ACTUAL (Impulso)
        speed_force_x = ball.velocity_x * mass * 50 * self.scale_factor
        speed_force_y = ball.velocity_y * mass * 50 * self.scale_factor
        velocity_vector = [speed_force_x, speed_force_y]
        
        # 3. FUERZA DE RESISTENCIA DEL AIRE (opuesta al movimiento)
        air_resistance = 0.001
        air_force_x = -air_resistance * ball.velocity_x * abs(ball.velocity_x) * self.scale_factor
        air_force_y = -air_resistance * ball.velocity_y * abs(ball.velocity_y) * self.scale_factor
        air_resistance_vector = [air_force_x, air_force_y]
        
        # 4. FUERZA DE SPIN (Efecto Magnus)
        spin_force = ball.spin * 0.5 * self.scale_factor
        spin_vector = [spin_force, 0]
        
        # 5. FUERZA DE COLISIÓN (si hay impacto reciente)
        collision_vector = [0, 0]
        if ball.collision_effect > 0:
            collision_vector = [ball.velocity_x * 0.1 * self.scale_factor, ball.velocity_y * 0.1 * self.scale_factor]
        
        # Fuerza resultante
        total_force_x = (velocity_vector[0] + air_resistance_vector[0] + 
                        spin_vector[0] + collision_vector[0])
        total_force_y = (gravity_force + velocity_vector[1] + 
                        air_resistance_vector[1] + collision_vector[1])
        
        self.forces = {
            'gravedad': {
                'vector': gravity_vector,
                'magnitud': np.sqrt(gravity_vector[0]**2 + gravity_vector[1]**2),
                'angulo': np.degrees(np.arctan2(gravity_vector[1], gravity_vector[0]))
            },
            'velocidad': {
                'vector': velocity_vector,
                'magnitud': np.sqrt(velocity_vector[0]**2 + velocity_vector[1]**2),
                'angulo': np.degrees(np.arctan2(velocity_vector[1], velocity_vector[0]))
            },
            'resistencia_aire': {
                'vector': air_resistance_vector,
                'magnitud': np.sqrt(air_resistance_vector[0]**2 + air_resistance_vector[1]**2),
                'angulo': np.degrees(np.arctan2(air_resistance_vector[1], air_resistance_vector[0]))
            },
            'spin': {
                'vector': spin_vector,
                'magnitud': abs(spin_force),
                'angulo': 0 if spin_force >= 0 else 180
            },
            'resultante': {
                'vector': [total_force_x, total_force_y],
                'magnitud': np.sqrt(total_force_x**2 + total_force_y**2),
                'angulo': np.degrees(np.arctan2(total_force_y, total_force_x))
            }
        }
        
        # Guardar en historial para análisis
        if len(self.history) > 100:  # Mantener solo últimos 100 frames
            self.history.pop(0)
        self.history.append(self.forces.copy())
        
        return self.forces
    


    def update_screen_size(self, new_width, new_height):
        """Actualiza el tamaño de pantalla para recálculo de escalas"""
        self.screen_width = new_width
        self.screen_height = new_height
        self.scale_x = new_width / 1000
        self.scale_y = new_height / 700
        self.scale_factor = min(self.scale_x, self.scale_y)
        
        # Actualizar fuentes con nueva escala
        self.font = pygame.font.Font(None, int(24 * self.scale_factor))
        self.small_font = pygame.font.Font(None, int(20 * self.scale_factor))
        self.title_font = pygame.font.Font(None, int(28 * self.scale_factor))

# Clase Vector para cálculos matemáticos (mantenida para compatibilidad)
class Vector:
    """
    Clase para cálculos vectoriales básicos
    Basada en implementaciones de código abierto 
    """
    def __init__(self, values):
        self.values = tuple(values)
    
    def get_values(self):
        return self.values
    
    def get_size(self):
        return len(self.values)
    
    def get_norm(self):
        """Calcula la norma (magnitud) del vector"""
        return math.sqrt(sum(x ** 2 for x in self.values))
    
    def __add__(self, other):
        """Suma de dos vectores"""
        if self.get_size() == other.get_size():
            return Vector(tuple(x + y for x, y in zip(self.values, other.values)))
    
    def __sub__(self, other):
        """Resta de dos vectores"""
        if self.get_size() == other.get_size():
            return Vector(tuple(x - y for x, y in zip(self.values, other.values)))
    
    def __mul__(self, scalar):
        """Multiplicación por escalar"""
        return Vector(tuple(x * scalar for x in self.values))
    
    def dot_product(self, other):
        """Producto escalar (dot product)"""
        if self.get_size() == other.get_size():
            return sum(x * y for x, y in zip(self.values, other.values))
    
    def cross_product(self, other):
        """Producto vectorial (solo para 3D)"""
        if self.get_size() == 3 and other.get_size() == 3:
            x1, y1, z1 = self.values
            x2, y2, z2 = other.values
            return Vector((
                y1 * z2 - z1 * y2,
                z1 * x2 - x1 * z2,
                x1 * y2 - y1 * x2
            ))
    
    def get_angle_degrees(self, other):
        """Ángulo entre dos vectores en grados"""
        import math
        dot = self.dot_product(other)
        norms = self.get_norm() * other.get_norm()
        if norms == 0:
            return 0
        return math.degrees(math.acos(dot / norms))
    
    def normalize(self):
        """Vector normalizado (dirección)"""
        norm = self.get_norm()
        if norm == 0:
            return Vector((0,) * self.get_size())
        return Vector(tuple(x / norm for x in self.values))
    
    def __str__(self):
        return f"Vector{self.values}"

# Ejemplos de uso y pruebas
if __name__ == "__main__":
    import math
    
    # Pruebas básicas de la clase Vector
    v1 = Vector((1, 2, 3))
    v2 = Vector((3, 2, 1))
    
    print("Vectores de ejemplo:")
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"Suma: {v1 + v2}")
    print(f"Producto escalar: {v1.dot_product(v2)}")
    print(f"Magnitud v1: {v1.get_norm():.2f}")
    print(f"Ángulo entre v1 y v2: {v1.get_angle_degrees(v2):.2f}°")