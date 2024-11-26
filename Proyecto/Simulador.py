from Entidades import A_init, B_init, A_salida, A_entrada, B_entrada
from CapaRed import recibir_paquete, socket_alicia, socket_bartolo
import threading

def ejecutar_simulacion():
    """Inicia la simulación del protocolo rdt3.0."""
    A_init()
    B_init()

    # Enviar un mensaje desde ALICIA
    mensaje = "Hola, Bartolo!"
    A_salida(mensaje)

    # Procesar paquetes en bucle
    while True:
        paquete = recibir_paquete(socket_bartolo)
        if paquete:
            B_entrada(paquete)

        paquete = recibir_paquete(socket_alicia)
        if paquete:
            A_entrada(paquete)


if __name__ == "__main__":
    simulacion_thread = threading.Thread(target=ejecutar_simulacion)
    simulacion_thread.start()
