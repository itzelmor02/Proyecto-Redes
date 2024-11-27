from Entidades_UDP import *
import threading
import time

def pruebas():
    """
    Realiza pruebas enviando mensajes de ALICIA a BARTOLO,
    incluyendo mensajes corruptos y perdidos.
    """
    # Iniciar los hilos para ALICIA y BARTOLO
    threading.Thread(target=A_entrada, daemon=True).start()
    threading.Thread(target=B_entrada, daemon=True).start()

    # Enviar mensajes desde ALICIA a BARTOLO
    mensajes = [
        "Hola, Bartolo!",
        "¿Cómo estás?",
        "¡Adiós!",
        "Mensaje 4",
        "Mensaje 5",
        "Mensaje 6",
        "Mensaje 7",
        "Mensaje 8",
        "Mensaje 9",
        "Mensaje 10",
    ]

    for mensaje in mensajes:
        A_salida(mensaje)
        time.sleep(4)  # Esperar entre mensajes para simular tráfico real

    # Detener la simulación después de un tiempo
    time.sleep(10)
    detener_hilos()
    print("[Simulador] Pruebas finalizadas.")

if __name__ == "__main__":
    pruebas()