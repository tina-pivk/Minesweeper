import tkinter as tk
import model2

BARVE = ['0', 'blue2', 'green2', 'red4', 'purple1', 'cyan3', 'DarkOrange1', 'state gray', 'DarkGoldenrod2']

def meni():
    meni_vrstica = tk.Menu(okno)
    meni_seznam = tk.Menu(okno, tearoff=0)
    meni_seznam.add_command(label='lahko', command=lambda: nova_igra(8, 8, 10))
    meni_seznam.add_command(label='srednje', command=lambda: nova_igra(16, 16, 40))
    meni_seznam.add_command(label='težko', command=lambda: nova_igra(16, 31, 99))
    meni_seznam.add_command(label='po želji', command=lambda: po_zelji())
    meni_vrstica.add_cascade(label="zahtevnost", menu=meni_seznam)
    okno.config(menu=meni_vrstica)

def nova_igra(visina=8, sirina=8, st_bomb=10):
    for x in okno.winfo_children():
        if type(x) != tk.Menu:
            x.destroy()
    Minesweeper(okno, visina, sirina, st_bomb)

def po_zelji():
    okno2 = tk.Tk()
    okno2.title('Zahtevnost')

    def ok(vrstice, stolpci, bombe):
        nova_igra(vrstice, stolpci, bombe)
        okno2.destroy()

    v = tk.Entry(okno2)
    s = tk.Entry(okno2)
    b = tk.Entry(okno2)
    
    v.grid(row=1, column=2)
    s.grid(row=2, column=2)
    b.grid(row=3, column=2)
     
    v_l = tk.Label(okno2, text='vrstice').grid(row=1, column=1)
    s_l = tk.Label(okno2, text='stolpci').grid(row=2, column=1)
    b_l = tk.Label(okno2, text='bombe').grid(row=3, column=1)

    b1 = tk.Button(okno2, text="OK", width=10, command=lambda: ok(int(v.get()), int(s.get()), int(b.get())))
    b1.grid(row=4, column=1, padx=10, pady=10)
    b2 = tk.Button(okno2, text="Cancel", width=10, command=lambda: okno2.destroy())
    b2.grid(row=4, column=2, padx=10, pady=10)

    okno2.mainloop()


class Minesweeper:
    def __init__(self, okno, visina=8, sirina=8, st_bomb=10):
        self.visina = visina
        self.sirina = sirina
        self.st_bomb = st_bomb
        
        self.plosca = model2.Plosca(self.visina, self.sirina, self.st_bomb)

        self.zacni_znova = tk.Button(okno, text='Minesweeper', command=lambda: nova_igra(), width=12)
        self.zacni_znova.grid(row=0, column=1)

        self.stevec_potez = tk.Label(okno, text='0', width=3)
        self.stevec_potez.grid(row=0, column=2)

        self.stevec_bomb = tk.Label(okno, text='{}'.format(self.plosca.st_bomb), width=3)
        self.stevec_bomb.grid(row=0, column=0)

        prikaz_plosce = tk.Frame(okno)
        self.gumbi = []
        for vrstica in range(self.plosca.visina):
            vrstica_gumbov = []
            for stolpec in range(self.plosca.sirina):
                def desni_klik(event, vrstica=vrstica, stolpec=stolpec):
                    self.odkrij(vrstica, stolpec)
                def levi_klik(event, vrstica=vrstica, stolpec=stolpec):
                    self.oznaci(vrstica, stolpec)
                gumb = tk.Button(prikaz_plosce, text='', height=1, width=2)
                gumb.grid(row=vrstica, column=stolpec)
                gumb.bind('<Button-1>', desni_klik)
                gumb.bind('<Button-3>', levi_klik)
                vrstica_gumbov.append(gumb)
            self.gumbi.append(vrstica_gumbov)
        prikaz_plosce.grid(row=1, column=0, columnspan=2)
        

    def odkrij(self, vrsta, stolp):
        stanje = self.plosca.odkrij_polje(vrsta, stolp)
        
        if stanje == model2.MEJNA:
            sos_bombe = self.plosca.polja[vrsta][stolp].sosednje_bombe
            self.gumbi[vrsta][stolp].config(text='{}'.format(sos_bombe), state='disabled', relief='groove', disabledforeground=BARVE[sos_bombe])
            self.konec_igre_1()

        elif stanje == model2.PRAZNA:
            for vrstica in range(self.plosca.visina):
                for stolpec in range(self.plosca.sirina):
                    if self.plosca.polja[vrstica][stolpec] in self.plosca.odkriti:
                        if self.plosca.polja[vrstica][stolpec].sosednje_bombe == 0:
                            self.gumbi[vrstica][stolpec].config(state='disabled', relief='groove')
                        if self.plosca.polja[vrstica][stolpec].sosednje_bombe > 0:
                            sos_bombe = self.plosca.polja[vrstica][stolpec].sosednje_bombe
                            self.gumbi[vrstica][stolpec].config(text='{}'.format(sos_bombe), state='disabled', relief='groove', disabledforeground=BARVE[sos_bombe])
            self.konec_igre_1()
                
        elif stanje == model2.ZADETA_BOMBA:
            self.gumbi[vrsta][stolp].config(state='disabled', relief='groove', bg='red')
            self.zacni_znova.config(text='BOOM!')
            self.konec_igre_3()
            
        self.stevec_potez.config(text=str(self.plosca.poteza))
        

    def oznaci(self, vrsta, stolp):
        self.plosca.oznaci_bombo(vrsta, stolp)
        if self.plosca.polja[vrsta][stolp].oznacena == True:
            self.gumbi[vrsta][stolp].config(text='?')
        elif self.plosca.polja[vrsta][stolp].oznacena == False:
            self.gumbi[vrsta][stolp].config(text='')
        self.konec_igre_2()
        self.stevec_bomb.config(text=str(self.plosca.st_bomb - self.plosca.st_oznacenih))


    def konec_igre_1(self):
        if (len(self.plosca.odkriti) + self.plosca.st_bomb) == (self.plosca.visina * self.plosca.sirina):
            self.zacni_znova.config(text='ZMAGA!')
            self.konec_igre_3()

    def konec_igre_2(self):
        if self.plosca.st_oznacenih == self.plosca.st_bomb:
            stevilo = 0
            for bomba in self.plosca.bombe:
                if bomba in self.plosca.oznaceni:
                    stevilo += 1
            if stevilo == self.plosca.st_bomb:
                self.zacni_znova.config(text='ZMAGA!')
                self.konec_igre_3()
       
    def konec_igre_3(self):
        for vrstica in range(self.plosca.visina):
                for stolpec in range(self.plosca.sirina):
                    if self.plosca.polja[vrstica][stolpec].sosednje_bombe == -1:
                        if self.plosca.polja[vrstica][stolpec].oznacena == True:
                            self.gumbi[vrstica][stolpec].config(text='¤', state='disabled', disabledforeground='violet red')
                        else:
                            self.gumbi[vrstica][stolpec].config(text='x', state='disabled', disabledforeground='red')
                    elif self.plosca.polja[vrstica][stolpec] not in self.plosca.odkriti:
                        self.gumbi[vrstica][stolpec].config(state='disabled', relief='flat')
                        
                        
   
okno = tk.Tk()
okno.title('Minesweeper')
meni()
Minesweeper(okno)
okno.mainloop()
