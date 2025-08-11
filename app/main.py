# main.py
from views.cotizador_view import CotizadorView
from presenters.cotizacion_presenter import CotizacionPresenter

def main():
    view = CotizadorView()
    cotizacion_presenter = CotizacionPresenter(view)
    cotizacion_presenter.cargar_datos()

    view.mainloop()

if __name__ == "__main__":
    main()
