import tkinter as tk
import numpy as np

from Voronoi_realization import Voronoi
from tkinter import filedialog
from PIL import ImageTk, Image
from Poisson import poisson


class MainWindow:
    # radius of drawn points on canvas
    RADIUS = 1

    # flag to lock the canvas when drawn
    LOCK_FLAG = False

    def __init__(self, master):
        self.master = master
        self.master.title("Voronoi")

        self.grey = None

        self.frmMain = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        self.frmMain.pack(fill=tk.BOTH, expand=1)

        self.w = tk.Canvas(self.frmMain, width=1080, height=680)
        self.w.config(background='white')
        self.w.bind('<Double-1>', self.onDoubleClick)
        self.w.pack()

        self.frmButton = tk.Frame(self.master)
        self.frmButton.pack()

        self.btnOpen = tk.Button(self.frmButton, text='Open', width=15, command=self.openfile)
        self.btnOpen.pack(side=tk.LEFT)

        self.btnCalculate = tk.Button(self.frmButton, text='Calculate', width=15, command=self.onClickCalculate)
        self.btnCalculate.pack(side=tk.LEFT)

        self.btnClear = tk.Button(self.frmButton, text='Clear', width=15, command=self.onClickClear)
        self.btnClear.pack(side=tk.LEFT)

        self.btnSave = tk.Button(self.frmButton, text='Save', width=15, command=self.savefile)
        self.btnSave.pack(side=tk.LEFT)

    def openfile(self):
        self.imgpath = filedialog.askopenfilename(title='openfile',
                                                  filetypes=[('JPG', '*.jpg'), ('JPEG', '*.jpeg'), ('All Files', '*')])
        print(self.imgpath)
        # print(img)
        im = Image.open(self.imgpath)

        (x, y) = im.size
        self.y_s = 680
        self.x_s = x * self.y_s // y
        self.w.width = self.x_s
        out = im.resize((self.x_s, self.y_s), Image.ANTIALIAS)
        self.grey = out.convert('LA')
        # self.image = ImageTk.PhotoImage(out)

        # self.w.create_image(0, 0, image = self.image, anchor = tk.NW)

        # self.w.pack()

        # print(r)

    def savefile(self):
        r = filedialog.asksaveasfilename(title='savefile', initialdir='./', initialfile='picture.jpg')
        Image.save(r)
        print(r)

    def onClickCalculate(self):
        if not self.LOCK_FLAG:
            self.LOCK_FLAG = True

            # pObj = self.w.find_all()
            # print("pObj")
            # print(pObj)
            points = []
            if self.grey is not None:

                data = np.asarray(self.grey)
                # print(len(data))
                Coords = poisson(self.x_s, self.y_s, 2, 100, data)
            else:
                Coords = poisson(1080, 680, 5, 20)
            for coord in Coords:
                points.append((coord[0] + self.RADIUS, coord[1] + self.RADIUS))

            vp = Voronoi(points)
            vp.process()
            lines = vp.get_res()
            self.drawLinesOnCanvas(lines)

            # print(lines)

    def onClickClear(self):
        self.LOCK_FLAG = False
        self.w.delete(tk.ALL)

    def onDoubleClick(self, event):
        if not self.LOCK_FLAG:
            self.w.create_oval(event.x - self.RADIUS, event.y - self.RADIUS, event.x + self.RADIUS,
                               event.y + self.RADIUS, fill="black")

    def drawLinesOnCanvas(self, lines):
        for l in lines:
            self.w.create_line(l[0], l[1], l[2], l[3], fill='black')


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
