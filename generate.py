from websocket import create_connection
import json

example_board = {
 u'Food': [{u'X': 9, u'Y': 7},
           {u'X': 1, u'Y': 8},
           {u'X': 6, u'Y': 8},
           {u'X': 8, u'Y': 2},
           {u'X': 5, u'Y': 7}],
 u'Snakes': [{u'Body': [{u'X': 2, u'Y': -1},
                        {u'X': 2, u'Y': 0},
                        {u'X': 2, u'Y': 1}],
              u'Color': u'#B93021',
              u'Death': {u'Cause': u'wall-collision', u'Turn': 8},
              u'Health': 92,
              u'ID': u'gs_gQFTYyTjP9kWhtVgSRXHXWPG',
              u'Name': u'Team Rocket',
              u'URL': u'https://team-rocket-battle-snake.herokuapp.com/'},
             {u'Body': [{u'X': 1, u'Y': 0},
                        {u'X': 1, u'Y': 1},
                        {u'X': 1, u'Y': 2},
                        {u'X': 0, u'Y': 2},
                        {u'X': 0, u'Y': 1},
                        {u'X': 0, u'Y': 0},
                        {u'X': 1, u'Y': 0},
                        {u'X': 2, u'Y': 0},
                        {u'X': 2, u'Y': 1}],
              u'Color': u'#75CEDD',
              u'Death': {u'Cause': u'snake-self-collision', u'Turn': 106},
              u'Health': 99,
              u'ID': u'gs_b7RBKf6MMPxMrMptFMtvcmWS',
              u'Name': u'jsnek',
              u'URL': u'https://jsnek.herokuapp.com/'},
             {u'Body': [{u'X': 6, u'Y': 0},
                        {u'X': 5, u'Y': 0},
                        {u'X': 4, u'Y': 0},
                        {u'X': 4, u'Y': 1},
                        {u'X': 5, u'Y': 1}],
              u'Color': u'#75CEDD',
              u'Death': None,
              u'Health': 81,
              u'ID': u'gs_qBhM4kbT94CXYxyfdrWWrcHb',
              u'Name': u'Unnamed Snake',
              u'URL': u'https://unnamedsnake.herokuapp.com'},
             {u'Body': [{u'X': 0, u'Y': -1},
                        {u'X': 0, u'Y': 0},
                        {u'X': 0, u'Y': 1}],
              u'Color': u'#1e4fcd',
              u'Death': {u'Cause': u'wall-collision', u'Turn': 2},
              u'Health': 98,
              u'ID': u'gs_cygjj4dk3QVqpMc7w8CyDMMd',
              u'Name': u'Snakerdoodle',
              u'URL': u'https://snakerdoodle.herokuapp.com'}],
 u'Turn': 106}


board_frames = [
    example_board,
    example_board,
    example_board,
]


def get_frames(uid="372eb017-1431-41d6-8a60-0e3d63c56c81"):
    url = "wss://engine.battlesnake.io/socket/{uid}".format(uid=uid)
    ws = create_connection(url)
    content = ""
    while True:
        result = ws.recv()
        if result == "":
            break
        data = json.loads(result)
        board = Board(data)
        content += board.gen_arduino_code()
        content += "\n\n"
    with open("main/battlesnake.h", "w") as f:
        f.write(content)

    ws.close()


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
        return self.data.get("Food", [])

    @property
    def color(self):
        return "matrix.Color333({r}, {g}, {b})".format(r=self.r, g=self.g, b=self.b)

    def gen_arduino_code(self):
        lines = ["void board_%d(RGBmatrixPanel matrix){" %self.data.get("Turn", 0)]

        # Draw Boarder
        self.set_color(0, 7, 0)
        lines.append("\t"+self.rect(0, 0, 32, 32))
        self.set_color(0, 0, 0)
        lines.append("\t"+self.rect(self.x_offset, self.y_offset, self.w, self.h))

        # Draw Snakes
        self.set_color(7, 0, 0)
        for s in self.data.get("Snakes", []):
            lines += ["",
              "\t// {}".format(s.get("Name", "???")),
            ]
            for body_seg in self.pixels(coords=s.get("Body", [])):
                lines.append("\t"+body_seg)
        lines.append("")

        # Draw Food
        lines.append("\t// Food")
        self.set_color(2, 2, 2)
        for body_seg in self.pixels(coords=self.food):
            lines.append("\t" + body_seg)

        lines.append("}")
        content = "\n".join(lines)
        return content

    def pixels(self, coords):
        body = []
        for coord in coords:
            x = coord.get("X") + self.x_offset
            y = coord.get("Y") + self.y_offset
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


# b = Board(example_board)
# b.gen_arduino_code()
get_frames()
