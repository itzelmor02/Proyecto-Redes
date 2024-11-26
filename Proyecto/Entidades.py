from CapaRed import entregar_paquete, capa_5
from Utils import checksum
import threading

# Variables globales para el control de secuencia y temporizador de ALICIA
alice_seqnum = 0  # Número de secuencia para ALICIA (0 o 1)
temporizador = None  # Variable para almacenar el temporizador
ultimo_paquete_enviado = None  # Para almacenar el último paquete enviado por ALICIA

# --- Funciones de inicialización ---
def A_init():
    """
    Inicializa la entidad ALICIA, estableciendo el número de secuencia inicial.
    """
    global alice_seqnum
    alice_seqnum = 0  
    print("[ALICE] Inicializado.")

def B_init():
    """
    Inicializa la entidad BARTOLO.
    """
    print("[BARTOLO] Inicializado.")

# --- Función de salida para A ---
def A_salida(mensaje):
    """
    Procesa la salida de un mensaje desde ALICIA.
    Crea un paquete, lo envía a la capa de red e inicia un temporizador.
    """
    global alice_seqnum, temporizador, ultimo_paquete_enviado
    
    # Crea el paquete con datos, número de secuencia y checksum
    paquete = {
        "datos": mensaje,
        "seqnum": alice_seqnum,
        "checksum": checksum({"datos": mensaje, "seqnum": alice_seqnum}),
    }
    print(f"[ALICE] Enviando paquete: {paquete}")

    ultimo_paquete_enviado = paquete  # Guarda el paquete para posible retransmisión

    entregar_paquete("ALICIA", paquete)  # Envía el paquete a la capa de red

    # Inicia un temporizador para controlar la espera del ACK
    temporizador = threading.Timer(5, A_interrupcion_timer)  # 5 segundos de espera
    temporizador.start()
    print("[Timer] Temporizador iniciado para ALICIA por 5 segundos.")

# --- Función para manejar paquetes entrantes en A ---
def A_entrada(paquete):
    """
    Procesa la entrada de un paquete (ACK) en ALICIA.
    Verifica el checksum y el número de secuencia del ACK.
    """
    global alice_seqnum, temporizador
    print("[ALICE] Procesando ACK recibido...")
    
    # Calcula el checksum esperado para el ACK
    checksum_esperado = checksum({"acknum": paquete["acknum"]})
    if paquete["checksum"] != checksum_esperado:
        print(f"[ALICE] ACK recibido corrupto: {paquete}")
        return  # Ignora el ACK si es corrupto

    if paquete["acknum"] == alice_seqnum:  # Verifica si el número de secuencia es correcto
        print(f"[ALICE] ACK recibido: {paquete}")
        
        if temporizador is not None:
            temporizador.cancel()  # Detiene el temporizador si el ACK es correcto
            print("[Timer] Temporizador detenido para ALICIA.")
        
        alice_seqnum = 1 - alice_seqnum  # Alterna el número de secuencia (0 o 1)
    else:
        print(f"[ALICE] Número de ACK inesperado: {paquete['acknum']}")

# --- Función para manejar el temporizador expirado ---
def A_interrupcion_timer():
    """
    Función que se ejecuta cuando el temporizador de ALICIA expira.
    Retransmite el último paquete enviado.
    """
    global ultimo_paquete_enviado
    print("[Timer] Temporizador expirado para ALICIA.")
    print("[ALICE] Reenviando último paquete...")
    if ultimo_paquete_enviado is not None:
        entregar_paquete("ALICIA", ultimo_paquete_enviado)  # Reenvía el paquete

# --- Función para manejar paquetes entrantes en B ---
def B_entrada(paquete):
    """
    Procesa la entrada de un paquete en BARTOLO.
    Verifica el checksum, entrega el mensaje a la capa 5 y envía un ACK a ALICIA.
    """
    print("[BARTOLO] Procesando paquete recibido...")
    # Calcula el checksum esperado para el paquete
    checksum_esperado = checksum({"datos": paquete["datos"], "seqnum": paquete["seqnum"]})

    if paquete["checksum"] != checksum_esperado:  # Verifica si el paquete es corrupto
        print(f"[BARTOLO] Paquete corrupto detectado: {paquete}")
        return  # Ignora el paquete si es corrupto

    print(f"[BARTOLO] Paquete válido recibido: {paquete}")
    
    capa_5("BARTOLO", paquete["datos"])  # Entrega el mensaje a la capa 5

    # Crea un ACK con el número de secuencia del paquete recibido
    ack = {
        "acknum": paquete["seqnum"],
        "checksum": checksum({"acknum": paquete["seqnum"]}),
    }
    print(f"[BARTOLO] Enviando ACK: {ack}")
    entregar_paquete("BARTOLO", ack)  # Envía el ACK a la capa de red