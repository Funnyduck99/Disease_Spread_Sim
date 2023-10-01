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
        self.y_movement = math.sin(radians)
        self.x_movement = math.cos(radians)

        # Assigns radius length.
        self.radius = radius
        self.collision_distance = (self.radius*2)**2

        # Assigns recovery time.
        self.recovery_time = 500
        self.recovered = 0

        #Width and height of canvas.
        self.width = 1200 
        self.height = 720 

        # Assigns initial grid position. 
        self.grid_cell_size = (self.radius*2)
        self.gridx = self.x//self.grid_cell_size
        self.gridy = self.y//self.grid_cell_size

        # Assign grid size.
        self.grid_width = self.width//self.grid_cell_size
        self.grid_height = self.height//self.grid_cell_size





    def move(self):
        # If the x position hits the wall flip the x movement and set the position to its radius.
        if (self.x <= self.radius):
            self.x = self.radius
            self.x_movement = -self.x_movement

         # If the x position hits the wall flip the x movement and set the position to its the width of canvas - radius.
        if (self.x >= self.width - self.radius):
            self.x = self.width -self.radius
            self.x_movement = -self.x_movement

        # If Y position hits wall, set y to radius.
        if (self.y <= 0+self.radius):
            self.y=self.radius
            self.y_movement = -self.y_movement

        # If y hits wall set y to canvas height - radius.
        if (self.y >= self.height - self.radius):
            self.y_movement = -self.y_movement
            self.y = self.height-self.radius

        # Adds movement values to current position.
        self.y += self.y_movement
        self.x += self.x_movement
        
        # Updates internal grid position.
        self.gridx = self.x//self.grid_cell_size
        self.gridy = self.y//self.grid_cell_size


    def collision(self, grid, spread):
        for i in range(-1, 2):
            for j in range(-1, 2):
                gridx = self.gridx + i
                gridy = self.gridy + j

                if gridx >= self.grid_width or gridy >= self.grid_height:
                    continue

                people = grid[int(gridx)][int(gridy)]

                for person in people:
                    if person is self:
                        continue

                    distance = distance_calc(self.x, person.x, self.y, person.y)
                    if distance < 1e-6:  # Adjust the threshold value as needed
                        continue

                    if distance <= self.collision_distance:
                        dist_sqrt = math.sqrt(distance)
                        overlap = self.radius + person.radius - dist_sqrt

                        nx = (self.x - person.x) / dist_sqrt
                        ny = (self.y - person.y) / dist_sqrt

                        self.x += overlap * nx
                        self.y += overlap * ny
                        person.x -= overlap * nx
                        person.y -= overlap * ny

                        rel_velocity_x = self.x_movement - person.x_movement
                        rel_velocity_y = self.y_movement - person.y_movement

                        impulse = (2.0 * (rel_velocity_x * nx + rel_velocity_y * ny)) / (self.radius + person.radius)

                        self.x_movement -= impulse * person.radius * nx
                        self.y_movement -= impulse * person.radius * ny
                        person.x_movement += impulse * self.radius * nx
                        person.y_movement += impulse * self.radius * ny

                        if spread >= random.randint(1, 100):
                            if person.infection_status == 'diseased' and self.infection_status == 'healthy':
                                self.infection_status = 'diseased'
                                self.color = 'red'
                            elif self.infection_status == 'diseased' and person.infection_status == 'healthy':
                                person.infection_status = 'diseased'
                                person.color = 'red'

                            



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