# Proyecto Cotizador Universal

Si deseas optimizar tus compras, probablemente cuentes con varias **fuentes de datos**, cada uno con diferentes formatos y nombres de producto.

ENTONCES, ¿cómo se puede simplificar el trabajo de encontrar el mismo producto en cada archivo?

Para utilizar este proyecto de Python, debes colocar tus archivos de datos (de preferencia archivos csv o excel) en la misma dirección donde esté la carpeta "app". Luego, solo ejecuta el archivo ``main.py``.

Recuerda instalar las librerías en ``requirements.txt``

## Exportar proyecto
Es posible exportar el proyecto a un archivo ejecutable .exe usando el siguiente comando ```pyinstaller --onefile "app/main.py"```
Este archivo exe sigue el comportamiento del programa normalmente: colocalo en la misma direccion de tus archivos excel para incluirlos entre las opciones de cotizacion