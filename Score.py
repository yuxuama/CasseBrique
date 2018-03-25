
class Score:
    def __init__(self, casse_brique, x1, y1, f):
        self.casse_brique = casse_brique
        self.score = 0
        self.cscore = self.casse_brique.canvas.create_text(x1, y1, text='Score = %s' % self.score, font=f)
        self.cscore2 = self.casse_brique.canvas.create_rectangle(310, 570, 390, 590, outline='red')

    def uptade(self, bri):
        if bri.compteur <= 0:
            self.score += 1
            self.casse_brique.canvas.itemconfig(self.cscore, text='Score = %s' % self.score)

