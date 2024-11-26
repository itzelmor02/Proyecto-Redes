import json
import random
import socket

# Configuración para la simulación de red
PROB_PERDIDA = 0.1
PROB_CORRUPCION = 0.2
BUFFER_SIZE = 1024

# Sockets para simular la comunicación entre ALICIA y BARTOLO
socket_alicia = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_bartolo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socket_alicia.bind(("localhost", 10000))
socket_bartolo.bind(("localhost", 10001))


def enviar_paquete(entidad, paquete, direccion):
    """Serializa y envía un paquete con posibilidad de pérdida o corrupción."""
    # Simula pérdida de paquete
    if random.random() < PROB_PERDIDA:
        print(f"[Capa 3] El paquete de {entidad} se perdió.")
        return

    # Serializa el paquete a JSON
    paquete_serializado = json.dumps(paquete).encode()

    # Simula corrupción de paquete
    if random.random() < PROB_CORRUPCION:
        paquete_serializado = bytearray(paquete_serializado)
        paquete_serializado[0] = (paquete_serializado[0] + 1) % 256
        paquete_serializado = bytes(paquete_serializado)
        print(f"[Capa 3] El paquete de {entidad} fue corrompido.")

    # Envía el paquete
    print(f"[Capa 3] Enviando paquete de {entidad}: {paquete}")
    socket_alicia.sendto(paquete_serializado, direccion)


def recibir_paquete(socket_receptor):
    """Recibe y deserializa un paquete."""
    datos, _ = socket_receptor.recvfrom(BUFFER_SIZE)
    try:
        paquete = json.loads(datos.decode())
        return paquete
    except json.JSONDecodeError:
        print("[Capa 3] Paquete recibido corrupto.")
        return None
