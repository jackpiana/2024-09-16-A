
from database.DAO import DAO
import networkx as nx




class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.mapStati = DAO.getter_idMapState()
        self.bestScore = 0
        self.bestPath = []


    def build_graph(self, minLat, minLong, shape):
        self.grafo.clear()

        nodes = DAO.getter_nodes(minLat, minLong, shape)
        self.grafo.add_nodes_from(nodes)

        confini = DAO.getter_confini()
        for n1 in nodes:
            for n2 in nodes:
                if n1 > n2:
                    if (n1.state.upper(), n2.state.upper()) in confini:
                        self.grafo.add_edge(n1, n2, weight= (n1.pesoNodo + n2.pesoNodo))

        print(self.grafo)



    def get_dettagli(self):
        nodi = list(self.grafo.nodes)
        archi = list(self.grafo.edges(data=True))
        nodi_ordinati = sorted(nodi, key=lambda nodo: self.grafo.degree[nodo], reverse=True)
        archi_ordinati = sorted(archi, key=lambda x: x[2]['weight'], reverse=True)
        return archi_ordinati[:5], nodi_ordinati[:5]


    def calcola_bestpath(self):
        print("inizio ricorsione...")
        self.bestPath = []
        self.bestScore = 0
        for n in list(self.grafo.nodes):
            stato = self.mapStati[n.state]
            self.ricorsione([(stato, n)])
        print("fine ricorsione")

    def ricorsione(self, parziale):
        rimanenti = self.calcola_rimanenti(parziale)
        if rimanenti == []:
            return
        else:
            rimanenti = rimanenti.copy()
            for n in rimanenti:
                parziale.append(n)
                parziale = parziale.copy()
                self.calcolaPunteggio(parziale)
                self.ricorsione(parziale)
                parziale.pop()

    def calcola_rimanenti(self, parziale):
        rimanenti = []
        statoStart = parziale[-1][0]
        nodoStart = parziale[-1][1]
        viciniId = list(self.grafo.neighbors(nodoStart))
        for nodoVicino in viciniId:
            statoVicino = self.mapStati[nodoVicino.state]
            if statoVicino.densita_popolazione() > statoStart.densita_popolazione():
                rimanenti.append((statoVicino, nodoVicino))
        return rimanenti

    def calcolaPunteggio(self, parziale):
        pesoTot = 0
        distanceTot = 0
        for i in range(len(parziale)-1):
            s1 = parziale[i][0]
            s2 = parziale[i+1][0]
            print(s1, s2)

            n1 = parziale[i][1]
            n2 = parziale[i+1][1]
            print(n1, n2)

            try:
                pesoTot += self.grafo[n1][n2]['weight']
            except KeyError:
                print("keyError")
            distanceTot += s1.distance_HV(s2)

        score = pesoTot / distanceTot
        print(score)
        if score > self.bestScore:
            self.bestScore = int(score)
            self.bestPath = parziale
        return score


if __name__ == '__main__':
    m = Model()
    m.build_graph(41, -100, 'sphere')
    m.calcola_bestpath()
    print(m.bestPath)




