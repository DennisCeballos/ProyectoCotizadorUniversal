# Clase para gestionar las fuentes de datos
import pandas as pd #nimodo i guess
from models.Utils import Utils

class FuenteDatos:
    # Inicializa la clase, inicializando un dataframe para el path que se haya entregado
    def __init__(self, _path):
        self.path = _path
        
        pos = self.path.rfind(".")
        self.nombre = self.path[:pos] #obtiene el nombre sin la extension de archivo
        
        self.nameNombre_preferido = None
        self.namePrecio_preferido = None

        posibles_nombre = Utils.getPosibles_nameNombre()
        posibles_precio = Utils.getPosibles_namePrecio()

        self.df = pd.read_excel(self.path)

        # bucle para encontrar la fila que contiene NOMBRE y PRECIO de producto
        # pero el nombre del producto puede ser varias palabras segun proveedor, por eso existe la lista de posibles_nombre
        # y el mismo caso para posibles_precio
        for index, row in self.df.iterrows():
            
            # obtener los elementos de la fila para comprobar si es el inicio o no de la tabla
            elementos_fila = []
            for palabra in row.array:
                elementos_fila.append( str(palabra).lower() )
            
            #print("elementos_fila> ", end="")
            #print(elementos_fila)

            #* se obtiene el name que utiliza este archivo para sus "nombres de productos" y para sus "precios de producto"
            self.nameNombre_preferido = [value for value in elementos_fila if value in posibles_nombre]
            self.namePrecio_preferido = [value for value in elementos_fila if value in posibles_precio]
            
            # se debe quedar en None si es que no hubo interseccion
            self.nameNombre_preferido = self.nameNombre_preferido.pop() if len(self.nameNombre_preferido)>0 else None
            self.namePrecio_preferido = self.namePrecio_preferido.pop() if len(self.namePrecio_preferido)>0 else None

            # si son diferentes de nulos significa que sI existen
            if ( self.nameNombre_preferido ) and (self.namePrecio_preferido):
                    #print(f"ENCONTRE en {index}")
                    self.df = pd.read_excel(self.path, header=index+1) # type: ignore
                    self.df.rename(columns=str.lower, inplace=True)
                    break
        #print(f"Numero de filas: {self.df.count()} de archivo {self.nombre}")

    def __repr__(self):
        return f"Archivo {self.nombre} - Ubicacion: {self.path}"
    
    def getColumnaNombreProductos(self):
        listaNombres = []
        listaNombres.append(list(self.df[self.nameNombre_preferido].array))
        return listaNombres
    
    def getColumnaPrecios(self):
        listaNombres = []
        listaNombres.append(list(self.df[self.nameNombre_preferido].array))
        return listaNombres
    
    #* Retorna un dataframe con los datos de la fuente
    # pero siguiendo la estructura de un models.Producto
    def getDataframeProductos(self):
        df = self.df.copy()

        if not self.nameNombre_preferido or not self.namePrecio_preferido:
            return None
        
        df.rename(columns={self.nameNombre_preferido: "nombre", # type: ignore
                           self.namePrecio_preferido: "precio"}, # type: ignore
                  inplace=True) # type: ignore
        
        columnas_conservar = ["nombre", "precio"]
        df = df[[*columnas_conservar]]
        
        df["origen"] = self.nombre

        return df
    
    