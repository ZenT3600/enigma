class Alfabeto:
    """
    Classe: Alfabeto
    Attributi:
        tasti (dizionario indice:chiave)
        tasti_inversi (dizionario chiave:indice)
    Metodi:
        None
    """

    def __init__(self, caratteri):
        self.caratteri = caratteri
        for carattere in caratteri:
            if caratteri.count(carattere) > 1:
                raise ValueError("L'alfabeto non può contenere doppioni")

    def lunghezza(self):
        return len(self.caratteri)

    def isValid(self, carattere):
        return carattere in self.caratteri

    def indice(self, carattere):
        return self.caratteri.index(carattere)

    def carattere(self, indice):
        return self.caratteri[indice]


class Rotore:
    def __init__(self, connessioni):
        self.connessioni = connessioni
        self.rotazioni = 0

    def ruota(self, n):
        temp = self.connessioni[0:n]
        size = len(self.connessioni)
        for i in range(n, size):
            self.connessioni[i - n] = self.connessioni[i]
        for i in range(0, len(temp)):
            self.connessioni[size - n + i] = temp[i]
        self.rotazioni = (self.rotazioni + n) % len(self.connessioni)

    def restituisci_destra(self, indice):
        return self.connessioni[indice]

    def restituisci_sinistra(self, indice):
        return self.connessioni.index(indice)


class Riflessore:
    """
    Classe: Riflessore
    Attributi:
        connessioni (connessioni interne del riflessore)
    Metodi:
        rifletti (riflette un carattere ad un determinato indice basandosi sulle proprio connessioni interne)
    """

    def __init__(self, connessioni):
        self.connessioni = connessioni

    def rifletti(self, indice):
        """
        Metodo: rifletti
        Descrizione: riflette un carattere ad un determinato indice basandosi sulle proprio connessioni interne
        Parametri: indice
        """
        return indice + self.connessioni[indice]


class Enigma:
    """
    Classe: Enigma
    Attributi:
        shift (posizione di partenza dei rotori)
        tastiera (oggetto tastiera)
        rotori (lista contenente 'n' oggetti rotore)
        riflessore (oggetto riflessore)
    Metodi:
        configura (riconfigura la posizione dei rotori)
        cifra (cifra o decifra un messaggio, senza bisogno che il messaggio sia dichiarato leggibile o cifrato)
    """

    def __init__(self, alfabeto, shift, rotori, riflessore):
        self.alfabeto = alfabeto
        self.rotori = rotori
        self.rotori[0].ruota(shift[0])
        self.rotori[1].ruota(shift[1])
        self.rotori[2].ruota(shift[2])
        self.riflessore = riflessore
        self.scatti = [0, 0, 0]
        self.configura(shift)

    def configura(self, shift):
        shift = [int(s) for s in shift]
        for i, s in enumerate(shift):
            while self.rotori[i].rotazioni != s:
                self.rotori[i].ruota(1)
        self.scatti = [0, 0, 0]

    def cifra(self, msg):
        """
        Metodo: cifra
        Descrizione: cifra o decifra un messaggio, senza bisogno che il messaggio sia dichiarato leggibile o cifrato
        Parametri: msg
        """

        crt = []
        for m in msg:
            if self.alfabeto.isValid(m):
                c = self.alfabeto.indice(m)

                for r in self.rotori:
                    c = r.restituisci_destra(c)

                c = self.riflessore.rifletti(c)

                for r in reversed(self.rotori):
                    c = r.restituisci_sinistra(c)

                crt.append(self.alfabeto.carattere(c))

                self.rotori[0].ruota(1)
                self.scatti[0] += 1
                if self.scatti[0] % self.alfabeto.lunghezza() == 0:
                    self.rotori[1].ruota(1)
                    self.scatti[1] += 1
                    if self.scatti[1] % self.alfabeto.lunghezza() == 0:
                        self.rotori[2].ruota(1)
                        self.scatti[2] += 1

            else:
                crt.append(m)

        # print(self.scatti)
        return "".join(crt)
