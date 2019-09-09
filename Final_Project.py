#Final Project COM 110
#Professor Chung
#Abe Lusk
#Skylar Levey
#12/22/15

import graphics
from button import *
from math import *
from time import sleep
from random import randrange


class Ground:
    """Creates a ground object with a list of points for the top side then two anchor points in the bottom left
    and bottom right of the screen, then draws a green polygon to represent it in the GUI.
    The wind instance variable is also saved here seeing as the ground is updated every turn"""
    def __init__(self, win, groundList):
        #sets instace variables
        self.groundList = groundList
        self.groundPoly = Polygon(groundList)
        self.groundPoly.setFill("green")
        self.groundPoly.draw(win)
        self.wind = randrange(-50,51)
        self.windText = Text(Point(139,80), self.wind)
        self.windText.draw(win)

    def Undraw(self):
        """Undraws only the polygon part of the ground so it can be redrawn with new points"""
        self.groundPoly.undraw()


class Tank:
    """Makes a tank object with a position, and a color.  also passed are the ground object, the window,
    and the position of the text representing it's health"""
    def __init__(self, position, ground, win, textPos, color):
        #sets instace variables
        self.power = 40
        self.groundList = ground.groundList
        self.health = 99
        self.win = win
        self.posX, self.posY = position.getX(), position.getY()

        #makes the polygon for the top half of the tank with the given color
        self.tankPic1 = Polygon(Point(self.posX-2,self.posY-1), Point(self.posX-2,self.posY+1), Point(self.posX-1,self.posY+2), Point(self.posX+1,self.posY+2), Point(self.posX+2,self.posY+1), Point(self.posX+2,self.posY-1))
        self.tankPic1.draw(self.win)
        self.tankPic1.setFill(color)
        #makes the polygon for the treads of the tank, which is black for both tanks
        self.tankPic2 = Polygon(Point(self.posX-3,self.posY-1), Point(self.posX-2,self.posY-2), Point(self.posX+2,self.posY-2), Point(self.posX+3,self.posY-1))
        self.tankPic2.draw(self.win)
        self.tankPic2.setFill("black")

        #makes line representing the barrel line for the tank
        self.barrel = Line(Point(self.posX, self.posY),Point(self.posX-2*sqrt(2), self.posY+2*sqrt(2)))
        self.barrel.setWidth(4)    #makes it more visable
        self.barrel.draw(self.win)
        self.barrelAngle = 45

        #makes the text object representing the health, with the given position
        self.tankHealth = Text(textPos, "99")
        self.tankHealth.draw(win)
        

    def moveTank(self, direction):
        """Moves the tank's position horizontally with a given direction"""
        #checks to see if the tank is trying to move offscreen
        if (self.posX > 1 and direction <= 0) or (self.posX < 200 and direction >= 0):
            #incraments horizontal position
            self.posX += direction
            #finds the new y position based on the ground
            YpositionIncrament = self.groundList[int(self.posX)].getY() - self.posY +2
            self.posY += (YpositionIncrament)
            #moves the images appropriately
            self.tankPic1.move(direction, YpositionIncrament)
            self.tankPic2.move(direction, YpositionIncrament)
            self.barrel.move(direction, YpositionIncrament)


    def moveBarrel(self, angle):
        """Changes the angle of the barrel"""
        #undraws the barrel line
        self.barrel.undraw()
        #calculates the new endpoint of the line
        self.barrelX = -cos(angle*pi/180)*4
        self.barrelY = sin(angle*pi/180)*4
        #redefines the instance variables
        self.barrel = Line(Point(self.posX, self.posY), Point(self.posX+self.barrelX,self.posY+self.barrelY))
        self.barrel.setWidth(4)
        self.barrel.draw(self.win)
        self.barrelAngle = angle

    def changeHealth(self, healthIncrament):
        """Takes in an incrament and incraments the hidden health variable as such,
        also updates the text object representing the health"""
        self.health += healthIncrament
        self.tankHealth.setText(self.health)

        
class Bullet:
    """Makes a bullet object, also takes in both tanks for interaction purposes,
    the window, the ground, and the blast radius of the bullets"""
    def __init__(self, tank1, tank2, win, ground, blastRadius):
        #sets instace variables
        self.tank1 = tank1
        self.tank2 = tank2
        self.blastRadius = blastRadius
        self.groundObj = ground
        self.groundList = ground.groundList
        self.win = win
        self.posX, self.posY = tank1.posX, tank1.posY
        self.posX2, self.posY2 = tank2.posX, tank2.posY
        self.angle = tank1.barrelAngle

        #makes the bullet image itself
        self.bulletPic = Circle(Point(self.posX, self.posY), .5)
        self.bulletPic.draw(win)

    def shoot(self, power):
        """This method takes in the power, then actually does the shooting of the bullet with the physics equations and such"""
        #defines the velocity variables, the displacement variables, and time 
        horizontalVelocity = -cos(self.angle*pi/180)*power
        verticalVelocity = sin(self.angle*pi/180)*power
        timeCounter, vertDistance, horDistance = 0,0,0
        #this represents the actual point on our ground object
        roundedXValue = round(self.posX+horDistance)

        #while loop basically says while it is in the air and on screen
        while(self.groundList[roundedXValue].getY() < vertDistance + self.posY) and not(self.posX+horDistance < 0 or self.posX+horDistance > 200) and not((self.posX2-2)<(self.posX+horDistance)<(self.posX2+2) and (self.posY2-2)<(self.posY+vertDistance)<(self.posY2+2)):
            #physics
            vertDistance = verticalVelocity * timeCounter - 4.8 * timeCounter**2
            horDistance = horizontalVelocity * timeCounter
            #adds wind
            horizontalVelocity += (self.groundObj.wind/600)
            #updates the bullet position and time as time passes
            self.bulletPic.undraw()
            self.bulletPic = Circle(Point(horDistance + self.posX, vertDistance + self.posY), .5)
            self.bulletPic.draw(self.win)
            sleep(0.02)
            timeCounter += .04
            roundedXValue = round(self.posX+horDistance)

        self.bulletPic.undraw()
        #checks for onscreen
        if(self.posX+horDistance < 0 or self.posX+horDistance > 200):
            ThisDoesntMatter = "yes"

        #checks to see if it hit a tank directly, then chages health accordingly
        elif ((self.posX2-2)<(self.posX+horDistance)<(self.posX2+2) and (self.posY2-2)<(self.posY+vertDistance)<(self.posY2+2)):
            self.explosion(Point(self.posX+horDistance,self.posY+vertDistance))
            self.tank2.changeHealth(-50)

        #otherwise it hit the ground, calculats the distance around the landing spot and moves the ground around it
        else:
            referencePoint = self.groundList[roundedXValue]
            #goes through points in the list potentially in the blast
            for point in self.groundList[roundedXValue-self.blastRadius:roundedXValue+self.blastRadius+1]:
                dist = sqrt((point.getY() - referencePoint.getY())**2  + (point.getX() - referencePoint.getX())**2)
                #if they are in the blast move them to the outside of it
                if dist <= self.blastRadius:
                    newYValue = point.getY() - sqrt(self.blastRadius**2 - (point.getX()-roundedXValue)**2)
                    self.groundList[int(point.getX())] = Point(point.getX(), newYValue)
            self.explosion(referencePoint) #see explosion
                    
            #checks to see if a tank was in the blast radius
            tankBulletDist1 = sqrt((self.posX - referencePoint.getX())**2  + (self.posY - referencePoint.getY())**2)
            tankBulletDist2 = sqrt((self.posX2 - referencePoint.getX())**2  + (self.posY2 - referencePoint.getY())**2)
            #if either tank was change its health
            if tankBulletDist1 <= self.blastRadius:
                self.tank1.changeHealth(-33)
            if tankBulletDist2 <= self.blastRadius:
                self.tank2.changeHealth(-33)

        #if the ground was blown out from under them, have the tank fall
        self.tank1.moveTank(0)
        self.tank2.moveTank(0)
        self.groundObj.Undraw()
        #returns the new changed groundlist
        return self.groundList


    def explosion(self, point):
        """Makes an explosion animation"""
        #makes three circles of different colors and sizes drawn over each other to represent an explosion 
        inner = Circle(point, 2)
        inner.setFill("yellow")
        inner.draw(self.win)
        sleep(.033)
        middle = Circle(point, 3)
        middle.setFill("orange")
        middle.draw(self.win)
        sleep(.033)
        outer = Circle(point, 4)
        outer.setFill("red")
        outer.draw(self.win)
        sleep(.033)
        inner.undraw()
        middle.undraw()
        outer.undraw()


class interface:
    """Creates all of the things seen on screen that are not the tanks, ground or bullets"""
    def __init__(self, win):
        
        win.setBackground('skyblue')
        #makes buttons
        self.moveLeft = Button(win, Point(13,85), 10, 7, "Left")
        self.moveRight = Button(win, Point(27,85), 10, 7, "Right")
        self.barrelUp = Button(win, Point(50,90), 10, 7, "B-Up")
        self.barrelDown = Button(win, Point(65,90), 10, 7, "B-Down")
        self.setBarrel = Button(win, Point(63,80), 14, 7, "Set-Barrel")
        self.powerUp = Button(win, Point(95,90), 10, 7, "P-Up")
        self.powerDown = Button(win, Point(110,90), 10, 7, "P-Down")
        self.setPower = Button(win, Point(108,80), 14, 7, "Set-Power")
        self.fire = Button(win, Point(170,85), 20, 15, "FIRE")
        self.quitB = Button(win, Point(195,95),8, 6, "Quit")

        #makes text objects
        self.tank1HealthText = Text(Point(133, 90), "T1 Health:")
        self.tank2HealthText = Text(Point(133, 85), "T2 Health:")
        self.tank1HealthText.draw(win)
        self.tank2HealthText.draw(win)
        self.wind = Text(Point(132, 80), "Wind:")
        self.wind.draw(win)
        self.moves = Text(Point(17,92), "Moves Left:")
        self.moves.draw(win)
        self.movesNum = Text(Point(26,92), "5")
        self.movesNum.draw(win)

        #makes entry objects
        self.barrelInput = Entry(Point(50,80), 3)
        self.barrelInput.draw(win)
        self.barrelInput.setText("45")
        self.powerInput = Entry(Point(95,80), 3)
        self.powerInput.draw(win)
        self.powerInput.setText("40")


#Creates the instruction page with the text and then an option for the map choice
def instructionPage(window):
    #instruction text
    TitleText= Text(Point(100,90),"TANKS")
    TitleText.setSize(36)
    IntroText = Text(Point(100,65), "The Object of the game is to destroy the opponent's tank, \n"
                     "This can be done with either 2 direct hits (50 damage each) or 3 indirect (33 damage each) hits\n"
                     "Each player gets 5 moves a turn, once you have moved 5 times you are stuck there for the rest of the turn,\n"
                     "Also during your turn you can set the angle of the barrel to any angle you want, and the power to anything in range 0-50\n"
                     "Each player is given one shot per turn and after a shot lands it is the opponet's turn.  Take note of the wind BTW (negative is left)\n\n"
                     "Player 1 is red, Player 2 is blue,  Player 1 goes first\n"
                     "(it's not that big of an advantage but if you can't decide the younger player goes first)\n\n"
                     "Choose a map then click play when you are ready to start")
    IntroText.setSize(15)
    TitleText.draw(window)
    IntroText.draw(window)
    #displays map options, and input box
    mapSelect = Text(Point(50,25), "Map Options:             3: Valley\n   1: Good Old Flat           4: More Hills\n2: King of the Hill           5: RANDO")
    mapChoise = Text(Point(94,24), "Map Choise:\n(Enter the #)")
    mapSelect.draw(window)
    mapChoise.draw(window)
    MapChoiseBox = Entry(Point(105,25),2)
    MapChoiseBox.setText("1")
    MapChoiseBox.draw(window)

    #makes the play button and waits until they click it to proceed
    Play = Button(window, Point(150,25), 20, 12, "PLAY")
    pt = window.getMouse()
    while(Play.isClicked(pt) != True):
        pt = window.getMouse()
    #undraws everything
    IntroText.undraw()
    TitleText.undraw()
    Play.undraw()
    Play.label.undraw()
    mapSelect.undraw()
    mapChoise.undraw()
    MapChoiseBox.undraw()
    #returns map choise
    return eval(MapChoiseBox.getText())


#This is what happens in a turn
def TankTurn(tank1, tank2, ground, win, interface):

    #if both tanks are alive:
    if not (tank1.health <= 0 or tank2.health <= 0):

        #changes the power and barrel to what they were for this tank
        interface.powerInput.setText(tank1.power)
        interface.barrelInput.setText(tank1.barrelAngle)
        #refreshes move, and activates the move buttons
        move = 5
        interface.movesNum.setText(move)
        interface.moveRight.activate()
        interface.moveLeft.activate()
        interface.setBarrel.activate()
        interface.setPower.activate()

        #get click loop until they press play or quit
        pt = win.getMouse()
        while(interface.quitB.isClicked(pt) != True and interface.fire.isClicked(pt) != True):
            interface.setBarrel.activate()
            interface.setPower.activate()

            #moves left and right based on click
            if interface.moveLeft.isClicked(pt) == True:
                tank1.moveTank(-3)
                move-=1
                interface.movesNum.setText(move)
            if interface.moveRight.isClicked(pt) == True:
                tank1.moveTank(3)
                move-=1
                interface.movesNum.setText(move)
            #no more move if move count = 0
            if move == 0:
                interface.moveRight.deactivate()
                interface.moveLeft.deactivate()

            #sets barrel and incraments if they pressed either BarrelUp or BarrelDown
            if interface.setBarrel.isClicked(pt) == True:
                userangle = eval(interface.barrelInput.getText())
                tank1.moveBarrel(userangle)
                interface.setBarrel.deactivate()

            if interface.barrelUp.isClicked(pt) == True:
                userangle = eval(interface.barrelInput.getText())
                tank1.moveBarrel(userangle+1)
                newangle = str(userangle+1)
                interface.barrelInput.setText(newangle)
                    
            if interface.barrelDown.isClicked(pt) == True:
                userangle = eval(interface.barrelInput.getText())
                tank1.moveBarrel(userangle-1)
                newangle = str(userangle-1)
                interface.barrelInput.setText(newangle)
                
                    
            #sets power and incraments if they pressed either PowerUp or PowerDown
            #the upward limit is 50 and the lower limit is 0
            if interface.setPower.isClicked(pt) == True:
                userPower = eval(interface.powerInput.getText())
                if userPower > 50:
                    userPower = 50
                    interface.powerInput.setText(userPower)
                if userPower <= 0:
                    userPower = 0
                    interface.powerInput.setText(userPower)
                tank1.power = userPower
                interface.setPower.deactivate()
                

            if interface.powerUp.isClicked(pt) == True:
                userPower = eval(interface.powerInput.getText())
                if userPower < 50:
                    tank1.power += 1
                    interface.powerInput.setText(tank1.power)
                else:
                    interface.powerInput.setText("50")
                    tank1.power = 50

            if interface.powerDown.isClicked(pt) == True:
                userPower = eval(interface.powerInput.getText())
                if userPower > 0:
                    tank1.power -= 1
                    interface.powerInput.setText(tank1.power)
                else:
                    interface.powerInput.setText("0")
                    tank1.power = 0

            pt = win.getMouse()

        #when they click fire button:
        if(interface.fire.isClicked(pt) == True):
            #make a bullet and call shoot
            bullet1 = Bullet(tank1, tank2, win, ground, 5)
            newList = bullet1.shoot(tank1.power)
            #undraw the wind and then set the ground to the new changed ground (also resets wind)
            ground.windText.undraw()
            ground = Ground(win, newList)
            #if either of the tanks are dead, undraw stuff so their are no errors in recursion
            if tank1.health <= 0 or tank2.health <= 0:
                ground.groundPoly.undraw()
                ground.windText.undraw()
            #call take turn but the tanks are switch so it's the other player's turn
            TankTurn(tank2, tank1, ground, win, interface)
            return True

        #if they quit then undraw stuff and quit
        if(interface.quitB.isClicked(pt) == True):
            ground.groundPoly.undraw()
            ground.windText.undraw()
            return False

#displays who won and gives the user the option to play again
def playAgain(window, health1, health2):   
    square = Rectangle(Point(65, 65), Point(135,35))
    square.setFill("teal")
    square.draw(window)
    #this is there as a check for if they quit
    if health1 > 0 and health2 > 0:
        winner = Text(Point(100,60),"Are you Sure????")
        winner.setSize(20)
        winner.draw(window)

    #these are the 3 possible outcomes
    elif health1 <= 0 and health2 <= 0:
        winner = Text(Point(100,60),"You tied, congradulations... I guess")
        winner.setSize(20)
        winner.draw(window)
    elif health1 <= 0:
        winner = Text(Point(100,60),"Player 2 is the Winner!!!!!")
        winner.setSize(20)
        winner.draw(window)
    elif health2 <= 0:
        winner = Text(Point(100,60),"Player 1 is the Winner!!!!!")
        winner.setSize(20)
        winner.draw(window)

    #gives the user 2 options
    PlayAgain = Button(window, Point(90,45), 20, 15, "PLAY Again??")
    Quit = Button(window, Point(110,45), 15, 10, "Quit :(")

    #takes click until the user click a button
    pt = window.getMouse()
    while(PlayAgain.isClicked(pt) != True and Quit.isClicked(pt) != True):
        pt = window.getMouse()
    #if they clicked play again undraw the options and return true
    if PlayAgain.isClicked(pt) == True:
        winner.undraw()
        PlayAgain.undraw()
        PlayAgain.label.undraw()
        Quit.undraw()
        Quit.label.undraw()
        square.undraw()
        return True
    #otherwise they click quit so return false
    return False

#makes the ground object based on what option they picked at the beginning
def mapOption(option):
    glist = []

    #flat
    if option == 1:
        for i in range(201):
            glist.append(Point(i,30))
        return glist, Point(20,32), Point(180,32)

    #big hill in the center
    if option == 2:
        for i in range(20):
            glist.append(Point(i,20))
        for i in range(20,90):
            glist.append(Point(i,10+i/2))
        for i in range(90,110):
            glist.append(Point(i,55))
        counter = 55
        for i in range(110,180):
            counter -= .5
            glist.append(Point(i,counter))
        for i in range(180,201):
            glist.append(Point(i,20))
        return glist, Point(10,22), Point(190,22)

    #both sides raised up and a big flat-bottomed valley in the middle
    if option == 3:
        for i in range(10):
            glist.append(Point(i,60))
        for i in range(10,50):
            glist.append(Point(i,70-i))
        for i in range(50,150):
            glist.append(Point(i,20))
        counter = 20
        for i in range(150,190):
            counter += 1
            glist.append(Point(i,counter))
        for i in range(190,201):
            glist.append(Point(i,60))
        return glist, Point(8,62), Point(192,62)

    #4 little hills
    if option == 4:
        for i in range(20):
            glist.append(Point(i,20))
        for i in range(0,160):
            glist.append(Point(i+20,sin(i/(7.276))*10+20))
        for i in range(180,201):
            glist.append(Point(i,20))
        return glist, Point(10,22), Point(190,22)

    #randomly generated
    if option == 5:
        leftside, rightside = [],[]
        for i in range(20):
            glist.append(Point(i,45))

        counter = 45
        for i in range(20,100):
            incrament = randrange(-2,3)
            counter += incrament
            leftside.append(Point(i,counter))
        for i in range(80):
            glist.append(leftside[i])

        counter = 45
        for i in range(179,99,-1):
            incrament = randrange(-2,3)
            counter += incrament
            rightside.append(Point(i,counter))
        rightside.reverse()
        for i in range(80):
            glist.append(rightside[i])

        for i in range(180,201):
            glist.append(Point(i,45))
            
        return glist, Point(10,47), Point(190,47)

def main():
    #makes the window, and sets the coordinates
    win = GraphWin("Tanks", 1200,600)
    win.setCoords(1,1,200,100)

    #displays instructions and gets map choise
    userMap = instructionPage(win)
    
    choise = True
    #while playAgain = true, (the user click play again)
    while(choise == True):
        #make a new ground
        groundList,t1pos,t2pos = mapOption(userMap)
        groundList.append(Point(200,0))
        groundList.append(Point(0,0))
        ground1 = Ground(win, groundList)

        #make the tanks
        tank1 = Tank(t1pos,ground1, win, Point(142, 90), "red")
        tank1.moveBarrel(135)
        tank2 = Tank(t2pos,ground1, win, Point(142, 85),"blue")
        #and the interface
        interface1 = interface(win)

        #play the game, (if it ends with both players dead return true,
        #otherwise it means they clicked quit
        choise = TankTurn(tank1, tank2, ground1, win, interface1)
        #if it ended with both players dead, ask the user if they want to play again
        if choise == True:
            choise = playAgain(win, tank1.health, tank2.health)

        #undraw everything
        interface1.movesNum.undraw()
        tank1.tankHealth.undraw()
        tank2.tankHealth.undraw()
        tank1.barrel.undraw()
        tank2.barrel.undraw()
        tank1.tankPic1.undraw()
        tank2.tankPic1.undraw()
        tank1.tankPic2.undraw()
        tank2.tankPic2.undraw()

    #if they clicked quit close the window
    win.close()


main()
