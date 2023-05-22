# Program     : Wall Class
# Name        : Georgios Dialynas-Vatsis
# Date        : June 16, 2022
# Description : Manages wall generation, that's it.
import pygame
import random
class Wall:
    divisor = 10

    # Time in frames for how long to delete a wall
    lifetime = 1 * 60

    walls = []
    def __init__(self,x,y,width,length):
        Wall.walls.append(self)

        # Top left position for the wall
        self.x = x
        self.y = y

        # Length and width of the wall.
        self.width = width
        self.length = length

        # This is obvious
        self.color = "white"

        

    # This generates 
    def generate(width,length):
        Wall.no_wall_area = []
        Wall.walls = []
        # This is the ratio of non spawned walls to spawned walls 
        # For example 2 would be 50%, 3 would be 33%
        # Must be int
        upper = 2

        # this generates a width for each wall based upon the game's resolution
        wall_width = width/Wall.divisor
        wall_length = length/Wall.divisor

        for i in range(Wall.divisor):
            for j in range(Wall.divisor):
                    # Generates Wall divisor ^ 2 walls  
                    x = i*(wall_width)
                    y = j*(wall_length)

                    # Check to see if the current selected wall area is going to be a wall or a safe area
                    if (random.randint(0, upper-1) == 0):
                        Wall(x,y,wall_width,wall_length)
                    else:
                        # This finds the center of the area that the wall would have spawned in 
                        # and adds those co-ords into a list of safe areas for the players to spawn in.
                        # It does this by taking the 2 corner co-ords and dividing them by 2 to get the center
                        Wall.no_wall_area.append(((x+(x+wall_width))/2,((y+(y+wall_length))/2)))

        # Send it back to the main game for spawning players in  
                
    # This deletes a random wall from the game until there are no walls left
    def delete(clock_cycle):
        # If there are walls left
        if (len(Wall.walls) > 0):
            # If enough time has passed for a wall to go
            if ((clock_cycle % Wall.lifetime) == 0):
                # Pick a random wall and get rid of it
                del Wall.walls[random.randint(0,len(Wall.walls)-1)]

    # Draws the wall out
    def draw(self,window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, self.width, self.length))
                