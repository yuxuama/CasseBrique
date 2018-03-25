
from math import *

class Balle:

    def __init__(self, casse_brique, x1, y1, x2, y2):

        self.casse_brique = casse_brique
        self.dx = 10
        self.dy = -10
        self.started = False
        self.oval = casse_brique.canvas.create_oval(x1, y1, x2, y2, fill='blue', outline='blue')
        self.x1 = x1
        self.x2 = x2
        self.y2 = y2
        casse_brique.canvas.bind_all('<KeyPress-space>', self.traite_evt_clavier)
        self.touche_bas = False

    def demarre(self):
        self.started = not self.started

    def deplace(self, deplacement):
        if self.started:
            self.casse_brique.canvas.move(self.oval, self.dx, self.dy)
        else:
            self.casse_brique.canvas.move(self.oval, deplacement, 0)

    def toucher_la_raquette(self, raquette):
        c = self.centre()
        r = self.rayon()
        if c[0] <= raquette.bas_x() and c[0] >= raquette.haut_x():
            if c[1] <= raquette.bas_y() + (raquette.bas_y() - raquette.haut_y()) + r and c[1] + r == raquette.haut_y():
                self.modifie(raquette)
        if c[1] <= raquette.bas_y() and c[1] >= raquette.haut_y():
            if c[0] + r >= raquette.haut_x() and c[0] - r <= raquette.bas_x():
                self.dx *= -1

    def touche_un_bord(self):
        pasi = self.casse_brique.canvas.coords(self.oval)
        if pasi[0] <= 0:
            self.casse_brique.canvas.move(self.oval, abs(pasi[0]), 0)
            self.dx *= -1
        if pasi[2] >= self.casse_brique.L:
            self.casse_brique.canvas.move(self.oval, (self.casse_brique.L - pasi[2]), 0)
            self.dx *= -1
        if pasi[1] <= 0:
            self.casse_brique.canvas.move(self.oval, 0, abs(pasi[1]))
            self.dy *= -1
        if pasi[3] >= self.casse_brique.H:
            self.touche_bas = True
            self.dy *= -1

    def rayon(self):
        rayon = (self.x2 - self.x1) / 2
        return rayon

    def centre(self):
        pas = self.casse_brique.canvas.coords(self.oval)
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
        dr = dcr / self.casse_brique.R
        l = sqrt(self.dx * self.dx + self.dy * self.dy)
        alpha = atan2(self.dy, self.dx)
        beta = asin(dr)
        self.dy = -l * sin(alpha + 2 * beta)
        self.dx = l * cos(alpha + 2 * beta)
