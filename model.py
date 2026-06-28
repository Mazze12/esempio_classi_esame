import copy
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._artisti = DAO.getAllArtisti()
        self._idMap={}
        for a in self._artisti:
            self._idMap[a.ArtistId] = a
        self._grafo = nx.DiGraph()

    def getAllGeneri(self):
        return DAO.getAllGeneri()

    def getAllArtisti(self):
        return DAO.getAllArtisti()

    def getAllNodes(self, genere):
        return DAO.getAllNodes(genere)

    def getAllEdges(self, genere):
        return DAO.getAllEdges(genere, self._idMap)

    def buildGraph(self, genere):
        self._grafo.clear()
        nodi = self.getAllNodes(genere)
        archi = self.getAllEdges(genere)
        self._grafo.add_nodes_from(nodi)
        for a in archi:
            self._grafo.add_edge(a.nodoSorgente, a.nodoDestinazione, weight = a.pesoArco)

        return len(self._grafo.nodes), len(self._grafo.edges)


    def influenzaArtista(self,a):
        peso_uscente =0
        peso_entrante = 0
        influenza = 0
        for u, v, attributi in self._grafo.out_edges(a, data=True):
            peso_uscente += attributi["weight"]
        for u, v, attributi in self._grafo.in_edges(a, data=True):
            peso_entrante += attributi["weight"]

        influenza = peso_uscente-peso_entrante
        return influenza

    def getTopArtista(self, genere):
        nodi = self.getAllNodes(genere)
        influenzaTop=0
        topArtista = 0
        for a in nodi:
            i = self.influenzaArtista(a)
            if i > influenzaTop:
                topArtista = a
                influenzaTop = i
        return topArtista, influenzaTop

    def getTop5(self, genere):
        archi = self.getAllEdges(genere)
        archiOrdinati = sorted(archi, key = lambda i: i.pesoArco, reverse = True)
        return archiOrdinati[:5]

    def getPesoArco(self, u, v):
        return self._grafo[u][v]["weight"]

    def score(self, parziale):
        score = 0
        for i in range(len(parziale)-1):
            pesoArco = self.getPesoArco(parziale[i], parziale[i+1])
            score += pesoArco

        return score

    def getPath(self, v0):
        #Inizializzo le variabili generiche
        parziale = [v0]
        self._bestPath = []
        self._costoCammino = -1

        #Esploriamo i vicini del nodo di partenza v0
        #Con grafo diretto --> successors()
        #Con grafo non diretto --> neighbors
        for v in self._grafo.successors(v0):
            parziale.append(v)
            #Avvio la ricorsione
            self.ricorsione(parziale)
            #Effettuo il meccanismo di backtracking: rimuoviamo il vicino per trovare le altre strade del ciclo
            parziale.pop()
        return self._bestPath , self._costoCammino

    def ricorsione(self, parziale):
        #Verifico se la soluzione parziale è meglio del BestCase utilizzando la funzione score
        punteggio_attuale = self.score(parziale)
        if punteggio_attuale > self._costoCammino:
            self._bestPath = copy.deepcopy(parziale)
            self._costoCammino = punteggio_attuale

        #Verifico quindi se ha senso continuare ad andare avanti con la ricerca di un cammino ottimale - Nel caso ci
        #fossero vincoli di terminazione

        #Effettuo quindi il mio meccanismo di ricorsione per lavorare sul nodo successivo
        nodo_corrente = parziale[-1]
        #Recupero i vicini dell'ultimo modo inserito all'interno della mia lista parziale
        for v in self._grafo.successors(nodo_corrente):
            if v not in parziale:
                #verifico che il peso del potenziale arco che andremo ad aggiungere sia maggiore del precedente
                pesoE = self._grafo[nodo_corrente][v]["weight"]
                nodo_precedente = parziale[-2]
                pesoP = self._grafo[nodo_precedente][nodo_corrente]["weight"]
                if pesoE>pesoP:
                    parziale.append(v)
                    self.ricorsione(parziale)
                    parziale.pop()












