
class Brique:
    def __init__(self, casse_brique, x1, y1, x2, y2, couleur):
        self.casse_brique = casse_brique
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.bri = self.casse_brique.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=couleur)
        self.compteur = 2

    def touche_la_balle(self, balle):
        ce = balle.centre()
        ra = balle.rayon()
        # width = self.x2 - self.x1
        # height = self.y2 - self.y1
        if self.x2 >= ce[0] >= self.x1:
            if ce[1] > self.y2 >= ce[1] - ra:
                balle.dy *= -1
                self.compteur -= 1
                self.update_couleur()
                return True
            elif ce[1] < self.y1 <= ce[1] + ra:
                balle.dy *= -1
                self.compteur -= 1
                self.update_couleur()
                return True
        if self.y2 >= ce[1] >= self.y1:
            if ce[0] > self.x2 >= ce[0] - ra:
                balle.dx *= -1
                self.compteur -= 1
                self.update_couleur()
                return True
            elif ce[0] < self.x1 <= ce[1] + ra:
                balle.dx *= -1
                self.compteur -= 1
                self.update_couleur()
                return True

        return False

    def is_dead(self):
        return self.compteur <= 0

    def efface(self):
        self.casse_brique.canvas.delete(self.bri)

    def update_couleur(self):
        self.casse_brique.canvas.itemconfig(self.bri, fill=self.casse_brique.couleur[self.compteur])

