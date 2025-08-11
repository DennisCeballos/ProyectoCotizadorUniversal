import tkinter as tk
from tkinter import ttk, Button, Canvas

class CotizadorView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Cotizaciones")
        self.geometry("650x800")
        self.resizable(False, False)
        
        self.configure(bg = "#DBDBDB")

        self.canvas = Canvas(
            bg = "#DBDBDB",
            width = 650,
            height = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x=0, y=0)

        #
        #* Seccion de busqueda de producto
        #
        self.canvas.create_text(
            40.0,
            40.0,
            anchor="nw",
            text="Nombre Producto",
            fill="#000000",
            font=("IstokWeb Regular", 12 * -1)
        )
        
        self.entryBuscador = tk.Entry()
        self.entryBuscador.place(
            x=40.0,
            y=60.0,
            width=470.0,
            height=30.0
        )
        
        self.btnBuscar = Button(
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("btnBuscar clicked"),
            relief="flat",
            text="Buscar"
        )
        self.btnBuscar.place(
            x=530.0,
            y=60.0,
            width=70.0,
            height=30.0
        )

        #
        #* Seccion de Opciones
        #
        self.canvas.create_text(
            40.0,
            110.0,
            anchor="nw",
            text="Opciones",
            fill="#000000",
            font=("IstokWeb Regular", 12 * -1)
        )

        self.tablaOpciones = ttk.Treeview(show="headings")
        self.tablaOpciones["columns"] = ["descripcion", "precio", "origen"]

        #self.tablaOpciones.column("#0")
        self.tablaOpciones.column("descripcion", width=300)
        self.tablaOpciones.column("precio", width=70-1)
        self.tablaOpciones.column("origen", width=95-1)

        #self.tablaOpciones.heading("#0", text="#")
        self.tablaOpciones.heading("descripcion", text="Nombre")
        self.tablaOpciones.heading("precio", text="Precio S/.")
        self.tablaOpciones.heading("origen", text="Origen")

        self.tablaOpciones.place(
            x=40, y=130,
            width=470, height=270
        )

        self.btnAgregar = Button(
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("btnAgregar clicked"),
            relief="flat",
            text="Agregar"
        )
        self.btnAgregar.place(
            x=530.0, y=130.0,
            width=70.0, height=30.0
        )
        
        #
        #* Seccion de Cotizaciones
        #
        self.canvas.create_text(
            40.0,
            428.0,
            anchor="nw",
            text="Cotizaciones",
            fill="#000000",
            font=("IstokWeb Regular", 12 * -1)
        )

        self.tablaCotizaciones = ttk.Treeview(show="headings")
        self.tablaCotizaciones["columns"] = ["descripcion", "precio", "origen"]

        #self.tablaOpciones.column("#0")
        self.tablaCotizaciones.column("descripcion", width=300)
        self.tablaCotizaciones.column("precio", width=90)
        self.tablaCotizaciones.column("origen", width=120-1)

        #self.tablaOpciones.heading("#0", text="#")
        self.tablaCotizaciones.heading("descripcion", text="Nombre")
        self.tablaCotizaciones.heading("precio", text="Precio S/.")
        self.tablaCotizaciones.heading("origen", text="Origen")

        self.tablaCotizaciones.place(
            x=40, y=450,
            width=560, height=200
        )

        self.btnEliminar = Button(
            text="Eliminar",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("btnEliminar clicked"),
            relief="flat"
        )
        self.btnEliminar.place(
            x=40.0, y=665.0,
            width=70.0, height=30.0
        )

        #
        #* Seccion Final de Exportar a Excel
        #
        self.canvas.create_text(
            40.0,
            725.0,
            anchor="nw",
            text="Exportar",
            fill="#000000",
            font=("IstokWeb Regular", 12 * -1)
        )

        self.btnCopiar = Button(
            text="Copiar al Portapapeles",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("btnCopiar al Portapapeles"),
            relief="flat"
        )
        self.btnCopiar.place(
            x=40.0, y=745.0,
            width=200.0, height=30.0
        )

        self.btnExportar = Button(
            text="Exportar Excel",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("btnExportar Excel"),
            relief="flat"
        )
        self.btnExportar.place(
            x=255.0, y=745.0,
            width=200.0, height=30.0
        )
        

        #
        # configuraciones extras
        #
        def entry_ctrl_bs(event):
            ent = event.widget
            end_idx = ent.index(tk.INSERT)
            start_idx = ent.get().rfind(" ", None, end_idx)
            ent.selection_range(start_idx, end_idx)
        self.entryBuscador.bind('<Control-BackSpace>', entry_ctrl_bs)

    def set_buscar_callback(self, callback):
        self.btnBuscar.config(command=callback)
        self.entryBuscador.bind('<Return>', lambda x: callback()) #hay un lambda x porque BIND siempre pasa un parametro "event" que no se requiere en la funcion callback (no tiene parametros)
    
    def set_agregar_callback(self, callback):
        self.btnAgregar.config(command=callback)
        self.tablaOpciones.bind('<Double 1>', lambda x: callback())
        self.tablaOpciones.bind('<Return>', lambda x: callback())
    
    def set_eliminar_callback(self, callback):
        self.btnEliminar.config(command=callback)
        self.tablaCotizaciones.bind('<Return>', lambda x: callback())
        self.tablaCotizaciones.bind('<Delete>', lambda x: callback())
        self.tablaCotizaciones.bind('<BackSpace>', lambda x: callback())
    
    def set_copiar_callback(self, callback):
        self.btnCopiar.config(command=callback)

    def set_exportar_callback(self, callback):
        self.btnExportar.config(command=callback)