import socket
import threading
import random
import json
from Utils import checksum, verificar_checksum

# Configuración básica
HOST = "127.0.0.1"  # Dirección local
PORT_A = 5000        # Puerto de ALICIA
PORT_B = 5001        # Puerto de BARTOLO
BUFFER_SIZE = 1024   # Tamaño del buffer

# Sockets para ALICIA y BARTOLO
socket_alicia = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_alicia.bind((HOST, PORT_A))

socket_bartolo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_bartolo.bind((HOST, PORT_B))
