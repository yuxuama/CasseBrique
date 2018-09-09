class Brique:
    def __init__(self, casse_brique, x1, y1, x2, y2, couleur):
        self.casse_brique = casse_brique
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.bri = self.casse_brique.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=couleur)
        self.compteur = self.casse_brique.i_couleur + 1

    def touche_la_balle(self, balle):
        ce = balle.centre()
        ra = balle.rayon()
        if self.x2 >= ce[0] >= self.x1:
            if ce[1] - ra <= self.y2 and ce[1] > self.y1:
                balle.dy *= -1
                self.compteur -= 1
                self.update_couleur()
            elif ce[1] + ra >= self.y1 and ce[1] < self.y2:
                balle.dy *= -1
                self.compteur -= 1
                self.update_couleur()
        if self.y2 >= ce[1] >= self.y1:
            if ce[0] - ra <= self.x2 and ce[0] > self.x1 :
                balle.dx *= -1
                self.compteur -= 1
                self.update_couleur()
            elif ce[0] + ra >= self.x1 and ce[0] < self.x2:
                balle.dx *= -1
                self.compteur -= 1
                self.update_couleur()

    def is_dead(self):
        return self.compteur <= 0

    def efface(self):
        self.casse_brique.canvas.delete(self.bri)

    def update_couleur(self):
        self.casse_brique.canvas.itemconfig(self.bri, fill=self.casse_brique.couleur[self.compteur - 1])
