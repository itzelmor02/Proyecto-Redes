import random
from Entidades import A_init, B_init, A_salida, A_entrada, B_entrada
from CapaRed import capa_3
from Utils import checksum

# Probabilidades de pérdida y corrupción de paquetes
PROB_PERDIDA = 0.1  
PROB_CORRUPCION = 0.2  

def capa_3_simulada(entidad, paquete):
    """
    Simula la capa de red (capa 3) con posibilidad de pérdida o corrupción de paquetes.
    """
    if random.random() < PROB_PERDIDA:
        print(f"[Simulador] Paquete de {entidad} perdido en la capa 3.")
        return  # Simula la pérdida del paquete

    if random.random() < PROB_CORRUPCION:
        paquete_corrupto = paquete.copy()
        # Corrompe el checksum aleatoriamente
        paquete_corrupto["checksum"] = random.randint(0, 65535)  
        print(f"[Simulador] Paquete de {entidad} corrompido en la capa 3.")
        capa_3(entidad, paquete_corrupto)  # Envía el paquete corrupto a la capa 3
    else:
        print(f"[Simulador] Paquete de {entidad} enviado sin errores: {paquete}")
        capa_3(entidad, paquete)  # Envía el paquete sin errores a la capa 3

if __name__ == "__main__":
    
    A_init()  # Inicializa a ALICIA
    B_init()  # Inicializa a BARTOLO

    mensaje = "Hola, Bartolo!"
    print(f"[ALICE] Enviando paquete: {mensaje}")
    A_salida(mensaje)  # ALICIA envía un mensaje

    # Crea un paquete de prueba para la simulación
    paquete_prueba = {
        "datos": mensaje,
        "seqnum": 0,
        "checksum": checksum({"datos": mensaje, "seqnum": 0})
    }

    capa_3_simulada("ALICIA", paquete_prueba)  # Simula el envío del paquete

    print(f"[BARTOLO] Procesando paquete recibido...")
    B_entrada(paquete_prueba)  # BARTOLO procesa el paquete

    # Crea un ACK para la simulación
    ack = {
        "acknum": paquete_prueba["seqnum"],
        "checksum": checksum({"acknum": paquete_prueba["seqnum"]})
    }
    capa_3_simulada("BARTOLO", ack)  # Simula el envío del ACK

    print(f"[ALICE] Procesando ACK recibido...")
    A_entrada(ack)  # ALICIA procesa el ACK