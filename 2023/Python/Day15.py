import re
import time

class LensSolver:
    def __init__(self, filbane):
        self.filbane = filbane
        self.minne = [[] for _ in range(256)]

    def last_inn_data(self):
        with open(self.filbane, 'r') as fil:
            return fil.read()

    @staticmethod
    def beregn_hash(ordet):
        verdi = 0
        for c in ordet:
            verdi += ord(c)
            verdi *= 17
            verdi %= 256
        return verdi

    def del_en(self, data):
        return sum(self.beregn_hash(word) for word in data.split(','))

    def del_to(self, data):
        for tekst in data.split(','):
            etikett = re.search(r'\w+', tekst).group()
            hsh = self.beregn_hash(etikett)
            if '-' in tekst:
                indeks = self.finn_indeks(self.minne[hsh], etikett)
                if indeks >= 0:
                    self.minne[hsh].pop(indeks)
            elif '=' in tekst:
                fl = int(tekst[tekst.index('=') + 1:])
                indeks = self.finn_indeks(self.minne[hsh], etikett)
                if indeks >= 0:
                    self.minne[hsh][indeks] = (etikett, fl)
                else:
                    self.minne[hsh].append((etikett, fl))
        return sum((i + 1) * (j + 1) * fl for i, boks in enumerate(self.minne) for j, (_, fl) in enumerate(boks))

    @staticmethod
    def finn_indeks(lst, etikett):
        for i, (lbl, _) in enumerate(lst):
            if lbl == etikett:
                return i
        return -1

    def kjor(self):
        start_tid = time.time()
        data = self.last_inn_data()
        del1_resultat = self.del_en(data)
        del2_resultat = self.del_to(data)
        slutt_tid = time.time()
        totaltid = (slutt_tid - start_tid) * 1000
        return del1_resultat, del2_resultat, totaltid

if __name__ == '__main__':
    solver = LavaProductionSolver('input.txt')
    del1_resultat, del2_resultat, totaltid = solver.kjor()
    print(f"Svaret for del 1 er: {del1_resultat}")
    print(f"Svaret for del 2 er: {del2_resultat}")
    print(f"Tiden det tok er: {totaltid:.2f} millisekunder")
