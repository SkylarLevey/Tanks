
from graphics import *

class Button:

    """A button is a labeled rectangle in a window.
    It is enabled or disabled with the activate()
    and deactivate() methods. The clicked(pt) method
    returns True if and only if the button is enabled and pt is inside it."""

    def __init__(self, win, center, width, height, label):
        ## as you read through this, ask yourself:  what are the instance variables here?
        ## it would be useful to add comments describing what some of these variables are for...
        """ Creates a rectangular button, eg:
        qb = Button(myWin, centerPoint, width, height, 'Quit') """ 
        w,h = width/2.0, height/2.0   #W and H are half the height and half the width respectively
        x,y = center.getX(), center.getY()  #X and Y are the x and y coordinates of the center,
        ## you should comment these variables...
        self.xmax, self.xmin = x+w, x-w  #xmin and xmax are the x coordinates of the sides of the buttons
        self.ymax, self.ymin = y+h, y-h  #xmin and xmax are the y coordinates of the top and bottom of the button
        p1 = Point(self.xmin, self.ymin) #one of the corners of the button
        p2 = Point(self.xmax, self.ymax) #the opposite corner to p1
        self.rect = Rectangle(p1,p2)     #makes a rectangle with p1 and p2
        self.rect.setFill('lightgray')   #makes the rectangle light gray
        self.rect.draw(win)              #draws the rectangle
        self.label = Text(center, label) #creates the label text object
        self.label.draw(win)             #draws the label
        self.activate() #this line was not there in class today

    def getLabel(self):
        """Returns the label string of this button."""
        return self.label.getText()

    def activate(self):
        """Sets this button to 'active'."""
        self.label.setFill('black') #color the text "black"
        self.rect.setFill('lightgray')
        self.rect.setWidth(2)       #set the outline to look bolder
        self.active = True          #set the boolean variable that tracks "active"-ness to True

    def deactivate(self):
        """Sets this button to 'inactive'."""
        self.rect.setFill('darkgray')
        self.rect.setWidth(1)
        self.active = False

    def isClicked(self, p):
        """Returns true if button active and Point p is inside"""
        x,y = p.getX(),p.getY()
        if self.xmin < x and x < self.xmax and self.ymin < y and y < self.ymax and self.active == True:
            return True
        return False
    def undraw(self):
        self.rect.undraw()
        self.label.undraw
    
    
def main():
    win = GraphWin("button", 300,300)

    happy = Button(win, Point(150, 175), 100, 50, "HAPPY")
    quitB = Button(win, Point(150,250), 75, 50, "Quit")
    pt = win.getMouse()
    while(quitB.isClicked(pt) == False):
        if(happy.isClicked(pt) == True):
            print("YAY")
        pt = win.getMouse()
    win.close() 
    
if __name__ == "__main__": 
    main()
