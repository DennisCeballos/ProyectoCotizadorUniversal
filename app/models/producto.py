# Clase para gestionar los productos que se generan en una cotizacion
class Producto:
    def __init__(self, _descripcion, _precio, _origen):
        self.descripcion = _descripcion
        self.precio = _precio
        self.origen = _origen

    def __repr__(self):
        return f"{self.descripcion} - S/.{self.precio} ({self.origen})"
