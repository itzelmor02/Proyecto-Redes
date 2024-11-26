import json
from Simulador_UDP import socket_alicia, socket_bartolo, HOST, PORT_A, PORT_B
from Utils import checksum

# Variables globales
alice_seqnum = 0
bartolo_seqnum = 0

def A_salida(mensaje):
    """Envía un paquete desde ALICIA a BARTOLO."""
    global alice_seqnum

    # Crear paquete con datos y checksum
    paquete = {
        "datos": mensaje,
        "seqnum": alice_seqnum,
        "checksum": checksum({"datos": mensaje, "seqnum": alice_seqnum}),
    }

    # Convertir el paquete a JSON para enviarlo por UDP
    paquete_serializado = json.dumps(paquete).encode("utf-8")
    socket_alicia.sendto(paquete_serializado, (HOST, PORT_B))
    print(f"[ALICIA] Paquete enviado: {paquete}")

def B_entrada():
    """Recibe paquetes en BARTOLO y envía ACKs."""
    global bartolo_seqnum

    while True:
        # Recibir paquete
        data, addr = socket_bartolo.recvfrom(1024)
        paquete = json.loads(data.decode("utf-8"))
        print(f"[BARTOLO] Paquete recibido: {paquete}")

        # Verificar integridad y número de secuencia
        if verificar_checksum(paquete) and paquete["seqnum"] == bartolo_seqnum:
            print(f"[BARTOLO] Paquete válido procesado.")
            # Entregar el mensaje a la capa 5
            a_capa_5("BARTOLO", paquete["datos"])

            # Responder con un ACK
            ack = {
                "acknum": paquete["seqnum"],
                "checksum": checksum({"acknum": paquete["seqnum"]}),
            }
            socket_bartolo.sendto(json.dumps(ack).encode("utf-8"), addr)
            print(f"[BARTOLO] ACK enviado: {ack}")

            # Actualizar número de secuencia
            bartolo_seqnum = 1 - bartolo_seqnum
        else:
            print(f"[BARTOLO] Paquete inválido o duplicado.")
