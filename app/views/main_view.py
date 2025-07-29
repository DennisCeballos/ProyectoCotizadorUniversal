# views/main_view.py
import tkinter as tk
from tkinter import ttk, Button, Canvas
from models.Utils import SearchableComboBox

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Cotizaciones")
        self.geometry("650x436")
        self.resizable(False, False)
        
        self.configure(bg = "#DBDBDB")

        self.canvas = Canvas(
            bg = "#DBDBDB",
            height = 436,
            width = 650,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x=0, y=0)

        options = ["Apple", "Banana", "Cherry", "Date", "Grapes", "Kiwi", "Mango", "Orange", "Peach", "Pear"]

        self.combo = SearchableComboBox(self, options)
        self.combo.place(y=30, x=20)
        
        self.canvas.create_rectangle(
            40.0,
            130.0,
            510.0,
            330.0,
            fill="#FFFFFF",
            outline="")

        self.eleccion = tk.StringVar()
        self.ComboBoxProducto = ttk.Combobox(width=40, height=30, textvariable=self.eleccion)
        self.ComboBoxProducto.place(x=40,y=60)
        self.ComboBoxProducto['values'] = (' January', 
                          ' February',
                          ' March',
                          ' April',
                          ' May',
                          ' June',
                          ' July',
                          ' August',
                          ' September',
                          ' October',
                          ' November',
                          ' December')

        '''
        self.canvas.create_rectangle(
            40.0,
            60.0,
            350.0,
            90.0,
            fill="#FFFFFF",
            outline="")
        '''

        self.canvas.create_text(
            40.0,
            40.0,
            anchor="nw",
            text="Nombre Producto",
            fill="#000000",
            font=("IstokWeb Regular", 12 * -1)
        )

        self.canvas.create_text(
            40.0,
            346.0,
            anchor="nw",
            text="Exportar",
            fill="#000000",
            font=("IstokWeb Regular", 12 * -1)
        )

        self.canvas.create_text(
            40.0,
            110.0,
            anchor="nw",
            text="Cotizaciones",
            fill="#000000",
            font=("IstokWeb Regular", 12 * -1)
        )

        self.button_1 = Button(
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat",
            text="Agregar"
        )
        self.button_1.place(
            x=368.0,
            y=59.0,
            width=70.0,
            height=30.0
        )

        self.button_2 = Button(
            text="Regresar",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(
            x=530.0,
            y=128.0,
            width=70.0,
            height=30.0
        )

        self.button_3 = Button(
            text="Exportar Excel",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.button_3.place(
            x=40.0,
            y=366.0,
            width=200.0,
            height=30.0
        )

        self.button_4 = Button(
            text="Eliminar",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        self.button_4.place(
            x=530.0,
            y=168.0,
            width=70.0,
            height=30.0
        )