

class Raquette:

    def __init__(self, canvas):
        self.canvas = canvas
        self.rectangle = self.canvas.create_rectangle(150, 520, 250, 540, fill='orange', outline='orange')

    def deplace(self, dx):
        pos = self.canvas.coords(self.rectangle)
        if pos[2]+dx < 400 or pos[0] + dx > 0:
            self.canvas.move(self.rectangle, dx, 0)

    def centre(self):
        pos = self.canvas.coords(self.rectangle)
        return (pos[0] + pos[2]) / 2.

    def haut_x(self):
        pos = self.canvas.coords(self.rectangle)
        return pos[0]

    def haut_y(self):
        pos = self.canvas.coords(self.rectangle)
        return pos[1]

    def bas_x(self):
        pos = self.canvas.coords(self.rectangle)
        return pos[2]

    def bas_y(self):
        pos = self.canvas.coords(self.rectangle)
        return pos[3]

