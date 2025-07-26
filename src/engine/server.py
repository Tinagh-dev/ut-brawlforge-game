import os
import pygame
import socket
import threading 
from config import screen_width, screen_height, FPS
from src.engine.bullet import Bullet
from src.engine.platform import Platform
from src.engine.explosion import Explosion
from src.engine.camera import Camera
from src.engine.input_handler import InputHandler
from src.engine.Ninja import Ninja
from src.engine.Archer import Archer
from src.engine.NinjaGirl import NinjaGirl
from src.engine.Roboman import Roboman
from src.engine.menu import PauseMenu
from src.engine.power_ups import Power_up
from src.levels import multiplayer_data, load_level_data, build_enemies, build_objects, apply_targets_to_enemies
import json




HOST="0.0.0.0"
PORT=9191


class multiplayer_game:
    def __init__(self, screen, platform_image, background, selected_char, selected_char2):
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(2)  # Expecting 2 clients for now
        print(f"Server started on {HOST}:{PORT}")
        
        
        self.clients = []  # list of (conn, addr)
        self.inputs = [None, None]
        self.states = [None, None]
        
        self.screen = screen
        self.background = background
        
        self.clock = pygame.time.Clock()
        
        self.screen_color = (60, 100, 150)
        
        self.scroll = [0, 0]
        
        self.shot_bullets = []
        self.explosions = []
        self.bullet_class = Bullet
        
        
        self.game_active = True

        self.shutter_strength = 0
        self.shutter_start_time = 0
        self.shutter_duration = 150

        player_start_pos = multiplayer_data['player_start']
        player2_start_pos = multiplayer_data['player2_start']

        self.hero = self.create_hero(selected_char, player_start_pos, 1)
        self.hero2 = self.create_hero(selected_char2, player2_start_pos, 2)
        
        self.platforms = load_level_data(multiplayer_data, platform_image)
        self.power_ups = [Power_up(player_start_pos['x']-100, player_start_pos['y'], 'guard drone', [self.hero, self.hero2])]


        self.hero.attack_targets =  [self.hero2]
        self.hero2.attack_targets =  [self.hero]
        
    def client_thread(self, conn, client_id):
        print(f"Client {client_id} connected")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                input_data = json.loads(data.decode('utf-8'))
                self.inputs[client_id] = input_data
                print(f"Client {client_id} input: {input_data}")

                # Build the state response
                client_state = self.states[client_id]
                opponent_id = 1 - client_id
                opponent_state = self.states[opponent_id]

                state_response = {
                    "self": client_state,
                    "opponent": opponent_state
                }

                conn.sendall(json.dumps(state_response).encode('utf-8'))

            except Exception as e:
                print(f"Error with client {client_id}: {e}")
                break
        conn.close()
        print(f"Client {client_id} disconnected")
        
        
    def start(self):
        for i in range(2):
            conn, addr = self.server_socket.accept()
            self.clients.append((conn, addr))
            threading.Thread(target=self.client_thread, args=(conn, i), daemon=True).start()

        print("All clients connected. Game ready to begin.")