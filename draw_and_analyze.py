import tkinter as tk
from PIL import Image,ImageDraw
import numpy as np
import cv2
import matplotlib.pyplot as plt
from ripser import Rips
import persim, persim.plot
from persim import PersImage

class ImageGenerator:
    def __init__(self, parent, posx, posy, sizex, sizey):
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = sizex
        self.sizey = sizey
        self.b1 = "up"
        self.xold = None
        self.yold = None 
        self.drawing_area=tk.Canvas(self.parent,width=self.sizex,height=self.sizey)
        self.drawing_area.place(x=self.posx,y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.button=tk.Button(self.parent,text="Analyze",width=10,bg='black',command=self.save)
        self.button.place(x=self.sizex/7,y=self.sizey+20)
        self.button1=tk.Button(self.parent,text="Clear",width=10,bg='black',command=self.clear)
        self.button1.place(x=(self.sizex/7)+90,y=self.sizey+20)
        self.figure = plt.figure()
        #self.ax = plt.plot()
        self.rips = Rips()
        self.pim = PersImage(spread=1, pixels=[50,50], verbose=True)
        plt.ion()
        plt.show()
        plt.draw()
        plt.pause(0.01)
        self.image=Image.new("RGB",(256,256),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)

    def save(self):
        im = np.array(self.image)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = cv2.resize(im,(64,64))
        (thresh, data1) = cv2.threshold(im, 250, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        loc = cv2.findNonZero(~data1)
        loc = np.resize(loc, [-1,2])
        pers_dgms = self.rips.fit_transform(loc)
        plt.clf()
        plt.subplot(1,3,1)
        plt.imshow(data1)
        plt.title("Image")
        plt.subplot(1,3,2)
        self.rips.plot(pers_dgms,legend=True) 
        plt.title("Persistence diagram")       
        ax = plt.subplot(1,3,3)
        
        img = self.pim.transform(pers_dgms[1])
        plt.title("Pers. image for $H_1$\n")
        self.pim.show(img, ax)
        plt.draw()
        plt.pause(0.01)

    def clear(self):
        self.drawing_area.delete("all")
        self.image=Image.new("RGB",(256,256),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)

    def b1down(self,event):
        self.b1 = "down"

    def b1up(self,event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self,event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=3,fill='blue')
                self.draw.line(((self.xold,self.yold),(event.x,event.y)),(0,0,0),width=3)

        self.xold = event.x
        self.yold = event.y

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Draw a shape!")
    win_x_size = 300
    win_y_size = 300
    root.wm_geometry("%dx%d+%d+%d" % (win_x_size, win_y_size, 10, 10))
    root.config(bg='white')

    canvas_x_size = 256
    canvas_y_size = 256
    ImageGenerator(root, 10, 10, canvas_x_size, canvas_y_size)
    root.mainloop()
