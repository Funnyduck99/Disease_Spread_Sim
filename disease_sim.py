import pygame
from person import Person
from game import Game
import pygame_menu
import math
import random


def main():
    # Initialize pygame
    pygame.init()

    # Create instance of game.
    game = Game()

    # Set window size and start the clock.
    game.screen = pygame.display.set_mode((1200, 720))
    game.clock = pygame.time.Clock()

    # Create menu.
    menu = pygame_menu.Menu('Welcome', 500, 400,theme=pygame_menu.themes.THEME_BLUE)
    game.font = pygame.font.Font(None, 24)

    # Create inputs for the parameters.
    game.population_size = menu.add.text_input('Popuplation Size: ', default=200)
    game.infected_size = menu.add.text_input('Infected Population Size: ', default=1)
    game.spread_rate = menu.add.text_input('Spread Rate: ', default=50)
    game.death_rate = menu.add.text_input('Death Rate: ', default=50)

    # Adds the Play and Quit Button.
    menu.add.button('Play', lambda: running_simulation(game,game.population_size.get_value(),game.infected_size.get_value(),game.spread_rate.get_value(),game.death_rate.get_value()))
    menu.add.button('Quit', pygame_menu.events.EXIT)

    # Loops through menu.
    menu.mainloop(game.screen)

    # Set game running to be true.
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







def running_simulation(game,pop,inf,spr,dea):

    # The simulation parameters that where assigned in the starting menu.
    total_population = int(pop)
    infected = int(inf)
    spread_rate = int(spr)
    death_rate = int(dea)


    # Initialize the list of dead people, will start out as empty.
    dead_list = []

    # Create the initial grid of people.
    grid = create_population_grid(total_population,infected)

    # Set the simulation running to True.
    game.running = True

    # The main loop.
    while game.running:

        # Checks events for if the red x is clicked to close simulation.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

        # Sets populations to 0.
        healthy_population = 0
        recovered_population = 0
        infected_population = 0

        # Iterate through and update positioning and check infection status.
        for row in grid:
            for sublist in row:
                for person in sublist:
                    person.move()
                    person.recovery_or_die(death_rate)

        # Iterate through and check for colisions.
        for row in grid:
            for colum in row:
                for person in colum:
                    person.collision(grid,spread_rate)

        # Update positioning in grid.
        for i,row in enumerate(grid):
            for j,colum in enumerate(row):
                for person in colum:
                    if i != int(person.gridx):
                        grid[int(i)][int(j)].remove(person)
                        grid[int(person.gridx)][int(person.gridy)].append(person)
                    elif j != int(person.gridy):
                        grid[int(i)][int(j)].remove(person)
                        grid[int(person.gridx)][int(person.gridy)].append(person)


        

        # When person dies make sure that their position is in bounds to avoid graphical glitches, move them from the grid to the dead list.
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

        # Finds sizes of each population
        for i,row in enumerate(grid):
            for j,colum in enumerate(row):
                for person in colum:
                    if person.infection_status == 'diseased':
                        infected_population+=1
                    elif person.infection_status == 'healthy':
                        healthy_population+=1
                    elif person.infection_status == 'recovered':
                        recovered_population+=1

        draw_screen(game,grid,dead_list,healthy_population,infected_population,recovered_population,total_population)



def draw_screen(game,grid,dead_list,healthy_population,infected_population,recovered_population,total_population):

    # Fill the screen white.
    game.screen.fill("white")

    # Draw the dead people before the living so they are shown behind them.
    for person in dead_list:
        pygame.draw.circle(game.screen, person.color, (person.x,person.y), person.radius)

    # Draw the living people.
    for row in grid:
        for sublist in row:
            for person in sublist:
                pygame.draw.circle(game.screen, person.color, (person.x, person.y), person.radius)

    # Background for the info.
    pygame.draw.rect(game.screen, (0,200,0), pygame.Rect(8, 10, 235, 85))

    #  Show fps counter in top left.
    fps = str(int(game.clock.get_fps()))
    fps_text = game.font.render(f"FPS: {fps}", True, pygame.Color("black"))
    game.screen.blit(fps_text, (10, 10))

    # Display Total Population.
    population_text = game.font.render(f"Population Size: {total_population}", True, pygame.Color("black"))
    game.screen.blit(population_text, (10, 24))

    # Display healthy Population.
    healthy_text = game.font.render(f"Healthy Population Size: {healthy_population}", True, pygame.Color("black"))
    game.screen.blit(healthy_text, (10, 38))

    # Display recovered Population.
    recovered_text = game.font.render(f"Recovered Population Size: {recovered_population}", True, pygame.Color("black"))
    game.screen.blit(recovered_text, (10, 52))

    # Display infected Population.
    infected_text = game.font.render(f"Infected Population Size: {infected_population}", True, pygame.Color("black"))
    game.screen.blit(infected_text, (10, 66))

    # Display dead Population.
    dead_text = game.font.render(f"Dead Population Size: {len(dead_list)}", True, pygame.Color("black"))
    game.screen.blit(dead_text, (10, 80))

    # 60 fps.
    pygame.display.flip()
    game.clock.tick(60)






def create_population_grid(population, infected_population):
    # Initialize radius of circle.
    radius = 5

    # The number of collums and rows.
    num_columns = 720//10
    num_rows = 1200//10

    # Creates a grid with each zone having an empty list where people will go.
    grid = [[[] for _ in range(num_columns)] for _ in range(num_rows)]

    # Creates people and adds to the list.
    for index in range(population):

        # Create random x and y values where the people will spawn.
        x = random.randint(0+radius, 1200-radius)
        y = random.randint(0+radius, 720-radius)


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


