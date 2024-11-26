import threading
from CapaRed import enviar_paquete, recibir_paquete
from Utils import checksum, verificar_checksum

# Variables globales
alice_seqnum = 0
temporizador = None
ultimo_paquete_enviado = None
DIRECCION_BARTOLO = ("localhost", 10001)
DIRECCION_ALICIA = ("localhost", 10000)


def A_init():
    """Inicializa la entidad ALICIA."""
    global alice_seqnum
    alice_seqnum = 0
    print("[ALICE] Inicializado.")


def B_init():
    """Inicializa la entidad BARTOLO."""
    print("[BARTOLO] Inicializado.")


def A_salida(mensaje):
    """Procesa la salida de un mensaje desde ALICIA."""
    global alice_seqnum, ultimo_paquete_enviado, temporizador

    paquete = {
        "datos": mensaje,
        "seqnum": alice_seqnum,
        "checksum": checksum({"datos": mensaje, "seqnum": alice_seqnum}),
    }
    print(f"[ALICE] Enviando paquete: {paquete}")

    ultimo_paquete_enviado = paquete
    enviar_paquete("ALICIA", paquete, DIRECCION_BARTOLO)

    # Inicia el temporizador
    temporizador = threading.Timer(5, A_interrupcion_timer)
    temporizador.start()


def A_interrupcion_timer():
    """Retransmite el último paquete al expirar el temporizador."""
    global ultimo_paquete_enviado
    print("[Timer] Temporizador expirado. Retransmitiendo último paquete.")
    enviar_paquete("ALICIA", ultimo_paquete_enviado, DIRECCION_BARTOLO)


def A_entrada(paquete):
    """Procesa la entrada de un paquete (ACK) en ALICIA."""
    global alice_seqnum, temporizador

    if not verificar_checksum(paquete):
        print("[ALICE] ACK recibido corrupto.")
        return

    if paquete["acknum"] == alice_seqnum:
        print("[ALICE] ACK válido recibido.")
        if temporizador:
            temporizador.cancel()
        alice_seqnum = 1 - alice_seqnum
    else:
        print("[ALICE] ACK con número incorrecto.")


def B_entrada(paquete):
    """Procesa la entrada de un paquete en BARTOLO."""
    if not verificar_checksum(paquete):
        print("[BARTOLO] Paquete recibido corrupto.")
        return

    print(f"[BARTOLO] Paquete válido recibido: {paquete}")
    mensaje = paquete["datos"]
    print(f"[BARTOLO] Mensaje entregado a capa 5: {mensaje}")

    ack = {
        "acknum": paquete["seqnum"],
        "checksum": checksum({"acknum": paquete["seqnum"]}),
    }
    enviar_paquete("BARTOLO", ack, DIRECCION_ALICIA)
