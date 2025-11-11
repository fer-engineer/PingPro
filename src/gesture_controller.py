import cv2
import mediapipe as mp
import numpy as np
import pygame

class GestureController:
    def __init__(self, width, height):
        self.screen_width = width
        self.screen_height = height
        
        # Inicializar cámara
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("⚠️ No se pudo acceder a la cámara. El control por gestos no funcionará.")
            self.camera_available = False
        else:
            self.camera_available = True
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Configuración de MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Posición de la mano y frame
        self.hand_x = self.screen_width * 3 // 4
        self.hand_y = self.screen_height // 2
        self.last_frame = None
        self.frame_counter = 0

    def process_frame(self):
        """Procesa un frame de la cámara para detectar la mano."""
        if not self.camera_available:
            return

        success, image = self.cap.read()
        if not success:
            # Si falla la lectura, usar un frame negro como fallback
            self.last_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            return

        # Optimización: procesar una imagen más pequeña si es posible
        # image = cv2.resize(image, (320, 240))

        image.flags.writeable = False
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        
        results = self.hands.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        self.last_frame = image

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Usar el punto medio de la palma para más estabilidad
                x = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x
                y = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].y
                
                # Mapeo a la pantalla
                self.hand_x = int(x * self.screen_width)
                self.hand_y = int(y * self.screen_height)
                
                # Dibujar landmarks para feedback visual
                self.mp_draw.draw_landmarks(self.last_frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def get_hand_position_2d(self):
        """Obtiene la posición 2D de la mano, procesando un nuevo frame."""
        self.process_frame()
        return self.hand_x, self.hand_y

    def get_camera_frame(self):
        """Devuelve el último frame procesado como una superficie de Pygame."""
        if self.last_frame is not None:
            frame_rgb = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB)
            frame_pygame = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
            return frame_pygame
        return None

    def cleanup(self):
        """Libera los recursos de la cámara y MediaPipe."""
        if self.camera_available:
            self.cap.release()
        self.hands.close()