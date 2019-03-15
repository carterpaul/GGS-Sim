from tkinter import *

SCALE=2
ACTIVE_COLOR = '#f00'
INACTIVE_COLOR = '#1f1'
BORDER_COLOR = '#000'
ui = None

class UI(Frame):

    def __init__(self):
        super().__init__()

        self.master.title("GGS-Sim")
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH)

        self.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(self)
        self.grid = hex_grid(28,45)
        self.grid.draw(self.canvas)

        otherButton=Button(self, text="Other Button")
        otherButton.pack(side=RIGHT, padx=5, pady=5)
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.pack(side=RIGHT)


class hex:

    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.active = False
        self.id = None
        global ui

    def __str__(self):
        return("(" + str(self.r) + ", " + str(self.c) + ")")

    def draw(self, canvas, outline, fill):
        x_offset = self.c*14
        y_offset = self.r*12
        if self.r%2 == 1: #odd-numbered rows are offset to pack hexagons
            x_offset = x_offset + 7
        points=[7,0,14,4,14,12,7,16,0,12,0,4]
        for i in range(len(points)):
            if i%2 == 0: #if it's an x-coordinate
                points[i] = points[i] + x_offset
            else: #if it's a y-coordinate
                points[i] = points[i] + y_offset
        points = [x*SCALE for x in points]
        self.id = canvas.create_polygon(points, outline=outline, fill=fill, width=2)
        canvas.pack(fill=BOTH, expand=1)

    def click(self):
        if not self.active:
            self.draw(ui.canvas, BORDER_COLOR, ACTIVE_COLOR)
            self.active = True
        else:
            self.draw(ui.canvas, BORDER_COLOR, INACTIVE_COLOR)
            self.active = False


class hex_grid:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = []
        for curRow in range(rows):
            row = []
            for curColumn in range(columns):
                row.append(hex(curRow, curColumn))
            self.grid.append(row)

    def draw(self, canvas):
        for row in self.grid:
            for hex in row:
                hex.draw(canvas, BORDER_COLOR, INACTIVE_COLOR)

    def get_hex_by_id(self, id):
        for row in self.grid:
            for item in row:
                if item.id == id:
                    return item
        return None

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
    ui.grid.get_hex_by_id(eventorigin.widget.find_closest(click_x, click_y)[0]).click()
    print(click_x,click_y)


def main():
    global ui
    root = Tk()
    ui = UI()
    root.geometry("1280x720")
    root.bind("<Button 1>",on_click)
    root.mainloop()

if __name__ == '__main__':
    main()
