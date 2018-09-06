from random import randint

MEJNA = '#'
PRAZNA = '0'
ZADETA_BOMBA = 'B'
NEVELJAVNA_POTEZA = '*'

class Polje:
    def __init__(self, vrstica, stolpec):
        self.vrstica = vrstica
        self.stolpec = stolpec
        self.oznacena = False
        self.sosednje_bombe = 0

    def __repr__(self):
        return 'Polje({0}, {1})'.format(
            self.vrstica, self.stolpec
        )

class Plosca:
    def __init__(self, visina=8, sirina=8, st_bomb=10):
        self.visina = visina
        self.sirina = sirina
        self.st_bomb = st_bomb
        
        self.polja = []
        for vrstica in range(self.visina):
            vrstica_polj = []
            for stolpec in range(self.sirina):
                Polje(vrstica, stolpec)
                vrstica_polj.append(Polje(vrstica, stolpec))
            self.polja.append(vrstica_polj)

        self.bombe = []
        self.odkriti = []
        self.oznaceni =[]


        self.poteza = 0
        self.st_oznacenih = 0

    def __repr__(self):
        return 'Plosca(visina={}, sirina={}, bombe={})'.format(
            self.visina, self.sirina, self.bombe
        )


    def postavi_bombe(self):
        for n in range(self.st_bomb):
            while True:
                x = randint(0, self.visina - 1)
                y = randint(0, self.sirina - 1)
                if self.polja[x][y] in self.odkriti:
                    pass
                elif self.polja[x][y].sosednje_bombe == 0:
                    self.polja[x][y].sosednje_bombe = -1
                    self.bombe.append(self.polja[x][y])
                    break
        
               

    def stevilo_sosednjih_bomb(self):
        sosedi = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for vrstica in range(self.visina):
            for stolpec in range(self.sirina):
                if self.polja[vrstica][stolpec].sosednje_bombe != -1:
                    for (dx, dy) in sosedi:
                        if 0 <= (vrstica + dx) < (self.visina) and 0 <= (stolpec + dy) < (self.sirina):
                            if self.polja[vrstica + dx][stolpec + dy].sosednje_bombe == -1:
                                self.polja[vrstica][stolpec].sosednje_bombe += 1
                            


    def odkrij_polje(self, vrstica, stolpec):
        if self.odkriti == []:
            self.odkriti.append(self.polja[vrstica][stolpec])
            self.postavi_bombe()
            self.stevilo_sosednjih_bomb()
            self.poteza += 1
            if self.polja[vrstica][stolpec].sosednje_bombe > 0:
                return MEJNA
            elif self.polja[vrstica][stolpec].sosednje_bombe == 0:
                self.odkrij_sosede(vrstica, stolpec)
                return PRAZNA 
        
        elif (self.polja[vrstica][stolpec] in self.odkriti) or (self.polja[vrstica][stolpec] in self.oznaceni):
            return NEVELJAVNA_POTEZA
        else:
            self.poteza += 1
            if self.polja[vrstica][stolpec].sosednje_bombe == -1:
                self.odkriti.append(self.polja[vrstica][stolpec])
                return ZADETA_BOMBA
            elif self.polja[vrstica][stolpec].sosednje_bombe > 0:
                self.odkriti.append(self.polja[vrstica][stolpec])
                return MEJNA
            elif self.polja[vrstica][stolpec].sosednje_bombe == 0:
                self.odkriti.append(self.polja[vrstica][stolpec])
                self.odkrij_sosede(vrstica, stolpec)
                return PRAZNA


    def odkrij_sosede(self, vrstica, stolpec):
        sosedi = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for (dx, dy) in sosedi:
            if 0 <= (vrstica + dx) < (self.visina) and 0 <= (stolpec + dy) < (self.sirina):
                if self.polja[vrstica + dx][stolpec + dy] not in self.odkriti:
                    self.odkriti.append(self.polja[vrstica + dx][stolpec + dy])
                    if self.polja[vrstica + dx][stolpec + dy].sosednje_bombe == 0:
                        self.odkrij_sosede(vrstica + dx, stolpec + dy)
                

    def oznaci_bombo(self, vrstica, stolpec):
        if self.polja[vrstica][stolpec] in self.odkriti:
            pass
        elif self.polja[vrstica][stolpec].oznacena == False:
            self.polja[vrstica][stolpec].oznacena = True
            self.oznaceni.append(self.polja[vrstica][stolpec])
            self.st_oznacenih += 1
        else:
            self.polja[vrstica][stolpec].oznacena = False
            self.oznaceni.remove(self.polja[vrstica][stolpec])
            self.st_oznacenih -=1



        



        
