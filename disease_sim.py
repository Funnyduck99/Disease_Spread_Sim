import pygame
from person import Person
from game import Game
import pygame_menu
import math
import random


def main():
    x =5
    pygame.init()
    game = Game()
    game.screen = pygame.display.set_mode((1200, 720))
    game.clock = pygame.time.Clock()

    menu = pygame_menu.Menu('Welcome', 500, 400,theme=pygame_menu.themes.THEME_BLUE)
    game.font = pygame.font.Font(None, 24)

    game.population_size = menu.add.text_input('Popuplation Size: ', default=200)
    game.infected_size = menu.add.text_input('Infected Population Size: ', default=1)
    game.spread_rate = menu.add.text_input('Spread Rate: ', default=50)
    game.death_rate = menu.add.text_input('Death Rate: ', default=50)
    menu.add.button('Play', lambda: start_the_game(game,game.population_size.get_value(),game.infected_size.get_value(),game.spread_rate.get_value(),game.death_rate.get_value()))
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(game.screen)


    game.running = True
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
        # fill the screen with a color to wipe away anything from last frame
        game.screen.fill("black")
        pygame.draw.rect(game.screen, "white", (300, 0, 900, 720))
        



        pygame.display.flip()
        game.clock.tick(60)







def start_the_game(game,pop,inf,spr,dea):
    population = int(pop)
    infected = int(inf)
    spread_rate = int(spr)
    death_rate = int(dea)
    dead_list = []
    grid = create_people(population,infected)
    game.running = True
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
        game.screen.fill("white")
        for person in dead_list:
            pygame.draw.circle(game.screen, person.color, (person.x,person.y), person.radius)
        for row in grid:
            for sublist in row:
                # Access and process each sublist
                for person in sublist:
                    person.move()
                    person.recovery_or_die(death_rate)
                    pygame.draw.circle(game.screen, person.color, (person.x, person.y), person.radius)
        #temp_list = [[[] for _ in range(num_columns)] for _ in range(num_rows)]
        for i,row in enumerate(grid):
            for j,colum in enumerate(row):
                for person in colum:
                    if i != int(person.gridx):
                        grid[int(i)][int(j)].remove(person)
                        grid[int(person.gridx)][int(person.gridy)].append(person)
                    elif j != int(person.gridy):
                        grid[int(i)][int(j)].remove(person)
                        grid[int(person.gridx)][int(person.gridy)].append(person)

                    #temp_list[int(person.gridx)][int(person.gridy)].append(person)
       # grid = temp_list
        
        
        for row in grid:
            for colum in row:
                for person in colum:
                    person.collision(grid,spread_rate)
        for row in grid:
            for people in row:
                for person in people:
                    if person.infection_status == 'dead':
                        if (person.x <= person.radius):
                            person.x = person.radius
                        if (person.x >= person.width - person.radius):
                            person.x = person.width -person.radius
                        if (person.y <= 0+person.radius):
                            person.y=person.radius
                        if (person.y >= person.height - person.radius):
                            person.y = person.height-person.radius
                        dead_list.append(person)
                        people.remove(person)

        fps = str(int(game.clock.get_fps()))
        fps_text = game.font.render(f"FPS: {fps}", True, pygame.Color("black"))
        game.screen.blit(fps_text, (10, 10))


        pygame.display.flip()
        game.clock.tick(60)











def create_people(population, infected_population):
    global number
    radius = 5
    num_columns = 720//10
    num_rows = 1200//10

    grid = [[[] for _ in range(num_columns)] for _ in range(num_rows)]


    temp_list = []

    for index in range(population):
        

        pick_cord = True
        while pick_cord == True:
            pick_cord = False
            x = random.randint(0+radius, 1200-radius)
            y = random.randint(0+radius, 720-radius)

            # Check for collisions with other people in the array
            if (len(temp_list)== 0):
          
                continue
          
            else:
                for dot in temp_list:
                    if (math.sqrt(math.pow((dot.x - x),2) + math.pow((dot.y - y),2))<11): #distance formula between the new dot and all other dots on the canvas if it isnt touching any then it can go there
                        
                        pick_cord = True
        # Set the disease status and color
        if index < infected_population:
            diseased = 'diseased'
            color = 'red'
        else:
            diseased = 'healthy'
            color = 'blue'
        
        # Create a new person object and add it to the array
        person = Person(x, y, diseased, color, radius)
        grid[person.x//10][person.y//10].append(person)

    return grid



if __name__ == "__main__":

   main()


