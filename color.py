class Color:
    def __init__(self, colors):
        self.colors = colors
        self.color = colors[0]

    def switch_color(self):
        self.color = self.colors[(self.colors.index(self.color) + 1) % len(self.colors)]

    def __eq__(self, other):
        return self.color == other.color

    def __ne__(self, other):
        return self.color != other.color
