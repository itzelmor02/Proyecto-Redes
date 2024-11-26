def checksum(paquete):
    """
    Calcula el checksum de un paquete sumando los valores ASCII de sus campos.
    """
    datos = paquete.get('datos', '')
    suma = sum(ord(char) for char in datos)
    suma += paquete.get('seqnum', 0)
    suma += paquete.get('acknum', 0)
    return suma % 65536


def verificar_checksum(paquete):
    """
    Verifica si el checksum de un paquete es válido.
    """
    return checksum(paquete) == paquete.get('checksum', 0)
