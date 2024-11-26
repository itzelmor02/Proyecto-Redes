from Entidades_UDP import A_salida, A_entrada, B_entrada

import threading

# Simulación de comunicación UDP entre ALICIA y BARTOLO
def pruebas():
    # Iniciar los hilos para ALICIA y BARTOLO
    threading.Thread(target=A_entrada, daemon=True).start()
    threading.Thread(target=B_entrada, daemon=True).start()

    # Enviar un mensaje desde ALICIA a BARTOLO
    mensajes = ["Hola, Bartolo!", "¿Cómo estás?", "¡Adiós!"]
    for mensaje in mensajes:
        A_salida(mensaje)
        time.sleep(2)  # Esperar entre mensajes

if __name__ == "__main__":
    pruebas()
