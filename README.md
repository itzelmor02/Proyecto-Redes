## Proyecto-Redes

# Integrantes
- Itzel Morales García
- Rodrigo Galeana Vidaurri

# Conclusión del Proyecto

1. ¿Cuál crees que es la principal desventaja de rdt3.0 como protocolo fiable de transferencia de datos?
La principal desventaja de rdt3.0 es su ineficiencia en entornos de alto rendimiento o alta latencia. Este protocolo depende de un reconocimiento explícito (ACK) por cada paquete enviado, lo que introduce un retraso considerable cuando:
- La latencia entre emisor y receptor es alta.
- Se necesita transmitir grandes cantidades de datos, ya que no aprovecha la transmisión en paralelo (pipelining) como lo hacen otros protocolos más avanzados como TCP.

2. ¿Consideras que este protocolo podría ser usado en la vida real? ¿Sí o no? Justifica tu respuesta.
No, por su ineficiencia en comparación con otros protocolos, por su falta de optimización para redes reales y por sus casos de uso limitados

3. ¿Qué cosas nuevas has aprendido con este proyecto?
Comprender cómo las fallas en la transmisión afectan la integridad y confiabilidad de los datos y la separación de responsabilidades entre capas, como la lógica de red y transporte.

4. ¿Cómo crees que lo aprendido se relaciona con los otros temas del curso y la carrera?
- **Arquitectura de redes**: Refuerza la comprensión de cómo los protocolos de transporte trabajan junto con las capas inferiores para garantizar una comunicación confiable.
- **Estructura de datos y algoritmos**: Retransmisión, control de errores y detección de paquetes alterados son problemas que se resuelven con algoritmos eficientes.
- **Sistemas distribuidos**: La confiabilidad en redes es un componente clave para sistemas distribuidos, como bases de datos o aplicaciones en la nube.

5. ¿Qué papel crees que juegan las Ciencias de la Computación en el diseño de protocolos de redes de computadoras?

Las Ciencias de la Computación son fundamentales porque proveen las herramientas para diseñar, analizar y optimizar los protocolos que sustentan la comunicación global.
