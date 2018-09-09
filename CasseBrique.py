# Author Matthieu Lecomte

import time
from Tkinter import *
from Brique import Brique
from Balle import Balle
from Score import Score
from Raquette import Raquette


class CasseBrique:

    def __init__(self):
        self.couleur = ['cyan', 'green', 'red']
        self.i_couleur = 0
        self.WIDTH = 396
        self.W2 = self.WIDTH / 2
        self.L = self.WIDTH
        self.H = 600
        self.H2 = self.H / 2
        self.R = 300.
        self.PAUSE = False
        self.VIE = 3
        self.tk = Tk()
        self.tk.title('CASSE BRIQUE')
        self.canvas = Canvas(self.tk, width=self.L, height=self.H)
        self.canvas.bind_all("<KeyPress-Left>", self.traite_keys_event)
        self.canvas.bind_all("<KeyPress-Right>", self.traite_keys_event)
        self.canvas.bind_all('<KeyPress-space>', self.traite_keys_event)
        self.canvas.pack()

        self.raquette = Raquette(self.canvas)
        self.balle = Balle(self, 190, 499, 210, 519)
        self.score = Score(self, 350, 580, 60)

        self.briques = []

        for g in range(0, 11):
            x1 = 44 * g + 5
            x2 = x1 + 40
            for f in range(0, 6):
                y1 = 25 * f + 5
                y2 = y1 + 20
                bri = Brique(self, x1, y1, x2, y2, self.couleur[self.i_couleur])
                self.briques.append(bri)
                self.i_couleur += 1
                if self.i_couleur > 2:
                    self.i_couleur = 0

    def traite_keys_event(self, evenement):
        if evenement.keysym == 'Right':
            self.raquette.deplace(10)
            if not self.balle.started:
                self.balle.deplace(10)
        elif evenement.keysym == 'Left':
            self.raquette.deplace(-10)
            if not self.balle.started:
                self.balle.deplace(-10)
        if evenement.keysym == 'space':
            self.balle.demarre()

    def play(self):
        self.tk.update()

        while 1:

            if not self.balle.touche_bas or not self.briques:
                self.balle.deplace(0)
                self.balle.touche_un_bord()
            else:
                continue

            self.balle.toucher_la_raquette()

            brique_dead = []

            for bri in self.briques:
                bri.touche_la_balle(self.balle)
                if bri.is_dead():
                    self.score.update()
                    brique_dead.append(bri)

            for bri in brique_dead:
                self.briques.remove(bri)
                bri.efface()

            if self.balle.touche_bas:
                self.canvas.create_text(self.W2, 300, text='Game over', font=60)
                self.tk.update()
                time.sleep(5)
                break

            if not self.briques:
                self.canvas.create_text(self.W2, 300, text='Bravo', font=60)
                self.tk.update()
                time.sleep(5)
                break

            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.1)


casse_brique = CasseBrique()
casse_brique.play()
