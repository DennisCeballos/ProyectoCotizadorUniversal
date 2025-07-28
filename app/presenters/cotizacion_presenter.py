# presenters/cotizacion_presenter.py
import pandas as pd
import os
from models.producto import Producto
from models.FuenteData import FuenteDatos

class CotizacionPresenter:
    def __init__(self, view):
        self.view = view
        self.productos = []

    def cargar_datos(self):
        posibles_nombre = ["nombre", "descripcion", "presentacion"]
        posibles_precio = ["precio", "costo"]
        
        #* Cargar pandas dataframe para cada fuente de datos *
        lista_FuenteDatos:list[FuenteDatos] = []

        # obtener la lista de ARCHIVOS de tipo excel, etc 
        current_path = str(os.getcwd())
        archivos = os.listdir(current_path)
        archivos = [f for f in archivos if os.path.isfile(current_path+'/'+f)]
        archivos_excel = [f for f in archivos if f.lower().find(".xls")>0 ] # solo archivos que tengan la extension xls

        # bucle para generar los dataframes por cada archivo
        for nombre_archivo in archivos_excel:
            lista_FuenteDatos.append( FuenteDatos(nombre_archivo) )
            

        # Comprobar lista de dataframse
        print(f"Numero de FuenteDatos creados>{len(lista_FuenteDatos)}")

        #* Generar la lista de nombres para el comboBox
        nombres_productos = []

        for fuente in lista_FuenteDatos:
            nombres_productos.extend(fuente.getColumnaProductos())
        
        nombres_productos = fuente.getColumnaProductos()

        self.view.ComboBoxProducto['values'] = ["Hola", "El", "pepe"]
        print(nombres_productos)
        self.view.ComboBoxProducto.current()

        self.productos = [
            Producto("Laptop HP", 2500, "Proveedor A"),
            Producto("Laptop Lenovo", 2300, "Proveedor B")
        ]

        #self.mostrar_en_vista()

    def mostrar_en_vista(self):
        pass
        '''
        self.view.cotizacion_listbox.delete(0, 'end')
        for p in self.productos:
            self.view.cotizacion_listbox.insert('end', str(p))
        '''


if __name__ == "__main__":
    presentarPrueba = CotizacionPresenter(None)
    presentarPrueba.cargar_datos()