# presenters/cotizacion_presenter.py
import pandas as pd
import numpy as np
import openpyxl
from datetime import datetime
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
        current_path = str(os.path.dirname(os.path.realpath(__file__)))
        print(current_path)
        current_path = current_path[: current_path.rfind('\\')]
        print(current_path)
        current_path = current_path[: current_path.rfind('\\')]
        print(current_path)
        archivos = os.listdir(current_path)
        archivos = [f for f in archivos if os.path.isfile(current_path+'/'+f)]
        archivos_excel = ["\\".join( [current_path,f] ) for f in archivos if f.lower().find(".xls")>0 ] # solo archivos que tengan la extension xls

        # bucle para generar los dataframes por cada archivo
        for nombre_archivo in archivos_excel:
            self.lista_FuenteDatos.append( FuenteDatos(nombre_archivo) )
        
        # Comprobar lista de dataframse
        print(f"Numero de FuenteDatos creados > {len(self.lista_FuenteDatos)}")

        self.dataProductosTodos = pd.concat( [fuente.getDataframeProductos() for fuente in self.lista_FuenteDatos], ignore_index=True)

        #
        #* Configurar las interacciones con los botones en la vista
        #
        self.view.set_buscar_callback(self.on_buscar)
        self.view.set_agregar_callback(self.on_agregar)
        self.view.set_copiar_callback(self.on_copiarPortapapeles)
        self.view.set_exportar_callback(self.on_exportarExcel)
        self.view.set_eliminar_callback(self.on_eliminar)

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

    def on_agregar(self):
        # Verificar que se ha seleccionado alguna opcion
        try:
            seleccion = self.view.tablaOpciones.selection()[0]
        except IndexError:
             print("No se ha seleccionado ninguna opcion")
             return
        
        # proceso necesario para obtener el valor como tal
        seleccion = self.view.tablaOpciones.item(seleccion)
        seleccion = seleccion.get("values")
        print("Agregando: ")
        print(seleccion)

        #insertar los datos en la tabla final
        self.view.tablaCotizaciones.insert("", 'end',values=seleccion) # type: ignore
    
    def on_eliminar(self):
        # Verificar que se ha seleccionado alguna opcion
        try:
            seleccion = self.view.tablaCotizaciones.selection()[0]
        except IndexError:
             print("No se ha seleccionado ninguna opcion")
             return
        
        # proceso necesario para obtener el valor como tal
        #seleccion = self.view.tablaCotizaciones.item(seleccion)
        #seleccion = seleccion.get("values")
        print("Eliminando de Cotizacion: ")
        print(seleccion)

        # eliminar dicho dato de la tabla final
        self.view.tablaCotizaciones.delete(seleccion) # type: ignore

    def on_copiarPortapapeles(self):
        filas = []

        # guardar la cabecera de la tabla
        headers = [self.view.tablaCotizaciones.heading(col)["text"] for col in self.view.tablaCotizaciones["columns"]]
        filas.append('\t'.join(headers))

        for item in self.view.tablaCotizaciones.get_children():
            values = self.view.tablaCotizaciones.item(item)["values"]
            row = '\t'.join(str(value) for value in values)
            filas.append(row)

        clipboard_data = '\n'.join(filas)

        # copiar al portapapeles
        self.view.clipboard_clear()
        self.view.clipboard_append(clipboard_data)
        self.view.update()  # mantiene el clipboard despues de salir del form
        print("Data de COtizacion guardada en el portapapeles")

    def on_exportarExcel(self):
        # crear un nuevo excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Data Cotizacion" # type: ignore

        # obtener los datos de cabecera
        headers = [self.view.tablaCotizaciones.heading(col)["text"] for col in self.view.tablaCotizaciones["columns"]]
        ws.append(headers) # type: ignore

        # agregar los datos de las filas
        for item in self.view.tablaCotizaciones.get_children():
            values = self.view.tablaCotizaciones.item(item)["values"]
            ws.append(values) # type: ignore

        # guardar en un archivo temporal
        app_dir = os.getcwd()
        # Generate formatted date-time string
        hora_actual = datetime.now()
        hora_formateado = hora_actual.strftime("Cotizacion Resumen_%d_%B_%y-%H_%M.xlsx")  # e.g., Cotizacion_07_August_25_14_45.xlsx
        file_path = os.path.join(app_dir, hora_formateado)
        wb.save(file_path)

        # abrir el archivo con la aplicacion default
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            #elif os.name == 'posix':  # macOS or Linux
            #    subprocess.call(('open' if sys.platform == 'darwin' else 'xdg-open', file_path))
        except Exception as e:
            print("Error. No se pudo abrir el archivo:", e)

        print(f"Archivo exportado en {file_path}")