import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_collegamenti(self, e):
        """
        Funzione che controlla prima se il valore dell'importo inserito sia valido (es. non deve essere una stringa) e
        poi popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Filiali presenti
        * Numero di Collegamenti
        * Lista di Collegamenti che superano l'importo indicato come soglia
        """
        valore_str = self._view.importo_medio_minimo.value
        if valore_str is None or valore_str == "":
            self._view.show_alert("Inserisci un valore numerico!")
            return
        try:
            soglia = float(valore_str)
        except ValueError:
            self._view.show_alert("Inserisci un valore numerico!")
            return


        self._model.costruisci_grafo(soglia)
        self._view.lista_visualizzazione.controls.clear()
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di filiali: {self._model.get_num_nodes()}")
        )
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di collegamenti: {self._model.get_num_edges()}")
        )
        self._view.lista_visualizzazione.controls.append(ft.Text(f"Collegamenti che superano la media inserita dall'utente:"))
        for e1,e2,data in self._model.get_all_edges():
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f" {e1}-{e2} --- Weight: {data['weight']}")
            )
        self._view.update()

