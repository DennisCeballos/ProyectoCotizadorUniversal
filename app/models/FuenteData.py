# Clase para gestionar las fuentes de datos
import pandas as pd #nimodo i guess
from models.Utils import Utils

class FuenteDatos:
    def __init__(self, _path):
        self.path = _path
        
        self.nombre = self.path[-5:]
        
        self.nameNombre_preferido = ""
        self.namePrecio_preferido = ""

        posibles_nombre = Utils.getPosibles_nameNombre()
        posibles_precio = Utils.getPosibles_namePrecio()

        self.df = pd.read_excel(self.path)

        # bucle para encontrar la fila que contiene NOMBRE y PRECIO de producto
        # pero el nombre del producto puede ser varias palabras segun proveedor, por eso existe la lista de posibles_nombre
        # y el mismo caso para posibles_precio
        for index, row in self.df.iterrows():
            
            #print(f"Fila: {index}")
            #print(row.array)
            elementos_fila = []
            for palabra in row.array:
                elementos_fila.append( str(palabra).lower() )
            
            print("elementos_fila> ", end="")
            print(elementos_fila)

            if (set( posibles_nombre ).intersection(set(elementos_fila))) and (set(posibles_precio).intersection(set(elementos_fila))):
                    print(f"ENCONTRE en {index}")
                    self.df = pd.read_excel(self.path, header=index+1)
                    print(self.df.head(5))
                    self.df.rename(columns=str.lower, inplace=True)
                    break

    def __repr__(self):
        return f"Archivo {self.nombre} - Ubicacion: {self.path}"
    
    def getColumnaProductos(self):
        success = False
        listaNombres = []
        for nombre in Utils.getPosibles_nameNombre():
            try:
                listaNombres.append(list(self.df[nombre].array))
            except:
                continue
            else:
                success = True
                break
        return listaNombres
    
    