
import pygame, math, sys, os, platform
import Tkinter as tk
from Tkinter import *
from pygame.locals import *

#simulation variables 
edge_clamp = False
bgColour = (0,0,0)
G = 6.67e-11
width, height = 1506, 760
FPS = 120
sunX = width/2
sunY = height/2
sunMass = 1.989e30
planetList = []
mainClock = pygame.time.Clock()
bgmColour = (255,255,255)
width_m = 400
height_m = 960
dt = 1


def sol(): #function that creates our solar system
    global dt
    dt = 0
    

def setSpeed(event):
    
    global dt
    dt = int(event.widget.get())
    

def addPlanet():
                
    top = tk.Toplevel(root)
    top.wm_title("Add Planet")
                
    add_mass = tk.Entry(top)
    add_mass.pack()
    add_mass.delete(0, END)
    add_mass.insert(0, "6e24")
                

    add_vi = tk.Entry(top)
    add_vi.pack()
    add_vi.delete(0, END)
    add_vi.insert(0, "1")
                

    add_angle = tk.Entry(top)
    add_angle.pack()
    add_angle.delete(0, END)
    add_angle.insert(0, 90)

    add_radius = tk.Entry(top)
    add_radius.pack()
    add_radius.delete(0, END)
    add_radius.insert(0, 152)

    def checkValues():
        nmass = float(add_mass.get())
        nvi = float(add_vi.get())
        ndegrees = float(add_angle.get())
        nangle = math.radians(ndegrees)
        nradius = float(add_radius.get())
        newPlanet(nmass, nvi, nangle, sunX + nradius , sunY)

    b_go = tk.Button(top, text="go", command = checkValues)
    b_go.pack()

                
class MainWindow(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, width = 100, *args, **kwargs)

        #add the UI
        self.add_button = tk.Button(self, text='Add Planet', padx = 10, pady = 10, command = addPlanet)
        self.add_button.grid(row = 1, column = 2)


        self.speed_label = tk.Label(self, text ='Simulation Speed')
        self.speed_label.grid(row = 2, column = 1)
        self.sim_speed = tk.Entry(self)
        self.sim_speed.grid(row = 2, column = 2)
        self.sim_speed.bind('<Return>', setSpeed)
         
        embed = tk.Frame(self, width = 1506, height = 760) #creates a frame to embed pygame window
        embed.grid(columnspan = (600), rowspan = 500)
        embed.grid(row = 1, column = 3)
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        if platform.system == "Windows": #if statement is required to keep this from running on Linux/Mac which would break
            os.environ['SDL_VIDEODRIVER'] = 'windib' 

        #setup the simulation screen
        MainWindow.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('sun')
        MainWindow.screen.fill(bgColour)
        pygame.draw.circle(self.screen,(255,255,0), (sunX, sunY), 14, 0) 
        pygame.display.update() 
    

class Planet:
    def __init__(self, mass, vi, angle, x, y):
        self.mass = mass
        self.vi = vi
        self.angle = angle
        self.x = x
        self.y = y
        self.dx = abs(x - sunX)
        self.dy = abs(y - sunY)
        self.radius = 4
        self.vx = vi * math.cos(angle)
        self.vy = vi * math.sin(angle)
        

    def render(self):
         #int(sizeco*math.pow(mass, .3333333333333))
        pygame.draw.circle(MainWindow.screen, (0,255,0), (int(self.x),int(self.y)) , self.radius , 0)

    def delete(self):
        pygame.draw.circle(MainWindow.screen, (0,0,0), (int(self.x), int(self.y)), self.radius, 0)

 
def newPlanet(mass, vi, angle, x, y):
    planet = Planet(mass, vi, angle, x, y)
    planetList.append(planet)
    print('planet added');

if __name__ == "__main__":
        root = tk.Tk()
        main = MainWindow(root)
        main.pack(side="top",fill="both",expand=True) 
                
def simulationLoop(): #main sim loop

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit
    
       #loop through every planet and update their properties
    for planet in planetList:
        pygame.draw.circle(MainWindow.screen,(255,255,0), (sunX, sunY), 14, 0) 
        planet.delete()
        planet.dx = abs(planet.x - sunX)
        planet.dy = abs(planet.y - sunY)
        r = (planet.dx + planet.dy)**2
        gravity = (sunMass * G)/((math.sqrt(((planet.dx*1e9)**2)+((planet.dy*1e9)**2)))**2) #Gmm/r2 , with the conversion from pixel to meter.
        if planet.dx == 0:
            theta = math.radians(90)
        else:
            theta = math.atan(planet.dy/planet.dx)
        gravx = gravity * math.cos(theta)
        gravy = gravity * math.sin(theta)

        #account for the fact that the co-ordinates are relative to the top left of the page

        if (planet.x - sunX) > 0:
            gravx = -1 * gravx
        if (planet.y - sunY) > 0:
            gravy = -1 * gravy

        #update the planet's speed and distance using standard kinematics equations
        
        planet.vy += gravy*dt
        planet.vx += gravx*dt
        planet.x += planet.vx*dt
        planet.y += planet.vy*dt 
        planet.render()

        
    #update the display, tick the clock and schedule the next loop    
    pygame.display.update()
    mainClock.tick_busy_loop(FPS)
    root.after(100, simulationLoop)

root.after(100, simulationLoop)
root.mainloop()






