# Program     : Player Class
# Name        : Georgios Dialynas-Vatsis
# Date        : June 16, 2022
# Description : Manages player movement, spawn, collision, and shooting
import pygame
import math
from bullet import *

class Player:
    players = []
    living_players = []
    def __init__(self,movement,shoot,aim,color):
        Player.players.append(self)

        # Set Movement Controls
        self.up = movement[0]
        self.left = movement[1]
        self.down = movement[2]
        self.right = movement[3]

        # Set aim and shoot controls
        self.aim_right = aim[0]
        self.aim_left = aim[1]
        self.shoot = shoot
    
        # Set Players velocity
        self.velocity = 3

        # Set starting position
        self.x = 10 
        self.y = 10

        # Set default angle and turn speed 
        self.angle = 0 
        self.aim_speed = 4

        # Set Size for player sprites
        self.radius = 20        
        self.cannon_length = 50
        self.cannon_width = 10

        # Set sprite color
        self.color = color

        # Set how often a bullet can fire (in frames)
        self.shot_delay = 10

        # Set beginning delay (negative shot delay lets players fire immediately)
        self.last_shot = -self.shot_delay

        self.score = 0
    
    def check_movement(self,keys,window):
            # Basic Movement controls
            self.x += self.velocity * (keys[self.right] - keys[self.left])
            self.y += self.velocity * (keys[self.down] - keys[self.up])

            # Basic Aim controls
            self.angle += self.aim_speed * (keys[self.aim_left] - keys[self.aim_right]) 

            # Make sure that angle is between 0 and 359 for consistancy.
            if (self.angle < 0):
                self.angle += 360 
            elif (self.angle > 360):
                self.angle %= 360

            # Create Wrapping Effect
            self.x = self.x % window.get_width()
            self.y = self.y % window.get_height()

    def check_wall_collision(self):
        for wall in Wall.walls:
            # Checks each side on every wall for collision with the player
            if(self.x > (wall.x - self.radius) and self.x < (wall.x + wall.width + self.radius) and self.y >  (wall.y - self.radius) and self.y < wall.y + wall.length + self.radius):
                return True
        return False

    def check_bullet_collision(self):
        bullet_index = 0
        # Check every bullet against the player for collision
        while (bullet_index < len(Bullet.bullets)):

            # Calculate the distance between the two points
            distance = (Bullet.bullets[bullet_index].x - self.x) ** 2 + (Bullet.bullets[bullet_index].y - self.y) ** 2;
            
            # Adds up the radius'
            radius = (Bullet.bullets[bullet_index].radius + self.radius) ** 2;

            # Collision
            if (distance <= radius):
                # Play the death sound effect
                bonk_sound = pygame.mixer.Sound("Sound/bonk.wav")
                bonk_sound.play()

                del Player.living_players[Player.living_players.index(self)]
                # delete the bullet
                del Bullet.bullets[bullet_index]
            else:
                # move onto the next bullet
                bullet_index += 1 
    

    def check_shot(self,keys,clock_cycle):
        if (keys[self.shoot]):
            # If enough time has past since last shot, shoot
            if (self.last_shot + self.shot_delay < clock_cycle):
                self.last_shot = clock_cycle

                # Save the current bullet for checks
                spawned_bullet = Bullet(self.cannon_end_x,self.cannon_end_y,self.angle,self.color,clock_cycle)

                # If the bullet was spawned in a wall, delete it.
                if (spawned_bullet.check_if_center_is_in_a_wall()):
                    del Bullet.bullets[Bullet.bullets.index(spawned_bullet)]
                # If the bullet was immediatly spawned inside a will kill it
         
    def draw(self,window):
        # pygame.draw.rect(window,self.color,)
        # Calculate where the cannon ends
        rad_angle = self.angle * math.pi / 180
        self.cannon_end_x =  (self.x + (self.cannon_length * math.cos(rad_angle)))
        self.cannon_end_y =  (self.y + -(self.cannon_length * math.sin(rad_angle)))
        
        # Draw Player body
        pygame.draw.circle(window,self.color,(self.x, self.y),self.radius)

        # Draw cannon & cannon head
        # pygame.draw.ciarcle(window,self.color,(self.cannon_end_x, self.cannon_end_y),self.cannon_width)
        pygame.draw.line(window,self.color,(self.x, self.y), (self.cannon_end_x, self.cannon_end_y),self.cannon_width)

    