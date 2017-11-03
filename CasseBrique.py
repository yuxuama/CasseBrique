from Tkinter import *
import random
import time
from math import *

"""objets"""

couleur = ['cyan', 'green', 'red']
WIDTH = 396
W2 = WIDTH / 2
L = WIDTH
H = 600
H2 = H / 2
R = 300.
PAUSE = False
COMPTEUR = 0
VIE = 3


class Brique:
    def __init__(self, x1, y1, x2, y2, i_couleur):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.bri = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=couleur[i_couleur])
        # rcompt = [ 1, 2, 3]
        # random.shuffle(rcompt)
        self.compteur = i_couleur + 1

    def touche_la_balle(self, balle, COMPTEUR):
        ce = balle.centre()
        ra = balle.rayon()
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        if ce[0] <= self.x2 and ce[0] >= self.x1:
            if (ce[1] + ra >= self.y1 and ce[1] - ra <= self.y2):
                COMPTEUR += 1
                balle.dy *= -1
                self.compteur -= 1
                self.update_couleur()
                return True
        if ce[1] <= self.y2 and ce[1] >= self.y1:
            if (ce[0] + ra >= self.x1 and ce[0] - ra <= self.x2):
                COMPTEUR += 1
                balle.dx *= -1
                self.compteur -= 1
                self.update_couleur()
                return True

        print(COMPTEUR)
        return False

    def touche_balle_coin(self, balle):
        ce = balle.centre()
        ra = balle.rayon()
        if ce[0] > self.x1:
            cx = ce[0] - self.x2
        else:
            cx = abs(ce[0] - self.x1)
        if ce[1] > self.y2:
            cy = ce[1] - self.y2
        else:
            cy = abs(ce[1] - self.y1)
        h = sqrt(cy * cy + cx * cx)
        if h == ra:
            self.compteur -= 1
            balle.dx *= -1
            balle.dy *= -1

    def is_dead(self):
        return self.compteur <= 0

    def efface(self):
        canvas.delete(self.bri)

    def update_couleur(self):
        if self.compteur == 1:
            canvas.itemconfig(self.bri, fill='cyan')
        if self.compteur == 2:
            canvas.itemconfig(self.bri, fill='green')
        if self.compteur == 3:
            canvas.itemconfig(self.bri, fill='red')


class Balle:
    def __init__(self, x1, y1, x2, y2):
        self.dx = 8
        self.dy = -8
        self.started = False
        self.oval = canvas.create_oval(x1, y1, x2, y2, fill='blue', outline='blue')
        self.x1 = x1
        self.x2 = x2
        canvas.bind_all('<KeyPress-space>', self.traite_evt_clavier)
        self.touche_bas = False

    def demarre(self):
        self.started = not self.started

    def deplace(self):
        if (self.started == False):
            return
        canvas.move(self.oval, self.dx, self.dy)

    def toucher_la_raquette(self, raquette):
        c = self.centre()
        r = self.rayon()
        if c[0] <= raquette.bas_x() and c[0] >= raquette.haut_x():
            if c[1] <= raquette.bas_y() + (raquette.bas_y() - raquette.haut_y()) + r and c[1] + r == raquette.haut_y():
                self.modifie(raquette)
        if c[1] <= raquette.bas_y() and c[1] >= raquette.haut_y():
            if (c[0] + r >= raquette.haut_x() and c[0] - r <= raquette.bas_x()):
                self.dx *= -1

    def touche_un_bord(self):
        pasi = canvas.coords(self.oval)
        if pasi[0] <= 0:
            canvas.move(self.oval, abs(pasi[0]), 0)
            self.dx *= -1
        if pasi[2] >= L:
            canvas.move(self.oval, (L - pasi[2]), 0)
            self.dx *= -1
        if pasi[1] <= 0:
            canvas.move(self.oval, 0, abs(pasi[1]))
            self.dy *= -1
        if pasi[3] >= H:
            self.touche_bas = True
            self.dy *= -1

    def rayon(self):
        rayon = (self.x2 - self.x1) / 2
        return rayon

    def centre(self):
        pas = canvas.coords(self.oval)
        centre_x = (pas[0] + pas[2]) / 2
        centre_y = (pas[1] + pas[3]) / 2
        return [centre_x, centre_y]

    def traite_evt_clavier(self, evt):
        if evt.keysym == 'space':
            self.demarre()

    def coords_impact(self):
        c = self.centre()
        r = self.rayon()
        imp_y = c[1] + r
        p_impact = [c[0], imp_y]
        return p_impact

    def distance_centre_ra(self, raquette):
        p_impact2 = self.coords_impact()
        return abs(p_impact2[0] - raquette.centre())

    def modifie(self, raquette):
        dcr = self.distance_centre_ra(raquette)
        dr = dcr / R
        l = sqrt(self.dx * self.dx + self.dy * self.dy)
        alpha = atan2(self.dy, self.dx)
        beta = asin(dr)
        self.dy = -l * sin(alpha + 2 * beta)
        self.dx = l * cos(alpha + 2 * beta)


class Raquette:
    def __init__(self):
        self.rectangle = canvas.create_rectangle(150, 520, 250, 540, fill='orange', outline='orange')
        canvas.bind_all("<KeyPress-Left>", self.mouvement_de_la_raquette)
        canvas.bind_all("<KeyPress-Right>", self.mouvement_de_la_raquette)

    def mouvement_de_la_raquette(self, evenement):
        pos = canvas.coords(self.rectangle)
        if evenement.keysym == 'Right':
            canvas.move(self.rectangle, 10, 0)
            if pos[2] >= 400:
                canvas.move(self.rectangle, -10, 0)
        elif evenement.keysym == 'Left':
            canvas.move(self.rectangle, -10, 0)
            if pos[0] <= 0:
                canvas.move(self.rectangle, 10, 0)

    def centre(self):
        pos = canvas.coords(self.rectangle)
        return (pos[0] + pos[2]) / 2.

    def haut_x(self):
        pos = canvas.coords(self.rectangle)
        return pos[0]

    def haut_y(self):
        pos = canvas.coords(self.rectangle)
        return pos[1]

    def bas_x(self):
        pos = canvas.coords(self.rectangle)
        return pos[2]

    def bas_y(self):
        pos = canvas.coords(self.rectangle)
        return pos[3]


class Score:
    def __init__(self, x1, y1, f):
        self.score = 0
        self.cscore = canvas.create_text(x1, y1, text='Score = %s' % self.score, font=f)
        self.cscore2 = canvas.create_rectangle(310, 570, 390, 590, outline='red')

    def uptade(self, bri):
        if bri.compteur <= 0:
            self.score += 1
            canvas.itemconfig(self.cscore, text='Score = %s' % self.score)


tk = Tk()
tk.title('CASSE BRIQUE')
canvas = Canvas(tk, width=L, height=H)

canvas.pack()

raquette = Raquette()
balle = Balle(190, 300, 210, 320)
score = Score(350, 580, 60)
tk.update()

briques = []

i_couleur = 0
for g in range(0, 11):
    x1 = 44 * g + 5
    x2 = x1 + 40
    for f in range(0, 6):
        y1 = 25 * f + 5
        y2 = y1 + 20
        bri = Brique(x1, y1, x2, y2, i_couleur)
        briques.append(bri)
        bri.update_couleur()
        i_couleur += 1
        if i_couleur > 2:
            i_couleur = 0

while 1:

    if balle.touche_bas == False:
        balle.deplace()
        balle.touche_un_bord()
        score.uptade(bri)
    balle.toucher_la_raquette(raquette)
    brique_dead = []
    for bri in briques:
        bri.touche_la_balle(balle, COMPTEUR)
        bri.touche_balle_coin(balle)
        if bri.is_dead():
            brique_dead.append(bri)

    if COMPTEUR >= 2:
        COMPTEUR = 0

    for bri in brique_dead:
        bri.efface()
        briques.remove(bri)

    if balle.touche_bas == True:
        canvas.create_text(W2, 300, text='Game over', font=60)

    if briques == []:
        canvas.create_text(W2, 300, text='Bravo', font=60)

    tk.update_idletasks()
    tk.update()
    time.sleep(0.1)
