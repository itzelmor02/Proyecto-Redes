def checksum(paquete):
    """
    Calcula el checksum de un paquete.
    Suma los valores ASCII de los caracteres en 'datos', 'seqnum' y 'acknum', 
    y luego aplica el módulo 65536 para obtener un valor de 16 bits.
    """
    # Obtiene los datos del paquete, utilizando una cadena vacía si no hay datos
    datos = paquete.get('datos', '')  
    suma = sum(ord(char) for char in datos)  # Suma los valores ASCII de los caracteres
    suma += paquete.get('seqnum', 0)  # Suma el número de secuencia si existe
    suma += paquete.get('acknum', 0)  # Suma el número de ACK si existe
    return suma % 65536  # Aplica el módulo 65536

def verificar_checksum(paquete):
    """
    Verifica si el checksum de un paquete es válido.
    Calcula el checksum de los datos y lo compara con el checksum almacenado en el paquete.
    """
    datos_checksum = checksum(paquete)  # Calcula el checksum
    return datos_checksum == paquete.get('checksum', 0)  # Compara con el checksum del paquete