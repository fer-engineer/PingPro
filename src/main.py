import pygame
import sys
import os
from menu_modern import ModernMenu, SCREEN_WIDTH, SCREEN_HEIGHT
from game import PingPongGame
from utils import Colors, InputBox, Button

# Configuración de la pantalla
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

def ensure_assets_folder():
    """Asegura que la carpeta assets exista"""
    if not os.path.exists('assets'):
        os.makedirs('assets')
    # Crear archivo de puntuaciones si no existe
    scores_file = 'assets/scores.json'
    if not os.path.exists(scores_file):
        with open(scores_file, 'w') as f:
            f.write('[]')

def show_name_input_screen(screen, score, leaderboard):
    """Muestra la pantalla para ingresar nombre después del juego"""
    input_box = InputBox(SCREEN_WIDTH//2 - 150, 350, 300, 60)
    save_button = Button(SCREEN_WIDTH//2 - 100, 450, 200, 50, "💾 GUARDAR")
    
    clock = pygame.time.Clock()
    name_entered = False
    saved = False
    
    while not name_entered:
        screen.fill(Colors.BACKGROUND)
        
        # Título
        title_font = pygame.font.Font(None, 60)
        instruction_font = pygame.font.Font(None, 36)
        
        title = title_font.render("¡PARTIDA TERMINADA!", True, Colors.ACCENT)
        score_text = title_font.render(f"Puntuación: {score}", True, Colors.PRIMARY)
        instruction = instruction_font.render("Ingresa tu nombre:", True, Colors.TEXT)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 180))
        screen.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, 280))
        
        # Dibujar elementos
        input_box.draw(screen)
        save_button.draw(screen)
        
        # Mensaje de confirmación
        if saved:
            confirm_font = pygame.font.Font(None, 32)
            confirm_text = confirm_font.render("¡Puntuación guardada! Presiona ESC para continuar", True, Colors.SUCCESS)
            screen.blit(confirm_text, (SCREEN_WIDTH//2 - confirm_text.get_width()//2, 520))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and saved:
                    name_entered = True
                
            if input_box.handle_event(event):
                # Enter presionado
                if input_box.text.strip():
                    leaderboard.add_score(input_box.text.strip(), score)
                    saved = True
                    
            mouse_pos = pygame.mouse.get_pos()
            save_button.is_hovered(mouse_pos)
            if save_button.is_clicked(mouse_pos, event) and input_box.text.strip():
                leaderboard.add_score(input_box.text.strip(), score)
                saved = True
        
        pygame.display.flip()
        clock.tick(FPS)

def main():
    """Función principal del juego"""
    global SCREEN_WIDTH, SCREEN_HEIGHT
    # Inicializar pygame
    pygame.init()
    
    # Asegurar que la carpeta assets existe
    ensure_assets_folder()
    
    # Crear la pantalla REDIMENSIONABLE
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Ping Pong Pro - Menú Principal")
    
    # Crear menú
    menu = ModernMenu(screen)
    clock = pygame.time.Clock()
    
    print("=" * 60)
    print("🎮 PING PONG PRO - CARGANDO...")
    print("=" * 60)
    print("✨ Características disponibles:")
    print("   • Modo Solo vs IA")
    print("   • Control por gestos con cámara")
    print("   • Física avanzada visible")
    print("   • Sistema de puntuaciones")
    print("   • Menú interactivo")
    print("=" * 60)
    
    running = True
    while running:
        # Manejar eventos
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                # Recrear el menú con el nuevo tamaño de pantalla
                menu = ModernMenu(screen)

        # Actualizar el menú con los eventos
        action = menu.update(events)
        
        if action == "quit":
            running = False
            
        elif action == "start_solo":
            print("🚀 Iniciando juego vs IA...")
            # Crear instancia del juego con la pantalla actual
            game = PingPongGame(screen, "solo", None)
            # Ejecutar el juego
            final_score = game.run_game()
            
            # Si el juego terminó con una puntuación, mostrar pantalla de nombre
            if final_score is not None and final_score > 0:
                show_name_input_screen(screen, final_score, menu.leaderboard)
                # Recrear el menú para volver al menú principal
                menu = ModernMenu(screen)

        elif action == "wait_for_player":
            # Pantalla de espera para el host
            waiting = True
            font = pygame.font.Font(None, 36)
            while waiting and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        waiting = False
                        # Aquí podrías añadir lógica para cerrar el servidor si el host cancela
                
                screen.fill(Colors.BACKGROUND)
                text = font.render("Esperando a que un oponente se conecte...", True, Colors.TEXT)
                screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2))
                pygame.display.flip()

                if menu.network.connection:
                    waiting = False
                    print("✅ Oponente conectado! Iniciando partida online como Host...")
                    game = PingPongGame(screen, "online_host", menu.network)
                    game.run_game()
                    menu = ModernMenu(screen) # Volver al menú después de la partida

        elif action == "start_client":
            print("✅ Conectado! Iniciando partida online como Cliente...")
            game = PingPongGame(screen, "online_client", menu.network)
            game.run_game()
            menu = ModernMenu(screen) # Volver al menú después de la partida
        
        # Dibujar el menú actual
        menu.draw()
        pygame.display.flip()
        clock.tick(FPS)
        
    # Limpiar recursos
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()