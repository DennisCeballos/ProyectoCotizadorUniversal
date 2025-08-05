# Clase para gestionar los productos que se generan en una cotizacion
class Producto:
    def __init__(self, _nombre, _precio, _origen):
        self.nombre = _nombre
        self.precio = _precio
        self.origen = _origen

    def __repr__(self):
        return f"{self.nombre} - S/.{self.precio} ({self.origen})"
