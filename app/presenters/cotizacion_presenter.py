# presenters/cotizacion_presenter.py
import pandas as pd
import numpy as np
import os
import re
from rapidfuzz import fuzz, process
from models.Producto import Producto
from models.FuenteData import FuenteDatos
from views.cotizador_view import CotizadorView
from models.Utils import Utils

class CotizacionPresenter:
    def __init__(self, view: CotizadorView):
        self.view = view
        self.productos_cotizacion = []
        self.lista_FuenteDatos:list[FuenteDatos] = []
        
        self.opciones_productos = None
        self.dataProductosTodos: pd.DataFrame = None  # type: ignore

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

        self.dataProductosTodos = pd.concat( [fuente.getDataframeProductos() for fuente in self.lista_FuenteDatos], ignore_index=True)

        #
        #* Configurar las interacciones con los botones en la vista
        #
        self.view.set_buscar_callback(self.on_buscar)

    def on_buscar(self):
        #* Generar la lista de opciones similares a la palabra a Buscar
        # obtener la palabra desde la visata
        palabra_buscar = self.view.entryBuscador.get()
        palabra_buscar = palabra_buscar.lower().strip()

        # tokenizar el query (e.g., "lili 5mg" → ['lili', '5mg'])
        query_tokens = re.findall(r"\w+", palabra_buscar)

        # extraer lista de nombres para hacer la busqueda difusa
        nombres = self.dataProductosTodos["nombre"].tolist()
        
        # filtro 1: encontrar elementos que contengan cualquiera de los tokens de la palabra
        contiene_tokens = self.dataProductosTodos[
        self.dataProductosTodos["nombre"].str.lower().apply(
            lambda nombre: any(token in nombre for token in query_tokens)
        )
        ].copy()

        # filtro 2: fuzzy match with top scores
        matches = process.extract(
            palabra_buscar,
            nombres,
            scorer=fuzz.partial_token_set_ratio,
            #limit=max_results * 2  # get more to merge
        )

        # filtrar por score minimo
        matches_filtrados = [(match, score) for match, score, _ in matches if score >= 50]

        # Crear DataFrame filtrado de los matches
        df_fuzzy = self.dataProductosTodos[self.dataProductosTodos["nombre"].isin([match for match, _ in matches_filtrados])].copy()

        # Añadir columna de score
        score_map = {match: score for match, score in matches_filtrados}
        df_fuzzy["score"] = df_fuzzy["nombre"].map(score_map)

        # Elementos de fuzzy pueden estar ya en contiene_tokens
        df_combinado = pd.concat([contiene_tokens, df_fuzzy]).drop_duplicates(subset="nombre")

        # Si no tiene score (viene del contains), lo ponemos en 100 para que tenga alta prioridad
        df_combinado["score"] = df_combinado["score"].fillna(100)

        # Ordenar y limitar
        df_combinado = df_combinado.sort_values(by="score", ascending=False)
        print(df_combinado)

        # Ordenar DE ACUERDO A ENCONTRAR LA QUERY
        # Compute position of query in 'nombre' (lowercase version)
        positions = df_combinado["nombre"].str.lower().str.find(palabra_buscar)

        # Assign a large value (e.g., np.inf) to names that do not contain the query
        positions = positions.where(positions != -1, np.inf)

        # Add the position as a temporary column
        df_combinado["query_position"] = positions

        # Sort by query position and drop temporary column
        df_combinado = df_combinado.sort_values(by="query_position", ascending=False).drop(columns="query_position")

        #* Insertar los filtrados en el treeview en la vista
        #limpiar la tabla
        self.view.tablaOpciones.delete(*self.view.tablaOpciones.get_children())

        #insertar los datos
        for index, row in df_combinado.iterrows():
            valor = (row["nombre"], row["precio"], row["origen"])
            self.view.tablaOpciones.insert("", index=0,values=valor)
