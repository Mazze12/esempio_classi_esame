import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genere = None
        self._artista=None

    def fillDDGenre(self):
        generi = self._model.getAllGeneri()
        for g in generi:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(data = g,
                                   key = g.Name,
                                   on_click = self._choiceGenere)
            )

    def _choiceGenere(self, e):
        self._genere = e.control.data
        print(f"Hai scelto il genere: {self._genere.Name}")


    def handleCreaGrafo(self, e):
        if self._genere is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Devi definire un genere per il quale filtrare i risultati", color="red", weight = "bold")
            )
            self._view.update_page()
        # Arrivti qua il genere è stato correttamente inserito quindi creo il grafo
        nNodes, nEdges = self._model.buildGraph(self._genere)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Struttura del grafo: ", color="green", weight="bold"))
        self._view.txt_result.controls.append(
            ft.Text(f"{nNodes} nodi \n {nEdges} archi"))
        self._view.update_page()

        # Stampo i vari nodi del grafo nel dettaglio identificando i vari nodi
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo è strutturato nel seguente modo: ", color="green", weight="bold"))
        for u,v, attributi in self._model._grafo.edges(data = True):
            self._view.txt_result.controls.append(
                ft.Text(f"{u.Name} --> {v.Name}: {attributi['weight']}")
            )
        self._view.update_page()
        """ Oppure:
        archi = self._model.getAllEdges(self._genere)
        for a in archi:
            self._view.txt_result.controls.append(
                    ft.Text(f"{a.nodoSorgente.Name} --> {a.nodoDestinazione.Name}: {a.pesoArco}")
                )
        self._view.update_page()"""
        topArtista, influenzaTop = self._model.getTopArtista(self._genere)
        self._view.txt_result.controls.append(
            ft.Text(f"\n L'artista con la maggior influenza è:", color="green", weight="bold")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"{topArtista.Name} con un'influenza di {influenzaTop}")
        )
        self._view.update_page()

        # Stampo i primi 5 archi per peso
        self._view.txt_result.controls.append(
            ft.Text(f"I 5 archi con peso maggiore sono: ", color="green", weight="bold"))
        topArchi = self._model.getTop5(self._genere)
        for a in topArchi:
            self._view.txt_result.controls.append(
                ft.Text(f"{a.nodoSorgente.Name} --> {a.nodoDestinazione.Name}: {a.pesoArco}")
            )
        self._view.update_page()

        #Riempio il secondo dropdown
        artisti = self._model.getAllNodes(self._genere)
        for a in artisti:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(data = a,
                                   key =a.Name,
                                   on_click = self._choiceArtista)
            )
        self._view.update_page()

    def _choiceArtista(self,e):
        self._artista = e.control.data
        print(f"Hai selezionato l'artista: {self._artista.Name}")



    def handleCammino(self,e):
        self._view.txt_result.controls.clear()
        if self._artista is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Devi definire un artista per il quale filtrare i risultati", color="red", weight="bold")
            )
            self._view.update_page()

        #Cerco il cammino ottimo
        bestPath, costoCammino = self._model.getPath(self._artista)

        self._view.txt_result.controls.append(
            ft.Text(f"Il cammino con costo massimo che parte dal nodo {self._artista.Name} ha costo pari a {costoCammino}", color = "green", weight = "bold")
        )
        for i in range(len(bestPath)-1 ):
            costo = self._model.getPesoArco(bestPath[i], bestPath[i+1])
            self._view.txt_result.controls.append(
                ft.Text(f"{bestPath[i].Name} --> {bestPath[i+1].Name}: {costo}")
            )
        self._view.update_page()
