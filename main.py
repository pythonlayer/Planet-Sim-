# Example file showing a circle moving on screen
import pygame
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
running = True
dt = 0

class point:
    AU=149597871
    G=6.67*10**-8.5
    SCALE=500/AU
    def __init__(self,position,mass,radius,color,type=0):
        self.pos = position
        self.r = radius
        self.m = mass
        self.COLOR= color
        self.t=type
        self.vel=pygame.Vector2(0,0)
    def draw(self,x,y):
        pygame.draw.circle(screen,self.COLOR,(x,y),self.r)
    def move(self,other):
        distance = math.sqrt((other.pos.x - self.pos.x) ** 2 + (other.pos.y - self.pos.y) ** 2)
            
        if distance != 0:  # Prevent division by zero
            if self.m < 0:  # Handling negative mass
                force = -abs((self.G * self.m * other.m) / (distance ** 2))
            else:
                force = (self.G * self.m * other.m) / (distance ** 2)
        else:
            force = 0
            
        angle = math.atan2(other.pos.y - self.pos.y, other.pos.x - self.pos.x)
        force_x = force * math.cos(angle)
        force_y = force * math.sin(angle)
        
        if self.m != 0:  # Check for massless object
            acceleration_x = (force_x * dt) / self.m
            acceleration_y = (force_y * dt) / self.m
        else:
            acceleration_x = force_x * dt
            acceleration_y = force_y * dt

        self.vel.x += acceleration_x
        self.vel.y += acceleration_y
            
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
    def collide(self, other, planet_list):
        distance = math.sqrt((other.pos.x - self.pos.x) ** 2 + (other.pos.y - self.pos.y) ** 2)
        if distance*self.SCALE < self.r:
            if self.t == 0:
                if abs(self.m) > abs(other.m):
                    self.m += other.m
                    self.r += other.r
                    planet_list.remove(other)
                elif abs(self.m) < abs(other.m):
                    other.m += self.m
                    other.r += self.r
                    planet_list.remove(self)
                else:
                    self.vel*=-1
                    self.m-=1/self.m
                    other.m-=1/other.m
                    planet_list.append(point(self.pos+other.pos /2,1/self.m,self.r,self.COLOR))
                    planet_list.append(point(self.pos-other.pos /2,1/self.m,self.r,other.COLOR))
                    planet_list[-1].vel=self.vel/2
                    planet_list[-2].vel=other.vel/2



def display_stats(planet):
    mass_display = int(planet.m / 10**10)
    print(f"Selected Planet Stats:")
    print(f"Mass: {mass_display} x 10^10 kg")
    print(f"Radius: {planet.r} units")

def modify_planet_stats(planet):
    choice = input("Enter 'M' to modify mass, 'R' to modify radius, or 'E' to exit: ").upper()
    if choice == 'M':
        new_mass = float(input("Enter the new mass in scientific notation (e.g., 2e30): "))
        planet.m = new_mass
    elif choice == 'R':
        new_radius = int(input("Enter the new radius: "))
        planet.r = new_radius
    elif choice == 'E':
        return
    else:
        print("Invalid choice. Please enter 'M', 'R', or 'E'.")
        modify_planet_stats(planet)

planets=[
    point(pygame.Vector2(0,0),10**30,20,(255,255,0)),  # Sun
    point(pygame.Vector2(0,point.AU*1.56),10**27,8,(0,25,25)),  # Earth
    point(pygame.Vector2(0,point.AU),10**22,5,(0,5,25)),  # Earth
    point(pygame.Vector2(0,point.AU*0.5),10**21,5,(43,255,255)),
    point(pygame.Vector2(0,point.AU*0.59),10**21,5,(43,255,255)),  # Earth
    point(pygame.Vector2(point.AU*1.56,0),10**27,8,(0,25,25)),  # Earth
]
planets[1].vel = pygame.Vector2(-6*10**6,0)
planets[2].vel = pygame.Vector2(6*10**6,0)
planets[3].vel = pygame.Vector2(6*10**6,0)
planets[4].vel = pygame.Vector2(-6*10**6,0)
planets[5].vel = pygame.Vector2(0,-6*10**6)
view_x = 0
view_y = 0
displaying_stats = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    speed = 1000
    if keys[pygame.K_LEFT]:
        view_x += speed * dt
    elif keys[pygame.K_RIGHT]:
        view_x -= speed * dt
    elif keys[pygame.K_UP]:
        view_y += speed * dt
    elif keys[pygame.K_DOWN]:
        view_y -= speed * dt

    screen.fill((25, 24, 50))

    # Check if mouse hovers over a planet to display its stats
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for planet in planets:
        adjusted_x = planet.pos.x * point.SCALE + (screen.get_height() * 0.5) + view_x
        adjusted_y = planet.pos.y * point.SCALE + (screen.get_width() * 0.5) + view_y
        x = adjusted_x
        y = adjusted_y
        if math.sqrt((mouse_x - x) ** 2 + (mouse_y - y) ** 2) <= planet.r:
            display_stats(planet)
            break

        planet.draw(x, y)
        for other in planets:
            if other != planet:
                planet.collide(other,planets)
                planet.move(other)

    pygame.display.flip()

    dt = clock.tick(60) / 500

pygame.quit()
