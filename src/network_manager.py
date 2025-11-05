import socket
import threading
import pickle

class NetworkManager:
    def __init__(self):
        self.server = '0.0.0.0'
        self.port = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_host = False
        self.connection = None
        self.addr = None
        self.player_data = [
            {'y': 350, 'score': 0},
            {'y': 350, 'score': 0}
        ]
        self.ball_data = {'x': 500, 'y': 350, 'vx': 0, 'vy': 0}

    def start_server(self):
        self.is_host = True
        try:
            self.socket.bind((self.server, self.port))
            self.socket.listen(1)
            print(f"Servidor iniciado en {self.server}:{self.port}. Esperando conexión...")
            accept_thread = threading.Thread(target=self._accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            return True
        except Exception as e:
            print(f"Error al iniciar el servidor: {e}")
            return False

    def _accept_connections(self):
        conn, addr = self.socket.accept()
        self.connection = conn
        self.addr = addr
        print(f"Conectado a: {addr}")
        client_handler_thread = threading.Thread(target=self._handle_client)
        client_handler_thread.daemon = True
        client_handler_thread.start()

    def _handle_client(self):
        while True:
            try:
                data = pickle.loads(self.connection.recv(2048))
                self.player_data[1]['y'] = data['y']
                
                reply = {
                    'ball': self.ball_data,
                    'paddle': self.player_data[0]
                }
                self.connection.sendall(pickle.dumps(reply))
            except (EOFError, pickle.UnpicklingError, ConnectionResetError):
                print("Cliente desconectado.")
                self.connection.close()
                self.connection = None
                break

    def connect_to_server(self, host_ip):
        self.is_host = False
        try:
            self.socket.connect((host_ip, self.port))
            self.connection = self.socket
            print(f"Conectado al servidor en {host_ip}")
            return True
        except Exception as e:
            print(f"Error al conectar con el servidor: {e}")
            return False

    def send(self, data):
        try:
            if self.connection:
                self.connection.send(pickle.dumps(data))
                return pickle.loads(self.connection.recv(2048))
        except socket.error as e:
            print(f"Error de conexión: {e}")
            self.connection = None
            return None
        return None

    def update_ball(self, ball):
        if self.is_host:
            self.ball_data['x'] = ball.x
            self.ball_data['y'] = ball.y
            self.ball_data['vx'] = ball.velocity_x
            self.ball_data['vy'] = ball.velocity_y

    def update_paddle(self, paddle):
        if self.is_host:
            self.player_data[0]['y'] = paddle.rect.y
