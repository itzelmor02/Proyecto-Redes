# Modificar funciones de retransmisión y manejo de ACKs
import json
import threading
from Simulador_UDP import *
from Utils import checksum, verificar_checksum

# Variables globales
alice_seqnum = 0
bartolo_seqnum = 0
TIMEOUT = 2  # Tiempo de retransmisión en segundos
timer = None  # Temporizador para retransmisión
ultimo_paquete = None  # Último paquete enviado desde ALICIA

def iniciar_temporizador(paquete, destino):
    """Inicia o reinicia el temporizador para retransmisión."""
    global timer
    if timer:
        timer.cancel()
    timer = threading.Timer(TIMEOUT, retransmitir, args=(paquete, destino))
    timer.start()

def retransmitir(paquete, destino):
    """Retransmite un paquete si no se recibe un ACK a tiempo."""
    global timer  # Acceder a la variable global timer
    print(f"[ALICIA] Retransmitiendo paquete: {paquete}")
    paquete_serializado = json.dumps(paquete).encode("utf-8")
    socket_alicia.sendto(paquete_serializado, destino)
    # Reiniciar el temporizador solo si la simulación sigue activa
    if simulacion_activa:
        iniciar_temporizador(paquete, destino)

def A_salida(mensaje):
    """Envía un paquete desde ALICIA a BARTOLO."""
    global alice_seqnum, ultimo_paquete

    # Crear paquete con datos y checksum
    paquete = {
        "datos": mensaje,
        "seqnum": alice_seqnum,
        "checksum": checksum({"datos": mensaje, "seqnum": alice_seqnum}),
    }
    ultimo_paquete = paquete  # Guardar el último paquete enviado

    print(f"[ALICIA] Enviando paquete: {paquete}")
    enviar_con_fallos(socket_alicia, paquete, (HOST, PORT_B))
    iniciar_temporizador(paquete, (HOST, PORT_B))  # Iniciar temporizador

def A_entrada():
    """Recibe ACKs en ALICIA."""
    global alice_seqnum, timer

    while simulacion_activa:
        try:
            data, addr = socket_alicia.recvfrom(1024)
            ack = json.loads(data.decode("utf-8"))
            print(f"[ALICIA] ACK recibido: {ack}")

            # Verificar integridad del ACK y si corresponde al paquete enviado
            if verificar_checksum(ack) and ack["acknum"] == alice_seqnum:
                print(f"[ALICIA] ACK válido recibido.")
                if timer:
                    timer.cancel()  # Detener el temporizador
                alice_seqnum = 1 - alice_seqnum  # Alternar número de secuencia
            else:
                print(f"[ALICIA] ACK inválido o duplicado. Reenviando paquete.")
                retransmitir(ultimo_paquete, (HOST, PORT_B))  # Reenviar el último paquete
        except socket.timeout:
            print(f"[ALICIA] Tiempo de espera agotado. Reenviando paquete.")
            retransmitir(ultimo_paquete, (HOST, PORT_B))  # Reenviar el último paquete
        except Exception as e:
            print(f"[ALICIA] Error: {e}")

def B_entrada():
    """Recibe paquetes en BARTOLO y envía ACKs."""
    global bartolo_seqnum

    while True:
        try:
            data, addr = socket_bartolo.recvfrom(1024)
            paquete = json.loads(data.decode("utf-8"))
            print(f"[BARTOLO] Paquete recibido: {paquete}")

            # Verificar integridad y número de secuencia
            if verificar_checksum(paquete) and paquete["seqnum"] == bartolo_seqnum:
                print(f"[BARTOLO] Paquete válido procesado.")
                # Entregar datos a la capa 5
                print(f"[BARTOLO] Mensaje entregado a capa 5: {paquete['datos']}")

                # Responder con un ACK
                ack = {
                    "acknum": paquete["seqnum"],
                    "checksum": checksum({"acknum": paquete["seqnum"]}),
                }
                enviar_con_fallos(socket_bartolo, ack, addr)
                print(f"[BARTOLO] ACK enviado: {ack}")
                bartolo_seqnum = 1 - bartolo_seqnum  # Alternar número de secuencia
            else:
                print(f"[BARTOLO] Paquete inválido o duplicado.")
        except socket.timeout:
            print(f"[BARTOLO] Tiempo de espera agotado.")  # No es necesario retransmitir en BARTOLO
        except Exception as e:
            print(f"[BARTOLO] Error: {e}")