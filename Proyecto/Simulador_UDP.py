import socket
import random
import json
import threading
from Utils import checksum

# Configuración básica
HOST = "127.0.0.1"  # Dirección local
PORT_A = 5000        # Puerto de ALICIA
PORT_B = 5001        # Puerto de BARTOLO
BUFFER_SIZE = 1024   # Tamaño del buffer

# Variables de control
simulacion_activa = True

# Sockets para ALICIA y BARTOLO
socket_alicia = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_alicia.bind((HOST, PORT_A))

socket_bartolo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_bartolo.bind((HOST, PORT_B))

def detener_hilos():
    """Finaliza la simulación y cierra los sockets."""
    global simulacion_activa
    simulacion_activa = False
    socket_alicia.close()
    socket_bartolo.close()
    print("[Simulador] Simulación detenida.")

# Configuración de fallos
PROBABILIDAD_PERDIDA = 0.1  # 10% de paquetes se pierden
PROBABILIDAD_CORRUPCION = 0.2  # 20% de paquetes se corrompen

def simular_perdida():
    """
    Decide aleatoriamente si un paquete se pierde según la probabilidad configurada.
    """
    return random.random() < PROBABILIDAD_PERDIDA

def simular_corrupcion(paquete):
    """
    Corrompe un paquete manipulando sus datos, seqnum o checksum.
    """
    if random.random() < PROBABILIDAD_CORRUPCION:
        # Alterar aleatoriamente los datos, el seqnum o el checksum
        tipo_corrupcion = random.choice(["datos", "seqnum", "checksum"])
        if tipo_corrupcion == "datos":
            paquete["datos"] = "CORRUPTO!"
        elif tipo_corrupcion == "seqnum":
            paquete["seqnum"] = 1 - paquete["seqnum"]  # Invertir el seqnum
        else:
            paquete["checksum"] = random.randint(0, 65535)  # Asignar un checksum aleatorio

        # Recalcular el checksum si se corrompieron los datos o el seqnum
        if tipo_corrupcion != "checksum":
            paquete["checksum"] = checksum(paquete)

        print("[Simulador] Paquete corrompido!")
    return paquete

def enviar_con_fallos(socket, paquete, direccion):
    """
    Envía un paquete simulando posibles fallos (pérdida o corrupción).
    """
    if simular_perdida():
        print("[Simulador] Paquete perdido!")
        return  # Simula pérdida no enviando el paquete
    paquete = simular_corrupcion(paquete)
    paquete_serializado = json.dumps(paquete).encode("utf-8")
    socket.sendto(paquete_serializado, direccion)