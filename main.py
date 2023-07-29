# Program     : Tank Game
# Name        : Georgios Dialynas-Vatsis
# Date        : June 16, 2022
# Description : Starts up the tank game, made for the CS Grade 12 culmanating
import pygame
from player import *
from scene import *
from wall import *
import os

# Pygame setup
pygame.init()
pygame.display.set_caption('Tanks!')
clock = pygame.time.Clock()


# Sets controls
player1_movement = [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d]
player2_movement = [pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT]
player3_movement = [pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l]

player1_aim = [pygame.K_e,pygame.K_q]
player2_aim = [pygame.K_COMMA,pygame.K_PERIOD]
player3_aim = [pygame.K_o,pygame.K_u]

player1_shoot = pygame.K_SPACE
player2_shoot = pygame.K_SLASH
player3_shoot = pygame.K_RETURN

# Sets their colors
player1_color = (255, 0, 0)
player2_color = (0, 0, 255)
player3_color = (0, 255, 0)

# Creates the players, you can add an infite amount of players if you want to
player1 = Player(player1_movement,player1_shoot,player1_aim,player1_color)
player2 = Player(player2_movement,player2_shoot,player2_aim,player2_color)
player3 = Player(player3_movement,player3_shoot,player3_aim,player3_color)


# How many ticks per second
tickrate = 60
# Please keep this at 0, this is used for bullet lifetime counts
clock_cycle = 0

scene_manager = Scene(0)

# Sets up the music and sets the volume to zero
song =  os.getcwd() + "/Sound/music_loop.wav"

# Begins the mixer and loads the song
pygame.mixer.init()
pygame.mixer.music.load(song)

# Sets the song to repeat
pygame.mixer.music.play(loops=-1)

# Minimize the volume so the intro can play
pygame.mixer.music.set_volume(0)

# Gameloop
run = True
while (run):

    # Keeps an int of how long since the game was booted.
    # This will eventually break the code in 4,874,520,144.63 years, so if you think that needs a check, I hope you have time to wait for it to error out.
    clock_cycle += 1
    clock.tick(tickrate)
    
    # Basic pygame window handling
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False

    # Start the first scene up
    scene_manager.clock_cycle = clock_cycle
    scene_manager.run()
    
    # refresh screen
    pygame.display.flip()

pygame.quit()
exit()