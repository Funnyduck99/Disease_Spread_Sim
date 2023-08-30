import random
import math


class Person:
    def __init__(self, x_position, y_position,status,color,radius):
        self.color = color
        self.x = x_position
        self.y = y_position
        self.infection_status = status
        self.direction = random.randint(1, 359)  # Add a random direction attribute
        radians = math.radians(self.direction)
        self.siny = math.sin(radians)
        self.cosx = math.cos(radians)
        self.radius = radius
        self.recovery_time = 500
        
        self.recovered = 0


        self.width = 1200  # width of the canvas
        self.height = 720  # height of the canvas


        self.gridx = self.x//10
        self.gridy = self.y//10





    def move(self):
        # If the x position hits the wall flip the x movement and set the position to its radius.
        if (self.x <= self.radius):
            self.x = self.radius
            self.cosx = -self.cosx

        if (self.x >= self.width - self.radius):
            self.x = self.width -self.radius
            self.cosx = -self.cosx

        if (self.y <= 0+self.radius):
            self.y=self.radius
            self.siny = -self.siny

        if (self.y >= self.height - self.radius):
            self.siny = -self.siny
            self.y = self.height-self.radius

        # Adds movement values to current position.
        self.y += self.siny
        self.x += self.cosx
        
        # Updates internal grid position.
        self.gridx = self.x//10
        self.gridy = self.y//10


    def collision(self, grid, spread):
        
        for i in range(-1,2,1):
            for j in range(-1,2,1):

                gridx=self.gridx+i
                gridy=self.gridy+j
                #print(f"gridx {gridx} gridy {gridy}")
                if (gridx >= 120 ) or (gridy >= 72):
                    continue
                
                
                people = grid[int(gridx)][int(gridy)]
                for person in people:
                    if person is self:
                        continue
                    distance = distance_calc(self.x, person.x, self.y, person.y)
                    if distance > 100:
                        continue
                    if spread >= random.randint(1, 100):
                            
                        
                        
                        if person.infection_status == 'diseased' and self.infection_status == 'healthy':
                            self.infection_status = 'diseased'
                            self.color = 'red'
                            self.recovered = 0
                        elif self.infection_status == 'diseased' and person.infection_status == 'healthy':
                            person.infection_status = 'diseased'
                            person.color = 'red'
                            person.recovered = 0
                    self.cosx, self.siny, person.cosx, person.siny = person.cosx, person.siny, self.cosx, self.siny
                        
                    while distance <= 100:
                        self.x += self.cosx
                        self.y += self.siny
                        distance = distance_calc(self.x, person.x, self.y, person.y)
                            



    def recovery_or_die(self,death_rate):
        
        if (self.infection_status == 'diseased'):
            self.recovered+=1
            if (self.recovery_time<self.recovered):
                if (random.randint(1,100)>100-death_rate):
                    self.infection_status = 'dead'
                    self.color = 'black'
                else:
                    self.infection_status = 'recovered'
                    self.color = 'green'





def distance_calc(x1,x2,y1,y2): #Tested
    distance = ((x1 - x2)**2 + (y1 - y2)**2)#the math to tell if a circle collides. Its just the distance formula.
    return distance