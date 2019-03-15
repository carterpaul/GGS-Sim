from tkinter import *

SCALE = 2
ACTIVE_FILL = '#f00'
INACTIVE_FILL = '#1f1'
DESELECTED_OUTLINE = '#000'
SELECTED_OUTLINE = '#fff'
NEIGHBOR_COLOR = '#0000ff'
ui = None


class UI(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.pack(fill=BOTH, expand=True)

    def initUI(self):
        self.master.title("GGS-Sim")
        self.canvas = Canvas(self)
        self.grid = hex_grid(28, 45)
        self.grid.draw(self.canvas)

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH)
        otherButton = Button(self, text="Other Button")
        otherButton.pack(side=RIGHT, padx=5, pady=5)
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.pack(side=RIGHT)


class hex:

    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.active = False
        self.selected = False
        self.id = None
        self.outline_color = DESELECTED_OUTLINE
        self.fill_color = INACTIVE_FILL

    def __str__(self):
        return("(" + str(self.r) + ", " + str(self.c) + ")")

    def draw(self, canvas):
        x_offset = self.c*14
        y_offset = self.r*12
        if self.r % 2 == 1:  # odd-numbered rows are offset to pack hexagons
            x_offset = x_offset + 7
        points = [7, 0, 14, 4, 14, 12, 7, 16, 0, 12, 0, 4]
        for i in range(len(points)):
            if i % 2 == 0:  # if it's an x-coordinate
                points[i] = points[i] + x_offset
            else:  # if it's a y-coordinate
                points[i] = points[i] + y_offset
        points = [x*SCALE for x in points]
        self.id = canvas.create_polygon(points, outline=self.outline_color,
                                        fill=self.fill_color)
        canvas.pack(fill=BOTH, expand=1)

    def select(self):
        self.selected = True
        self.outline_color = SELECTED_OUTLINE

    def deselect(self):
        self.selected = False
        self.outline_color = DESELECTED_OUTLINE

    def set_active(self):
        self.active = True
        self.fill_color = ACTIVE_FILL

    def set_inactive(self):
        self.active = False
        self.fill_color = INACTIVE_FILL

    def toggle_active(self):
        if self.active:
            self.set_inactive()
        else:
            self.set_active()


class hex_grid:

    def __init__(self, rows, columns):
        global ui
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.selected_hex = None
        for curRow in range(rows):
            row = []
            for curColumn in range(columns):
                row.append(hex(curRow, curColumn))
            self.grid.append(row)

    def draw(self, canvas):
        for row in self.grid:
            for hex in row:
                hex.draw(canvas)

    def get_hex_by_id(self, id):
        for row in self.grid:
            for item in row:
                if item.id == id:
                    return item
        return None

    def click(self, hex):
        hex.toggle_active()
        if self.selected_hex is not None:
            self.selected_hex.deselect()
        hex.select()
        self.selected_hex = hex
        self.draw(ui.canvas)

    # returns neighbors of given hex starting at top left moving c-clockwise
    def get_neighbors(self, hex):
        c = hex.c
        r = hex.r
        if r % 2 == 0:
            return [self.grid[r-1][c-1],
                    self.grid[r-1][c],
                    self.grid[r][c+1],
                    self.grid[r+1][c],
                    self.grid[r+1][c-1],
                    self.grid[r][c-1]]
        else:
            return [self.grid[r-1][c],
                    self.grid[r-1][c+1],
                    self.grid[r][c+1],
                    self.grid[r+1][c+1],
                    self.grid[r+1][c],
                    self.grid[r][c-1]]

    def __str__(self):
        result = ""
        for row in self.grid:
            result = result + str([str(hex) for hex in row]) + "\n"
        return result


def on_click(eventorigin):
    global ui
    click_x = eventorigin.x
    click_y = eventorigin.y
    print(eventorigin.widget.find_closest(click_x, click_y)[0])
    ui.grid.click(ui.grid.get_hex_by_id(eventorigin.widget
                                        .find_closest(click_x, click_y)[0]))
    print(click_x, click_y)


def main():
    global ui
    root = Tk()
    ui = UI()
    root.geometry("1280x720")
    root.bind("<Button 1>", on_click)
    root.mainloop()


if __name__ == '__main__':
    main()
