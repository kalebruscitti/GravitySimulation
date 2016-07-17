
import pygame, math, sys, os, platform, time
import Tkinter as tk
from Tkinter import *
from pygame.locals import *

#simulation variables 
edge_clamp = False
bgColour = (0,0,0)
G = 6.67e-11
width, height = 1506, 760
FPS = 60
sunX = width/2
sunY = height/2
sunMass = 1.989e30
planetList = []
mainClock = pygame.time.Clock()
bgmColour = (255,255,255)
width_m = 400
height_m = 960
dt = 10000


def sol(): #function that creates our solar system

    newPlanet(3.30e23, 56600, math.radians(90), sunX + 46, sunY, 212, 180, 140) #mercury
    newPlanet(4.87e24, 35000, math.radians(90), sunX + 107, sunY, 235, 106, 0) #venus
    newPlanet(5.97e24, 30300, math.radians(90), sunX + 147, sunY, 0, 255, 0) #earth
    newPlanet(6.24e23, 26500, math.radians(90), sunX + 206, sunY, 255, 0, 0) #mars
    newPlanet(1.898e27, 13720, math.radians(90), sunX + 740, sunY, 237, 148, 76)#jupiter 
    

def setSpeed(event):
    
    global dt
    dt = int(event.widget.get())*10000
    

def addPlanet():
                
    top = tk.Toplevel(root)
    top.wm_title("Add Planet")
                
    add_mass = tk.Entry(top)
    add_mass.grid(row=1, column=3)
    add_mass.delete(0, END)
    add_mass.insert(0, "6e24")
    mass_label=tk.Label(top, text = "Mass (KG)")
    mass_label.grid(row=1, column=1)
                
    add_vi = tk.Entry(top)
    add_vi.grid(row=2, column =3)
    add_vi.delete(0, END)
    add_vi.insert(0, "30300")
    vi_label=tk.Label(top, text="Inital Velocity (m/s)")
    vi_label.grid(row=2, column=1)

    add_angle = tk.Entry(top)
    add_angle.grid(row=3, column=3)
    add_angle.delete(0, END)
    add_angle.insert(0, 90)
    angle_label=tk.Label(top, text="Velocity Angle (Deg)")
    angle_label.grid(row=3, column=1)

    add_radius = tk.Entry(top)
    add_radius.grid(row=4, column=3)
    add_radius.delete(0, END)
    add_radius.insert(0, 147)
    radius_label=tk.Label(top, text="Orbital Radius (Million KM)")
    radius_label.grid(row=4, column=1)

    rgb_label = tk.Label(top, text = 'R G B')
    rgb_label.grid(row=5, column = 1)

    set_r = tk.Entry(top)
    set_r.grid(row=5, column=2)
    set_r.delete(0, END)
    set_r.insert(0, 0)

    set_g = tk.Entry(top)
    set_g.grid(row=5, column=3)
    set_g.delete(0, END)
    set_g.insert(0, 255)

    set_b = tk.Entry(top)
    set_b.grid(row=5, column=4)
    set_b.delete(0, END)
    set_b.insert(0, 0)
    
    def checkValues():
        nmass = float(add_mass.get())
        nvi = float(add_vi.get())
        ndegrees = float(add_angle.get())
        nangle = math.radians(ndegrees)
        nradius = float(add_radius.get())
        nr = int(set_r.get())
        ng = int(set_g.get())
        nb = int(set_b.get())
        newPlanet(nmass, nvi, nangle, sunX + nradius, sunY, nr, ng, nb)

    b_go = tk.Button(top, text="go", command = checkValues)
    b_go.grid(row=7, column=3)

def clear():
    for planet in planetList:
        planet.delete()
        planetList.remove(planet)
                
class MainWindow(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, width = 100, *args, **kwargs)

        #add the UI
        self.add_button = tk.Button(self, text='Add Planet', padx = 10, pady = 10, command = addPlanet)
        self.add_button.grid(row = 1, columnspan=2, column = 1)

        self.speed_label = tk.Label(self, text ='Simulation Speed')
        self.speed_label.grid(row = 2, column = 1)
        self.sim_speed = tk.Entry(self)
        self.sim_speed.grid(row = 2, column = 2)
        self.sim_speed.bind('<Return>', setSpeed)
        self.sim_speed.insert(0, 1)

        self.clear_all = tk.Button(self, text="Clear Planets", padx = 10, pady = 10, command = clear)
        self.clear_all.grid(columnspan=2, row=5, column=1)

        self.scale = tk.Label(self, text = "Scale: 1 pixel = 1 Million KM")
        self.scale.grid(row=4, columnspan=2, column=1)

        self.warn = tk.Label(self, text = "Speeds over 10x cause inaccuracy")
        self.warn.grid(row=3, columnspan=2, column=1)
         
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
        self.dx = abs(x - sunX) * 1e9
        self.dy = abs(y - sunY) * 1e9
        if mass < 1e25:
            self.radius = 4
        else:
            self.radius = 8

        self.vx = self.vi * math.cos(angle)
        self.vy = self.vi * math.sin(angle)
        

    def render(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b
        pygame.draw.circle(MainWindow.screen, (self.r,self.g,self.b), (int(self.x),int(self.y)) , self.radius , 0)

    def delete(self):
        pygame.draw.circle(MainWindow.screen, (0,0,0), (int(self.x), int(self.y)), self.radius, 0)

 
def newPlanet(mass, vi, angle, x, y, r, g, b):
    planet = Planet(mass, vi, angle, x, y)
    planet.render(r,g,b)
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
        
        r = math.sqrt((planet.dx**2 + planet.dy**2))
        gravity = (sunMass * G)/(r**2) #Gmm/r2                      
        if planet.dx == 0:
            theta = math.radians(90)
        else:
            theta = math.atan(planet.dy/planet.dx)
        gravx = gravity * abs(math.cos(theta))
        gravy = gravity * abs(math.sin(theta))
        

        #account for the fact that the co-ordinates are relative to the top left of the page

        if (planet.x - sunX) > 0:
            a_gravx = -1 * gravx
        else:
            a_gravx = gravx
        if (planet.y - sunY) > 0:
            a_gravy = -1 * gravy
        else:
            a_gravy = gravy

        #update the planet's speed and distance using standard kinematics equations
    
        planet.vy += a_gravy*dt
        planet.vx += a_gravx*dt
        planet.vy_pix = planet.vy/1e9
        planet.vx_pix = planet.vx/1e9
        planet.x += planet.vx_pix*dt
        planet.y += planet.vy_pix*dt
        planet.dx = abs(planet.x - sunX) * 1e9
        planet.dy = abs(planet.y - sunY) * 1e9
        #print(math.sqrt(planet.dx**2 + planet.dy**2));
        planet.render(planet.r,planet.g,planet.b)

        
    #update the display, tick the clock and schedule the next loop    
    pygame.display.update()
    mainClock.tick_busy_loop(FPS)
    root.after(1, simulationLoop)

root.after(1, simulationLoop)
root.mainloop()






