import sys
import os
class Utils:
    
    @staticmethod
    def getPosibles_nameNombre():
        return ["nombre", "descripcion", "presentacion"]
    
    @staticmethod
    def getPosibles_namePrecio():
        return ["precio", "costo", "coste"]

    @staticmethod
    def get_base_path() -> str: # Necesario para obtener el path del archivo ejecutandose
        if getattr(sys, 'frozen', False):
            # En caso se este ejecutando en un un archivo de pyinstaller
            return os.path.dirname(sys.executable) # type: ignore
        else:
            # En caso se este ejecutando en un ambiente de desarrollo
            # retorna la direccion de ESTE ARCHIVO, asi que hay que corregirlo
            ubi = os.path.dirname(os.path.abspath(__file__))
            ubi = ubi[: ubi.rfind('\\')]
            ubi = ubi[: ubi.rfind('\\')]
            return ubi