import random
import math


class Person:
    def __init__(self, x_position, y_position,status,color,radius):
        # Assign color.
        self.color = color

        # Assign x and y position.
        self.x = x_position
        self.y = y_position

        # Assign infection status.
        self.infection_status = status

        # Randomizes its starting direction.
        self.direction = random.randint(1, 359)  # Add a random direction attribute
        radians = math.radians(self.direction)
        self.siny = math.sin(radians)
        self.cosx = math.cos(radians)

        # Assigns radius length.
        self.radius = radius

        # Assigns recovery time.
        self.recovery_time = 500
        self.recovered = 0

        #Width and height of canvas.
        self.width = 1200 
        self.height = 720 

        # Assigns initial grid position. 
        self.gridx = self.x//10
        self.gridy = self.y//10





    def move(self):
        # If the x position hits the wall flip the x movement and set the position to its radius.
        if (self.x <= self.radius):
            self.x = self.radius
            self.cosx = -self.cosx

         # If the x position hits the wall flip the x movement and set the position to its the width of canvas - radius.
        if (self.x >= self.width - self.radius):
            self.x = self.width -self.radius
            self.cosx = -self.cosx

        # If Y position hits wall, set y to radius.
        if (self.y <= 0+self.radius):
            self.y=self.radius
            self.siny = -self.siny

        # If y hits wall set y to canvas height - radius.
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
        
        # Loops through adjacent places on the grid to avoid unnecessary checks.
        for i in range(-1,2,1):
            for j in range(-1,2,1):

                # Assign the grid value you are checking for collisions in.
                gridx=self.gridx+i
                gridy=self.gridy+j

                # If the x or y it wants to check on the grid is out of bounds, then continue.
                if (gridx >= 120 ) or (gridy >= 72):
                    continue
                
                # Creates a pointer to the array of people in a spot on the grid.
                people = grid[int(gridx)][int(gridy)]

                # Iterates through people in its section of grid.
                for person in people:

                    # If it is checking against itself then continue to next person.
                    if person is self:
                        continue

                    # Runs the x and y values through a distance formula.
                    distance = distance_calc(self.x, person.x, self.y, person.y)

                    # If the circles don't touch then continues to the next person.
                    if distance > 100:
                        continue
                    # Checks if it will spread or not.
                    if spread >= random.randint(1, 100):
                            
                        # Checks if one is diseased
                        if person.infection_status == 'diseased' and self.infection_status == 'healthy':
                            self.infection_status = 'diseased'
                            self.color = 'red'
                        elif self.infection_status == 'diseased' and person.infection_status == 'healthy':
                            person.infection_status = 'diseased'
                            person.color = 'red'

                    # When colliding, 2 circles swap momentum.
                    self.cosx, self.siny, person.cosx, person.siny = person.cosx, person.siny, self.cosx, self.siny
                    
                    # Makes sure that the circles don't get trapped in eachother although this causes bug of them jumping around.
                    while distance <= 100:
                        self.x += self.cosx
                        self.y += self.siny
                        distance = distance_calc(self.x, person.x, self.y, person.y)
                            



    def recovery_or_die(self,death_rate):
        
        # Checks if the person is diseased.
        if (self.infection_status == 'diseased'):

            # Adds a to the counter until its deturmined whether it dies or not.
            self.recovered+=1

            # Checks if it has reached the time.
            if (self.recovery_time<self.recovered):

                # Checks if the random number falls in the death range.
                if (random.randint(1,100)>100-death_rate):

                    # Kills the person and turns them black.
                    self.infection_status = 'dead'
                    self.color = 'black'
                else:

                    # Person survives and now is green and can no longer be infected.
                    self.infection_status = 'recovered'
                    self.color = 'green'





def distance_calc(x1,x2,y1,y2): #Tested

    # The math to tell if a circle collides. Its just the distance formula.
    distance = ((x1 - x2)**2 + (y1 - y2)**2)
    return distance