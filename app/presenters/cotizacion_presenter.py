# presenters/cotizacion_presenter.py
import pandas as pd
import os
from models.Producto import Producto
from models.FuenteData import FuenteDatos
from views.cotizador_view import CotizadorView
from models.Utils import Utils

class CotizacionPresenter:
    def __init__(self, view: CotizadorView):
        self.view = view
        self.opciones_productos = []
        self.productos_cotizacion = []
        self.lista_FuenteDatos:list[FuenteDatos] = []
        self.dataframe = None

    def cargar_datos(self):
        #* Cargar pandas dataframe para cada fuente de datos *

        # obtener la lista de ARCHIVOS de tipo excel
        current_path = str(os.getcwd())
        archivos = os.listdir(current_path)
        archivos = [f for f in archivos if os.path.isfile(current_path+'/'+f)]
        archivos_excel = [f for f in archivos if f.lower().find(".xls")>0 ] # solo archivos que tengan la extension xls

        # bucle para generar los dataframes por cada archivo
        for nombre_archivo in archivos_excel:
            self.lista_FuenteDatos.append( FuenteDatos(nombre_archivo) )
        
        # Comprobar lista de dataframse
        print(f"Numero de FuenteDatos creados>{len(self.lista_FuenteDatos)}")

        self.dataframe = pd.concat( [fuente.getDataframeProductos() for fuente in self.lista_FuenteDatos], ignore_index=True)
        print(self.dataframe.head(5))
        print(self.dataframe.size)
        print(self.dataframe["origen"].describe())

        #
        #* Configurar las interacciones con los botones en la vista
        #
        self.view.set_buscar_callback(self.on_buscar)

    def on_buscar(self):
        # Generar la lista de opciones similares a la palabra a Buscar
        datos_mostrar: list[Producto] = []
        palabraBuscar = self.view.entryBuscador.get()


    '''
    def fuzzy_filter(self, query):
        if not query:
            return self.options[:15]

        query = query.lower().strip()

            # Optional: fallback to fast substring match for very short queries
        if len(query) < 3:
            return [opt for opt in self.options if query in opt.lower()][:15]

        # Use rapidfuzz to get matches with similarity score
        matches = process.extract(
            query,
            self.options,
            scorer= fuzz.partial_token_set_ratio,  # good for word order variation
            limit=10  # limit for performance
        )

        rpta = matches[:10]
        print(rpta)
        return [match for match, score, _ in rpta if score >= 50]
    '''