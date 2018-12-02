
example_board = {
        "height":20,
        "width":20,
        "food":[{"x":0,"y":0},{"x":19,"y":19}],
        "turn": 0,
        "snakes":[{
            "id":"snake1",
            "name":"snake 1",
            "health":50,
            "body":[{"x":5,"y":5},{"x":5,"y":6}]
         }, {
          "id":"snake2",
          "name":"snake 2",
          "health":50,
          "body":[{"x":18,"y":5},{"x":18,"y":6}]}
        ]
}


class Board(object):

    def __init__(self, data):
        self.data = data
        self.w = data.get("width", 20)
        self.h = data.get("height", 20)
        self.x_offset = (32 - self.w) / 2
        self.y_offset = (32 - self.h) / 2

    def set_color(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @property
    def food(self):
        return self.data.get("food", [])

    @property
    def color(self):
        return "matrix.Color333({r}, {g}, {b})".format(r=self.r, g=self.g, b=self.b)

    def gen_arduino_code(self):
        lines = ["void board_%d(RGBmatrixPanel matrix){" %self.data.get("turn", 0)]

        # Draw Boarder
        self.set_color(0, 7, 0)
        lines.append("\t"+self.rect(0, 0, 32, 32))
        self.set_color(0, 0, 0)
        lines.append("\t"+self.rect(self.x_offset, self.y_offset, self.w, self.h))

        # Draw Snakes
        self.set_color(7, 0, 0)
        for s in self.data.get("snakes", []):
            lines += ["",
              "\t// {}".format(s.get("name", "???")),
            ]
            for body_seg in self.pixels(coords=s.get("body", [])):
                lines.append("\t"+body_seg)
        lines.append("")

        # Draw Food
        lines.append("\t// Food")
        self.set_color(2, 2, 2)
        for body_seg in self.pixels(coords=self.food):
            lines.append("\t" + body_seg)

        lines.append("}")
        content = "\n".join(lines)
        with open("main/battlesnake.h", "w") as f:
            f.write(content)

    def pixels(self, coords):
        body = []
        for coord in coords:
            x = coord.get("x") + self.x_offset
            y = coord.get("y") + self.y_offset
            body.append("matrix.drawPixel({x}, {y}, {c});".format(x=x, y=y, c=self.color))
        return body

    def rect(self, x, y, w, h):
        return "matrix.fillRect({x}, {y}, {w}, {h}, {c});".format(
            x=x,
            y=y,
            w=w,
            h=h,
            c=self.color
        )


b = Board(example_board)
b.gen_arduino_code()