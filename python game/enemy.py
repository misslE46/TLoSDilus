class Enemy:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="red", outline='grey', width=0)
        self.dx=0
        self.dy=0
        self.move_enemy()
        self.health=5

    def move_enemy(self):
        self.canvas.move(self.rect, self.dx, self.dy)
        self.canvas.after(32, self.move_enemy)