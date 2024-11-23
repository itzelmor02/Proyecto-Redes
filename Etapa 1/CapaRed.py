def entregar_paquete(entidad, paquete):
    """
    Simula la entrega de un paquete a la capa superior (capa 5) 
    de la entidad correspondiente (ALICIA o BARTOLO).
    """
    print(f"[Capa 3] Paquete entregado: {paquete}")
    if entidad == "ALICIA":
        print("[Capa 3] Entregando a BARTOLO.")
        return paquete  # Devuelve el paquete para que el simulador lo procese
    elif entidad == "BARTOLO":
        print("[Capa 3] Entregando a ALICIA.")
        return paquete  # Devuelve el paquete para que el simulador lo procese
    else:
        print(f"[Capa 3] Entidad desconocida: {entidad}")

def capa_3(entidad, paquete):
    """
    Simula la capa de red (capa 3) que entrega paquetes entre ALICIA y BARTOLO.
    En este caso, solo imprime un mensaje indicando que el paquete ha sido recibido.
    """
    print(f"[Capa 3] Paquete recibido de {entidad}: {paquete}")
    entregar_paquete(entidad, paquete)  # Entrega el paquete a la capa superior

def capa_5(entidad, mensaje):
    """
    Simula la capa de aplicación (capa 5) que recibe el mensaje.
    """
    print(f"[Capa 5] Mensaje recibido por {entidad}: {mensaje}")