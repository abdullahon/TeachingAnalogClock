__author__ = 'abdullahoncu'
from Tkconstants import TOP, RIGHT, LEFT
from Tkinter import *
import time
import math
import random
from math import *
import time




class Clock(Tk):


    def __init__(self):
        Tk.__init__(self)
        self.title('Analog Clock')
        self.canvas = Canvas(width=800, height=450)
        self.canvas.pack(side=TOP)
        self.plotter()
        Button(text='quit', command=quit).pack(side=LEFT, padx=40)
        self.menu()
        self.getEntry()
        self.basic()
        self.var = StringVar()
        Button(text='Compare', command=self.gec).pack(side=LEFT,padx=50)
        Button(text='Quiz',command=self.new_window).pack(side=LEFT,padx=50)

        # self.var.set("Bos")
        Label(self, textvariable=self.var).pack(side=RIGHT, padx=40)

    def activateListeners(self):          # to activate binding
        self.bind("<B1-Motion>", self.yelkovanDragged)
        self.bind("<B2-Motion>", self.akrepDragged)



    def plotter(self):                          #drawing points circles and yelkovan akrep
        self.circle(60, 200, 200, 200, 12)     #with other two func  circle and point
        self.canvas.delete('lines')

    def point(self, tick, range, radius):
        global angle
        angle = tick * (360.0 / range)
        radiansPerDegree = math.pi / 180
        pointX = int(round(radius * math.sin(angle * radiansPerDegree)))
        pointY = int(round(radius * math.cos(angle * radiansPerDegree)))
        return (pointX, pointY)

    def circle(self, points, radius, centerX, centerY, paints):

        self.canvas.create_oval(5, 5, 400, 400, fill='red')
        self.yelkovan = self.canvas.create_line(200, 200, 200, 20, width=3, fill="blue")
        self.akrep = self.canvas.create_line(200, 200, 330, 200, width=5, fill='yellow')
        self.adiak, self.adiyel = dict(), dict()
        #create  imaginary circles based on angles
        for i in range(60):
            x, y = self.point(i + 1, points, radius - 14)
            self.scaledX, self.scaledY = (x + centerX), (centerY - y)
            self.canvas.create_line(centerX, centerY, self.scaledX, self.scaledY, tag='lines')
            self.canvas.create_rectangle(self.scaledX - 1, self.scaledY - 1, self.scaledX + 0.5, self.scaledY + 0.5, fill='black')


            x1, y1 = self.point(i+1, points, radius - 22)
            x2, y2 = self.point(i+1, points, radius - 70)
            self.adiak[angle] = (x2 + centerX, centerY - y2)   #key angles
            self.adiyel[angle] = (x1 + centerX, centerY - y1)
        #print self.adiak
        #print self.adiyel

        for i in range(12):
            a, b = self.point(i + 1, paints, radius - 14)
            self.scaledX, self.scaledY = (a + centerX), (centerY - b)
            self.canvas.create_rectangle(self.scaledX - 6, self.scaledY - 6,
                                    self.scaledX + 0.5, self.scaledY + 0.5,
                                    fill='red')
            self.canvas.create_text(self.scaledX - 2, self.scaledY - 2, text=i + 1, fill='white')

    def yelkovanDragged(self, event):
        x2, y2 = event.x, event.y
        #print x2,y2
        angle = self.angle(x2, y2)
        x, y = self.adiyel.get(angle, self.adiyel[min(self.adiyel.keys(), key=lambda k: abs(k - angle))])
        self.canvas.coords(self.yelkovan, 200, 200, x, y)
        self.printClock("yelkovan", x, y)
        # self.canvas.delete(self.yelkovan)
        # self.yelkovan = self.canvas.create_line(200, 200, x, y, width=3, fill="blue")

    def akrepDragged(self, event):
        x2, y2 = event.x, event.y
        angle = self.angle(x2, y2)
        # dakika = self.time[1]
        # liste = [k for k in self.adiak.iterkeys() if (k + dakika/15) % 30 == 0]
        # print liste
        x, y = self.adiak.get(angle, self.adiak[min(self.adiak.keys(), key=lambda k: abs(k - angle))])
        # x, y = self.adiak.get(angle, self.adiak[min(liste, key=lambda k: abs(k - angle))])
        self.canvas.coords(self.akrep, 200, 200, x, y)
        self.printClock("akrep", x, y)

#Print the clock on the canvas
    def printClock(self, tur, x, y):
        if tur == "yelkovan":
            for aci, position in self.adiyel.iteritems():
                if position[0] == x and position[1] == y:
                    angle = aci
            dakika = 0 if angle == 360 else angle/6
            self.time = (self.time[0], dakika)     #update times based on yelkovan position with help pf angle
            # return self.time
        elif tur == "akrep":
            for aci, position in self.adiak.iteritems():
                if position[0] == x and position[1] == y:
                    angle = aci
            saat = 12 if angle == 360 else int(angle/30)
            self.time = (saat, self.time[1])
            # return self.time

    def angle(self, x, y):
        deltaX = x - 200
        deltaY = y - 200
        angle = math.atan2(deltaY, deltaX) * 180 / math.pi #find angle while draw angle widgets
        if angle+90 < 0:        #restore angle for proper using
            angle += 360        #make y cordinat to X and x to  Y, origin is center of clock
        return angle + 90

    def menu(self):             #create buttons
        Button(text="Basic", command=self.basic).pack(side=RIGHT,pady=40)
        Button(text="Intermediate", command=self.intermediate).pack(side=RIGHT,pady=40)
        Button(text="Advance", command=self.advance).pack(side=RIGHT,pady=40)

    def basic(self):         #set clock randomly just hours
        self.canvas.delete(self.akrep)
        self.canvas.delete(self.yelkovan)
        choice = random.choice([k for k in self.adiak.iterkeys() if k % 30 == 0])
        x = self.adiak[choice]
        saat = choice/30
        # print ("%02d"%saat) + ':00'
        self.akrep = self.canvas.create_line(200, 200, x[0], x[1], width=5, fill="yellow")
        self.yelkovan = self.canvas.create_line(200, 200, 200, 20, width=3, fill="blue")
        self.time = (saat, 0)


    def intermediate(self):#set clock randomly hours, quarters and half
        self.canvas.delete(self.akrep)
        self.canvas.delete(self.yelkovan)

        choice1 = random.choice([k for k in self.adiak.iterkeys() if k % 30 == 0])
        #take angle in for akrep
        choice2 = random.choice([k for k in self.adiyel.iterkeys() if k % 90 == 0 ] )
        #take angle in for yelkovan
        x2 = self.adiyel[choice2]

        choice2 = 0 if choice2 == 360 else choice2
        choice1 = 0 if choice1 == 360 and choice2 != 0 else choice1

        x1 = self.adiak[choice1 + choice2/15]

        saat = 12 if choice1 == 0 else int(choice1/30)
        dakika = 0 if choice2 == 0 else int(choice2/6)
        # print ("%02d"%saat) + ':' + ("%02d"%dakika)

        self.akrep = self.canvas.create_line(200, 200, x1[0], x1[1], width=5, fill="yellow")
        self.yelkovan = self.canvas.create_line(200, 200, x2[0], x2[1], width=3, fill="blue")
        self.time = (saat, dakika)


    def advance(self):      #set clock randomly
        self.canvas.delete(self.akrep)
        self.canvas.delete(self.yelkovan)

        choice1 = random.choice([k for k in self.adiak.iterkeys() if k % 30 == 0])
        choice2 = random.choice([k for k in self.adiyel.iterkeys()])
        x2 = self.adiyel[choice2]
        choice2 = 0 if choice2 == 360 else choice2

        adder = int(((choice2/6)%90)/12)

        if choice1 == 360 and adder != 0:
            choice1 = 0

        x1 = self.adiak[choice1 + adder*6]

        saat = 12 if choice1 == 0 else (choice1/30)
        dakika = 0 if choice2 == 360 else (choice2/6)
        # print ("%02d"%saat) + ':' + ("%02d"%dakika)

        self.akrep = self.canvas.create_line(200, 200, x1[0], x1[1], width=5, fill="yellow")
        self.yelkovan = self.canvas.create_line(200, 200, x2[0], x2[1], width=3, fill="blue")
        self.time = (saat, dakika)
    def real_time(self):
        self.canvas.delete(self.akrep)
        self.canvas.delete(self.yelkovan)
        choice1,choice2=time.localtime()[3],time.localtime()[4]
        saat = 12 if choice1 == 0 else (choice1/30)
        dakika = 0 if choice2 == 360 else (choice2/6)


    def getEntry(self):
        self.entry = Entry(self, bd=5)
        self.entry.pack(side=LEFT, padx=50)

    def gec(self):
        self.getTime = str(self.entry.get())
        self.compare()
        self.entry.delete(0, END)

    def compare(self):
        self.coming = str(int(self.time[0]))+":"+("%02d"%self.time[1])    #restore self.time tuple for using clock
        # print self.getTime, self.time, coming

        if self.getTime == self.coming:
            print "Correct"
            self.var.set("CORRECT")
        else:
            print "WRONG"
            self.var.set("WRONG!!")

    def new_window(self):
        self.a=Toplevel()
        self.a.title('Quiz Time!')
        self.a.geometry('400x300')
        self.fg=Entry(self.a,)
        self.fg.pack()
        Button(self.a,text='Basic',command=self.basic_test).pack()
        Button(self.a,text='Intermediate',command=self.intermediate_test).pack()
        Button(self.a,text='Advanced',command=self.advance_test).pack()
        Label(self, textvariable=self.var).place(bordermode=OUTSIDE, x=500, y=459)
        self.var = StringVar()

        Label(self.a,text='You have 10 Trials, Go!').pack()

    global rl,wl,yc
    yc,rl,wl=[],[],[]

    def advance_test(self):
        self.advance()
        self.coming = str(int(self.time[0]))+":"+("%02d"%self.time[1])    #restore self.time tuple for using clock
        rr=self.fg.get()
        # print self.getTime, self.time, coming

        if rr==self.coming:
            print "Correct"
            self.var.set("CORRECT")
        else:
            print "WRONG"
            self.var.set("WRONG!!")

    def basic_test(self):
        self.coming = str(int(self.time[0]))+":"+("%02d"%self.time[1])
        self.wrong=0
        self.right=0
        rr=self.fg.get()
        self.basic()


        if rr==self.coming:
            self.right=self.right+1
            rl.append(self.right)
        else:
            yc.append(rr)
            self.wrong=self.wrong+1
            wl.append(self.wrong)


        self.fg.delete(0,END)
        self.result=StringVar()
        if (len(wl)+len(rl))%10==0:
            hb= 'number of correct {}, number of wrong {}'.format(len(rl),len(wl))
            self.result.set(hb)
            self.jk=Label(self.a,textvariable=self.result).pack(side=BOTTOM)
            print self.wrong,self.right

    def intermediate_test(self):
        self.coming = str(int(self.time[0]))+":"+("%02d"%self.time[1])
        self.wrong=0
        self.right=0
        rr=self.fg.get()
        self.intermediate()


        if rr==self.coming:
            self.right=self.right+1
            rl.append(self.right)
        else:
            yc.append(rr)
            self.wrong=self.wrong+1
            wl.append(self.wrong)


        self.fg.delete(0,END)
        self.result=StringVar()
        if (len(wl)+len(rl))%10==0:
            hb= 'number of correct {}, number of wrong {}'.format(len(rl),len(wl))
            self.result.set(hb)
            self.jk=Label(self.a,textvariable=self.result).pack(side=BOTTOM)
            print self.wrong,self.right






q = Clock()
q.activateListeners()
q.mainloop()
q.real_time()
