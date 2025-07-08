import flet as ft
from UI.view import View
from database.DAO import DAO
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.lat = 0
        self.long = 0
        self.shape = None
        self.mapStates = DAO.getter_idMapState()


    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        self._view.update_page()

        self.read_casellaLat_float()
        self.read_casellaLong_float()
        if self.shape is None:
            self._view.create_alert(f"selezionare shape")
            return

        self._model.build_graph(self.lat, self.long, self.shape)
        self._view.txt_result1.controls.append(ft.Text(self._model.grafo))

        topArchi, topNodi = self._model.get_dettagli()

        self._view.txt_result1.controls.append(ft.Text("\ntop archi: \n"))

        print(self.mapStates)
        for e in topArchi:
            print(e[0], type(e[0]))

            self._view.txt_result1.controls.append(ft.Text(f"{self.mapStates[e[0].state]} - {self.mapStates[e[1].state]}  peso: {e[2]['weight']}"))

        self._view.txt_result1.controls.append(ft.Text("\ntop nodi: \n"))

        for n in topNodi:
            self._view.txt_result1.controls.append(ft.Text(f"{self.mapStates[n.state]} grado: {self._model.grafo.degree[n]}"))

        self._view.btn_path.disabled = False

        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        self._model.calcola_bestpath()
        bestPath = self._model.bestPath
        bestScore = self._model.bestScore
        self._view.txt_result2.controls.append(ft.Text(f"punteggio ottimo: {bestScore}\nmiglior path: \n"))
        for e in bestPath:
            self._view.txt_result2.controls.append(ft.Text(f"{e[0]}"))
        self._view.update_page()


    def fill_ddshape(self):
        pass

    def read_casellaLat_float(self):
        valore = self._view.txt_latitude.value
        estremi = DAO.getter_estremi_lat()
        try:
            valore = float(valore)
            if estremi[0] <= valore <= estremi[1]:
                self.lat = valore
                print(f"durata: {self.lat} {type(valore)}")
                return True
            else:
                self._view.create_alert(f"inserire valore latitudine nel range {estremi}")
                return False
        except ValueError:
            self._view.create_alert("inserire valore valido")
            return False

    def read_casellaLong_float(self):
        valore = self._view.txt_longitude.value
        estremi = DAO.getter_estremi_long()
        try:
            valore = float(valore)
            if estremi[0] <= valore <= estremi[1]:
                self.long = valore
                print(f"durata: {self.long} {type(valore)}")
                return True
            else:
                self._view.create_alert(f"inserire valore longitudine nel range {estremi}")
                return False
        except ValueError:
            self._view.create_alert("inserire valore valido")
            return False

    def fill_dropdown(self):
        lista_opzioni = DAO.getter_shapes()
        for o in lista_opzioni:
            self._view.ddshape.options.append(ft.dropdown.Option(key=o,
                                                                  text=o,
                                                                  data=o,
                                                                  on_click=self.read_dropdown))

    def read_dropdown(self, e):
        self.shape = e.control.data
        print(f"valore letto: {self.shape} - {type(self.shape)}")

