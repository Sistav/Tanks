# Program     : Scene Class
# Name        : Georgios Dialynas-Vatsis
# Date        : June 16, 2022
# Description : Manages gameplay, titlescreen, animations, and more.

import pygame
from bullet import *
from player import *
from wall import * 

class Scene:
    def __init__(self,start_type):
        
        # set window height and width 
        self.width = 1280
        self.height = 720

        # Set colors and fonts
        self.background_color = (0,0,0)
        self.text_color = (255,255,255)
        self.fontsize = 32
        self.font = pygame.font.Font('freesansbold.ttf', self.fontsize)

        # Create the window
        self.window = pygame.display.set_mode((self.width,self.height))

        # Check the mode type
        self.mode = start_type
        self.last_mode = None
        
        # Set the delay for the intro animation in frames
        self.animation_delay =  2

        # Set the amount of frames in the intro animation
        self.max_frames = 69

    def titlescreen(self,first_time = False):
        if (first_time):
            # Set the first frame and the time it started
            self.current_frame = 1
            self.start_time = self.clock_cycle
        
        # Get the png from the file explorer and load it
        photo = f"Frames\{self.current_frame}.png"
        frame = pygame.image.load(photo)

        # Center the image on a rectangle the size of the window
        frame_rect = frame.get_rect()
        frame_rect.center = self.window.get_width() // 2, self.window.get_height() // 2

        # Place the image on the screen
        self.window.blit(frame,frame_rect)

        # Draw the frame and update the display
        pygame.draw.rect(self.window, 'BLACK', frame_rect, 1)
        pygame.display.update()
        
        # If the time has passed, set the next frame in motion
        if ((self.start_time + self.animation_delay) < self.clock_cycle):  
            if (self.current_frame < self.max_frames):
                self.current_frame += 1
                self.start_time = self.clock_cycle
        
        # Hardcoded button locations for the last frame, This lets the player click on the animations
        # Which is something that's alot cooler.
        exit_left_x = 448
        exit_top_y = 528
        exit_right_x = 815
        exit_bottom_y = 687

        play_left_x = 448
        play_top_y = 288
        play_right_x = 815
        play_bottom_y = 447

        # Check if the mouse is clicked and if we're on the last frame
        if (pygame.mouse.get_pressed()[0] and self.current_frame == self.max_frames):
            # If so, get the locations
            mouse_location = pygame.mouse.get_pos()
            # If the mouse was on the play button
            if ((mouse_location[0] > play_left_x and mouse_location[0] < play_right_x) and (mouse_location[1] > play_top_y and mouse_location[1] < play_bottom_y)):
                self.mode = 1

            # If the mouse was on the exit button
            elif ((mouse_location[0] > exit_left_x and mouse_location[0] < exit_right_x) and (mouse_location[1] > exit_top_y and mouse_location[1] < exit_bottom_y)):
                pygame.quit()
                exit()
                               
    def gameplay(self,first_time = False):
        if (first_time):

            # Clear walls and bullets
            Wall.no_wall_area = []
            Bullet.bullets = []


            # Turn up the music
            pygame.mixer.music.set_volume(1)
            
            # Respawn all players
            Player.living_players = Player.players.copy()

            # Generate new walls
            while (len(Wall.no_wall_area) < len( Player.players)):
                Wall.generate(self.window.get_width(),self.window.get_height())

            # Place the characters in random spawns
            for i in range(len(Player.living_players)):
                choice = random.randint(0,len(Wall.no_wall_area)-1)

                # set the spawn and delete that from the pool of avaliable spawns
                spawn = Wall.no_wall_area[choice]
                del Wall.no_wall_area[choice]

                # set the x and y coords
                Player.living_players[i].x = spawn[0]
                Player.living_players[i].y = spawn[1]
                Player.living_players[i].angle = random.randint(0,360)
        
        # Generate the text for the score board by getting each players score
        bottom_score_text_string = ''
        for i in range(len(Player.players)):
           bottom_score_text_string += str(Player.players[i].score)
           if (i < len(Player.players) - 1):
            bottom_score_text_string += " - "

        # create a text surface object,
        # on which text is drawn on it.
        top_score_text = self.font.render('Score:', True, self.text_color, self.background_color)
        bottom_score_text = self.font.render(bottom_score_text_string, True, self.text_color, self.background_color)

        # create a rectangular object for the
        # text surface object
        top_text_Rect = top_score_text.get_rect()
        bottom_text_Rect = bottom_score_text.get_rect()

        # set the center of the rectangular object.
        top_text_Rect.center = (self.window.get_width()//2,self.fontsize)
        bottom_text_Rect.center = (self.window.get_width()//2,self.fontsize*2)

        # Get a bool of every key pressed
        keys = pygame.key.get_pressed()
        
        # Check player movement and if a bullet was shot
        player_iterator = 0
        while (player_iterator < (len(Player.living_players))):
            # Set the last known safe position for the player to be in
            old_player_x = Player.living_players[player_iterator].x
            old_player_y = Player.living_players[player_iterator].y

            # Let the player move
            Player.living_players[player_iterator].check_movement(keys,self.window)

            # If the player was stupid enough to hit a wall
            if (Player.living_players[player_iterator].check_wall_collision()):
                # Send them back to the old co-ord
                Player.living_players[player_iterator].x = old_player_x
                Player.living_players[player_iterator].y = old_player_y

            # Check if the player shot
            Player.living_players[player_iterator].check_shot(keys,self.clock_cycle)

            # Check if the player was hit
            Player.living_players[player_iterator].check_bullet_collision()
            player_iterator += 1

        # If there is only 1 player standing, find that player in the masterlist of players and update their score.
        if (len(Player.living_players) <= 1):
            if (len(Player.living_players) == 1):
                Player.players[Player.players.index(Player.living_players[0])].score += 1
            # Starts a new round
            self.last_mode = None

        bullet_index = 0
        while (bullet_index < len(Bullet.bullets)):
            # If the bullet has expired past it's lifetime...
            if ((Bullet.bullets[bullet_index].spawn_tick + Bullet.bullets[bullet_index].lifetime) < self.clock_cycle):
                # Kill it
                del Bullet.bullets[bullet_index]
            else:
                # Move the bullet   
                Bullet.bullets[bullet_index].move(self.window)
                
                # Set the previous two co-ords  
                Bullet.bullets[bullet_index].two_turns_ago_x = Bullet.bullets[bullet_index].one_turn_ago_x
                Bullet.bullets[bullet_index].two_turns_ago_y = Bullet.bullets[bullet_index].one_turn_ago_y

                Bullet.bullets[bullet_index].one_turn_ago_x = Bullet.bullets[bullet_index].x 
                Bullet.bullets[bullet_index].one_turn_ago_y = Bullet.bullets[bullet_index].y

                # Check if a bullet collided with a wall
                collided_wall = Bullet.bullets[bullet_index].check_wall_collision()
    
                # if the bullet hit a wall
                if (collided_wall != None):
                    # Move the bullet back so it doesn't clip into the wall
                    Bullet.bullets[bullet_index].x =  Bullet.bullets[bullet_index].two_turns_ago_x
                    Bullet.bullets[bullet_index].y =  Bullet.bullets[bullet_index].two_turns_ago_y

                    # Figure out whether to bounce the bullet on the x or the y axis
                    bounce_type = Bullet.bullets[bullet_index].check_wall_collision_type(collided_wall)

                    # Bounce said bullets accordingly
                    if (bounce_type == 0):
                        Bullet.bullets[bullet_index].angle = 180 - Bullet.bullets[bullet_index].angle

                    elif (bounce_type == 1):
                        Bullet.bullets[bullet_index].angle = -Bullet.bullets[bullet_index].angle
                else:
                    # Onto the next bullet
                    bullet_index += 1 

            
        # Make the background Black
        self.window.fill(self.background_color)

        # Try to delete a wall
        Wall.delete(self.clock_cycle)
        
        # Draw out the walls
        for i in range(len(Wall.walls)):
            Wall.walls[i].draw(self.window)

        # Draw out each player's sprite 
        for i in range(len(Player.living_players)):
            Player.living_players[i].draw(self.window)
        
        # Draw out the bullets
        for i in range(len(Bullet.bullets)):
            Bullet.bullets[i].draw(self.window)

        # Show the text onscreen
        self.window.blit(top_score_text, top_text_Rect)
        self.window.blit(bottom_score_text, bottom_text_Rect)

    def run(self):
        # Check if the scene needs to be initialized
        first_time = (self.mode != self.last_mode)
        self.last_mode = self.mode 

        scenes = [self.titlescreen,self.gameplay]

        # Run the scene
        scenes[self.mode](first_time)