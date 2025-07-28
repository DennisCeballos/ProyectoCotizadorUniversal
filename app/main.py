# main.py
from views.main_view import MainView
from presenters.cotizacion_presenter import CotizacionPresenter

def main():
    view = MainView()
    cotizacion_presenter = CotizacionPresenter(view)
    cotizacion_presenter.cargar_datos()

    view.mainloop()

if __name__ == "__main__":
    main()
