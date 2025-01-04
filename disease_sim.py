import pygame
from person import Person
from game import Game
import pygame_menu
import random
import matplotlib.pyplot as plt
from IPython import display


def main():
    # Initialize pygame
    pygame.init()

    # Create instance of game.
    game = Game()

    # Set window size and start the clock.
    game.screen = pygame.display.set_mode((1200, 720))
    game.clock = pygame.time.Clock()

    # Create menu.
    menu = pygame_menu.Menu('Welcome', 600, 500,theme=pygame_menu.themes.THEME_BLUE)
    game.font = pygame.font.Font(None, 24)

    # Create inputs for the parameters.
    game.population_size = menu.add.text_input('Popuplation Size: ', default=200)
    game.infected_size = menu.add.text_input('Infected Population Size: ', default=1)
    game.spread_rate = menu.add.text_input('Spread Rate: ', default=50)
    game.death_rate = menu.add.text_input('Death Rate: ', default=50)
    game.radius = menu.add.text_input('Circle Radius: ', default=5)
    game.recovery_time = menu.add.text_input('Recovery Time in Seconds: ', default=10)
    # Adds the Play and Quit Button.
    menu.add.button('Play', lambda: running_simulation(game,game.population_size.get_value(),game.infected_size.get_value(),game.spread_rate.get_value(),game.death_rate.get_value(),game.radius.get_value(),game.recovery_time.get_value()))
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







def running_simulation(game,pop,inf,spr,dea,radius,recovery_time):

    # Initialize the timer variable
    elapsed_time = 0

    # The simulation parameters that where assigned in the starting menu.
    total_population = int(pop)
    infected = int(inf)
    spread_rate = int(spr)
    death_rate = int(dea)
    avg_recovery_time = int(recovery_time)*60

    # Initialize list that will hold population ammounts for each fram, used for plotting.
    plot_dead = []
    plot_healthy = []
    plot_recovered = []
    plot_infected = []

    # Initialize the list of dead people, will start out as empty.
    dead_list = []

    # Create the initial grid of people.
    grid = create_population_grid(total_population,infected,radius,avg_recovery_time)

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

        # Iterate through and check for colisions.
        for row in grid:
            for colum in row:
                for person in colum:
                    person.move()
                    person.collision(grid,spread_rate)
                    person.recovery_or_die(death_rate)

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

        # Update positioning in grid.
        for i,row in enumerate(grid):
            for j,colum in enumerate(row):
               for person in colum:
                    if person.infection_status == 'dead':
                        dead_list.append(person)
                        colum.remove(person)
                    elif i != int(person.gridx) or j != int(person.gridy):
                        colum.remove(person)
                        grid[int(person.gridx)][int(person.gridy)].append(person)

        draw_screen(game,grid,dead_list,healthy_population,infected_population,recovered_population,total_population,elapsed_time)

        # Append population ammounts to plot lists.
        plot_healthy.append(healthy_population)
        plot_infected.append(infected_population)
        plot_recovered.append(recovered_population)
        plot_dead.append(len(dead_list))

        # Update the elapsed_time variable safely depending on how long the frame took.
        elapsed_time += 1 / 60

        if (infected_population == 0):
            game.running = False

    # Draw chart when done.
    plot(plot_healthy,plot_infected,plot_dead,plot_recovered)





def draw_screen(game,grid,dead_list,healthy_population,infected_population,recovered_population,total_population,elapsed_time):

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
    #pygame.draw.rect(game.screen, (0,200,0), pygame.Rect(8, 10, 235, 85))
    population_background = pygame.Surface((220+len(str(total_population))*10, 85))
    population_background.fill((0, 255, 0))  # Fill with green color
    population_background.set_alpha(200)  # Set transparency (adjust as needed)
    game.screen.blit(population_background, (8, 10))


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

    # Display elapsed time in the top right corner with 2 decimal places and a green box background
    timer_text = game.font.render(f"Time: {elapsed_time:.2f} seconds", True, pygame.Color("black"))
    timer_background = pygame.Surface((timer_text.get_width(), timer_text.get_height()))
    timer_background.fill((0, 255, 0))  # Fill with green color
    timer_background.set_alpha(200)  # Set transparency (adjust as needed)
    game.screen.blit(timer_background, (game.screen.get_width() - timer_text.get_width() - 15, 10))
    game.screen.blit(timer_text, (game.screen.get_width() - timer_text.get_width() - 10, 10))

    # 60 fps.
    pygame.display.flip()
    game.clock.tick(60)

def plot(healthy, infected, dead, recovered):
    thickness = 5
    display.clear_output(wait=True)
    plt.clf()
    plt.title('Populations')
    plt.xlabel('Time')
    plt.ylabel('Population amount')
    plt.plot(healthy, label='Healthy', color='green', linewidth=thickness)
    plt.plot(infected, label='Infected', color='red', linewidth=thickness)
    plt.plot(dead, label='Dead', color='black', linewidth=thickness)
    plt.plot(recovered, label='Recovered', color='blue', linewidth=thickness)
    plt.ylim(ymin=0)
    plt.legend()  # Add legend to the plot
    plt.show(block=False)
    plt.pause(0.1)






def create_population_grid(population, infected_population,radius,recovery_time):
    # Initialize radius of circle.
    radius = int(radius)

    # Initialized cell size.
    grid_cell_size = (radius*2)

    # The number of collums and rows.
    num_columns = 720//grid_cell_size
    num_rows = 1200//grid_cell_size

    # Creates a grid with each zone having an empty list where people will go.
    grid = [[[] for _ in range(num_columns+2)] for _ in range(num_rows+2)]

    # Creates people and adds to the list.
    for index in range(population):

        coords= True
        while (coords):
            coords = False
            # Create random x and y values where the people will spawn.
            x = random.randint(0+(radius+1), 1200-(radius+1))
            y = random.randint(0+(radius+1), 720-(radius+1))


            for i in range(-1, 2):
                for j in range(-1, 2):
                    gridx = int(x//grid_cell_size)+i
                    gridy = int(y//grid_cell_size)+j
                    
                    if 0<gridx >= num_rows or 0<gridy >= num_columns:
                        continue

                    people = grid[gridx][gridy]

                    for person in people:
                        distance = distance_calc(x, y, person.x, person.y)
                        if distance<(radius*2)**2+5:
                            coords = True
                            break
                    if coords:
                        break
                if coords:
                    break



        # Set the disease status and color
        if index < infected_population:
            diseased = 'diseased'
            color = 'red'
        else:
            diseased = 'healthy'
            color = 'blue'
        
        # Create a new person object and add it to the array
        person = Person(x, y, diseased, color, radius, recovery_time)
        #print(f'gridx {person.gridx} gridy {person.gridy}')
        grid[person.gridx][person.gridy].append(person)

    return grid

def distance_calc(x1,x2,y1,y2): #Tested

    # The math to tell if a circle collides. Its just the distance formula.
    distance = ((x1 - x2)**2 + (y1 - y2)**2)
    return distance

if __name__ == "__main__":

   main()
