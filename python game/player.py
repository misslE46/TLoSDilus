class Player:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill = "cyan", outline= 'cyan', width=0)
        self.keys_pressed = set()
        self.health = 100