import pygame
import sys 

#intialize pygame
pygame.init()

# set screen
screen = pygame.display.set_mode((800, 480))

# sond effects for the game
piece_up = pygame.mixer.Sound("piece_up.wav")
piece_down = pygame.mixer.Sound("piece_down.wav")
success = pygame.mixer.Sound("success.wav")

# Title and Icon for the game window.
pygame.display.set_caption("Tower of Hanoi")
window_icon = pygame.image.load("icon.png")
pygame.display.set_icon(window_icon)

# colors
black = (0,0,0)
red = (255,0,0)
green = (0,106,78)
blue = (0,127,255)
light_blue = (153,204,255)
on_btn_blue = (92,151,203)
off_btn_blue = (59,126,185)
on_btn_green = (112,166,53)
off_btn_green = (99,146,47)
btn_grey = (55,71,82)
grey = (165, 165, 165)
gold = (197,131,73)

# Class to describe each tower and the available positions on that tower
class Towers:
    def __init__(self):
        self.base_of_pole = []
        self.hitbox = []
        self.drawn_pos = []

        # Holds which locations of each tower is occupied.
        self.positions =[
                        {0:None,1:None,2:None,3:None,4:None,5:None,6:None,7:None},
                        {0:None,1:None,2:None,3:None,4:None,5:None,6:None,7:None},
                        {0:None,1:None,2:None,3:None,4:None,5:None,6:None,7:None}
                        ]                 

    def make_towers(self,screen):
        temp_dict = {}

        for xpos in range(50, 590+1, 270):
            base = pygame.Rect(xpos, 400, 160 , 20)
            pole = pygame.Rect(xpos+75, 190, 10, 210)
            self.base_of_pole.append((base,pole))

            self.hitbox.append(pygame.Rect(xpos+15, 190, 130, 210))   

            self.drawn_pos.append([pygame.Rect(xpos, ypos, 160 , 20) for ypos in range(200,375+1,25)])

# Class to describe all game disks 
class Disks:
    def __init__(self):
        self.disk_dict = {}
        self.disk_count = 3
        self.total_moves = 0

    def create_disks(self, num_of_disks, disk_dict):
        count = 7
        width = 111 

        for disk in range(num_of_disks,0,-1):
            temp = pygame.Rect(50, 50, width, 20)

            disk_dict.update({disk:temp})
            width -= 9
            count -= 1

def disk_start_pos(tower_pos, disk_dict, positions):
    current_pos = 7

    for num in range(len(disk_dict),0,-1):
        positions[0][current_pos] = num
        disk_dict[num].center = tower_pos[0][current_pos].center
        current_pos -= 1 

# Describes values that are needed to start the game.  
# Count is updated with the number of disks set by the player.
class Start:
    def __init__(self):
        self.running = True
        self.count = 3

# Class that describes the current moving disk values. 
# This class is used for moves that occur after the first move. 
class Current_Disk:
    def __init__(self):
        self.valid_place = False # Stores if the moving disk can be placed to moved location 
        self.idx_of_hb = 0 # Index on the tower the disk is moving to.
        self.new_tower_pos = 0 # The tower the disk is moved to.

# Class that describes the first move of the game 
# and is updated with values of the subsequent valid move.
class Previous_Disk:
    def __init__(self):
        self.valid_move = False # Stores if the clicked disk is able to be moved
        self.tower_hitbox = 0 # The tower the clicked disk came from.
        self.og_tower_pos = 0 # Position on the tower the clicked disk was moved from.
        self.disk_number = None # The number of the disk 

# validates player click to determine if a disk is moveable.
# If it is the previous_disk object is updated with disk information.
# previous_disk is object to hold disk info, hitbox is tower hitbox, positions is tower positions,
# disk_dict is the dictionary of all game disks, and cursor is user cursor.
def click_validator(previous_disk, hitbox, positions, disk_dict, cursor):
    for hb in hitbox:
        if hb.collidepoint(cursor):
            previous_disk.tower_hitbox = hitbox.index(hb)
            for disk in disk_dict: 
                if disk_dict[disk].collidepoint(cursor):
                    for pos in range(8):
                        if pos > 0:
                            if positions[previous_disk.tower_hitbox][pos] == disk and positions[previous_disk.tower_hitbox][pos-1] == None:
                                previous_disk.valid_move = True
                                previous_disk.og_tower_pos = pos
                                previous_disk.disk_number = disk
                                break
                        elif positions[previous_disk.tower_hitbox][pos] == disk:
                            previous_disk.valid_move = True
                            previous_disk.og_tower_pos = pos
                            previous_disk.disk_number = disk
                            break
            break        

# Validates if the place on screen is a valid placement. 
# If it is the current_disk object is updated with that placement information. 
def placement_validator(current_disk, new_towers, new_disks, og_tower_hitbox, disk):
    hitbox = new_towers.hitbox
    positions = new_towers.positions
    dict = new_disks.disk_dict

    for hb in hitbox:
        if hb.colliderect(dict[disk]) and hb != og_tower_hitbox:
            current_disk.idx_of_hb = hitbox.index(hb)
            for pos in range(7,-1,-1):
                if pos == 0 and positions[current_disk.idx_of_hb][pos] == None:
                    if positions[current_disk.idx_of_hb][pos+1] > disk:
                        current_disk.new_tower_pos = pos
                        current_disk.valid_place = True 
                else:
                    if positions[current_disk.idx_of_hb][pos] == None and positions[current_disk.idx_of_hb][pos-1] == None:
                        if pos < 7:
                            if positions[current_disk.idx_of_hb][pos+1] > disk:
                                current_disk.new_tower_pos = pos
                                current_disk.valid_place = True
                                break
                            else:
                                break
                        else:
                            current_disk.new_tower_pos = pos
                            current_disk.valid_place = True
                            break

def start_menu(new_start):
    launch_game = False
    launch_on_up = False

    while not launch_game:  
        cursor = pygame.mouse.get_pos()
        screen.fill(light_blue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launch_game = True
                new_start.running = False
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 200+100 > cursor[0] > 200 and 210+100 > cursor[1] > 210:
                    new_start.count -= 1
                    if new_start.count < 1: 
                        new_start.count = 1   
                elif 500+100 > cursor[0] > 500 and 210+100 > cursor[1] > 210:
                    new_start.count += 1
                    if new_start.count > 8:
                        new_start.count = 8
                elif 300+200 > cursor[0] > 300 and 380+50 > cursor[1] > 380:
                    launch_on_up = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if launch_on_up:    
                    launch_game = True

        if 200+100 > cursor[0] > 200 and 210+100 > cursor[1] > 210:
            pygame.draw.rect(screen, on_btn_blue, (200,210,100,100))
        else:
            pygame.draw.rect(screen, off_btn_blue, (200,210,100,100))

        if 500+100 > cursor[0] > 500 and 210+100 > cursor[1] > 210:
            pygame.draw.rect(screen, on_btn_blue, (500,210,100,100))
        else:
            pygame.draw.rect(screen, off_btn_blue, (500,210,100,100))

        if 300+200 > cursor[0] > 300 and 380+50 > cursor[1] > 380:
            pygame.draw.rect(screen, on_btn_green, (300,380,200,50))
        else:
            pygame.draw.rect(screen, off_btn_green, (300,380,200,50))  
        
        blit_text(screen, "Tower of Hanoi", (400,50), font_name='sans serif', size=90, color=gold)
        blit_text(screen, 'Click " + " to increase number of disks and " - " to decrease:', (400, 140), font_name='sans serif', size=30, color=black)
        blit_text(screen, str(new_start.count), (400, 240), font_name='sans serif', size=70, color=blue)
        blit_text(screen, 'Play', (400, 398), font_name='sans_serif', size=30, color=black)  
        pygame.draw.rect(screen, btn_grey, (515,253,70,15)) 
        pygame.draw.rect(screen, btn_grey, (543,225,15,70))
        pygame.draw.rect(screen, btn_grey, (215,253,70,15))

        pygame.display.update()

def game_over(num_of_disks,moves):
    screen.fill(light_blue)
    still_end = True
    play_again = False
    min_moves = 2**num_of_disks-1 
    while still_end:
        cursor = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 300+200 > cursor[0] > 300 and 380+50 > cursor[1] > 380:
                    play_again = True

            elif event.type == pygame.MOUSEBUTTONUP:
                    if play_again:  
                        pygame.mixer.stop()
                        return True 
                        

        blit_text(screen, 'You Won!', (400,60), font_name='sans serif', size=90, color=gold)
        blit_text(screen, f'Your Moves: {moves}', (415, 250), font_name='mono', size=30, color=black)
        blit_text(screen, f'Minimum Moves: {min_moves}', (410, 310), font_name='mono', size=30, color=red)
        
        # play again button
        if 300+200 > cursor[0] > 300 and 380+50 > cursor[1] > 380:
            pygame.draw.rect(screen, on_btn_green, (300,380,200,50))
        else:
            pygame.draw.rect(screen, off_btn_green, (300,380,200,50))

        blit_text(screen, 'Play Again?', (400, 398), font_name='sans_serif', size=30, color=black)

        if min_moves==moves:
            blit_text(screen, 'You finished in the least amount of moves!', (400, 160), font_name='mono', size=26, color=green)
        
        pygame.display.update()

def blit_text(screen, text, midtop, font_name, size, color):                                  
    font = pygame.font.SysFont(font_name, size)     
    font_surface = font.render(text, True, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)    

# start of game
def game_play():
    moving = False
    restart = False 

    # creates game objects.
    new_towers = Towers()
    new_disks = Disks()
    new_start = Start()
    current_disk = Current_Disk()
    previous_disk = Previous_Disk()

    start_menu(new_start) 

    new_disks.disk_count = new_start.count 

    new_towers.make_towers(screen)
    new_disks.create_disks(new_disks.disk_count, new_disks.disk_dict)
    disk_start_pos(new_towers.drawn_pos, new_disks.disk_dict, new_towers.positions)

    # game_loop
    while new_start.running:
        cursor = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                new_start.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor = pygame.mouse.get_pos()
                click_validator(previous_disk, new_towers.hitbox, new_towers.positions, new_disks.disk_dict, cursor)
                if previous_disk.valid_move:
                    moving_rect = new_disks.disk_dict[previous_disk.disk_number]
                    new_towers.positions[previous_disk.tower_hitbox][previous_disk.og_tower_pos] = None
                    if moving_rect.collidepoint(event.pos):
                        pygame.mixer.Sound.play(piece_up)
                        moving = True
                # restart check          
                if 10+150 > cursor[0] > 10 and 440+30 > cursor[1] > 440:
                    restart = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if previous_disk.valid_move:
                    placement_validator(current_disk, new_towers, new_disks, previous_disk.og_tower_pos, previous_disk.disk_number)
                    if current_disk.valid_place: 
                        moving_rect.center = new_towers.drawn_pos[current_disk.idx_of_hb][current_disk.new_tower_pos].center
                        new_towers.positions[current_disk.idx_of_hb][current_disk.new_tower_pos] = previous_disk.disk_number
                        if previous_disk.tower_hitbox != current_disk.idx_of_hb:
                            new_disks.total_moves+=1
                    else:
                        moving_rect.center = new_towers.drawn_pos[previous_disk.tower_hitbox][previous_disk.og_tower_pos].center
                        new_towers.positions[previous_disk.tower_hitbox][previous_disk.og_tower_pos] = previous_disk.disk_number
                    moving_rect = None
                    previous_disk.valid_move = False
                    current_disk.valid_place = False
                    pygame.mixer.Sound.play(piece_down)       
                    moving = False
                # restart check 
                if restart:    
                    return [100, 0]

            elif event.type == pygame.MOUSEMOTION and moving:
                moving_rect.move_ip(event.rel)

        screen.fill(light_blue)
        
        blit_text(screen, "To win: move all disk to the right most tower, in ascending order.", (400,20), font_name='sans serif', size=30, color=black)

        # draws towers
        for tower in new_towers.base_of_pole:
            pygame.draw.rect(screen, green, tower[0])
            pygame.draw.rect(screen, grey, tower[1])

        # draws disks
        for disk in range(new_disks.disk_count,0,-1):
            pygame.draw.rect(screen, blue, new_disks.disk_dict[disk])

        # restart game button
        if 10+100 > cursor[0] > 10 and 440+30 > cursor[1] > 440:
            pygame.draw.rect(screen, on_btn_green, (10,440,100,30))
        else:
            pygame.draw.rect(screen, off_btn_green, (10,440,100,30))

        blit_text(screen, 'Restart', (60, 447), font_name='sans_serif', size=30, color=black)

        blit_text(screen, f"Moves: {new_disks.total_moves}", (700, 65), font_name='mono', size=30, color=black)

        # end of game check returns list containing number of disks and total player moves to main.
        if new_towers.positions[2][8-new_disks.disk_count] != None:
            pygame.mixer.Sound.play(success)
            new_start.running = False
            return [new_disks.disk_count, new_disks.total_moves]
            #new_start.running = game_over(new_disks.disk_count,new_disks.total_moves)

        pygame.display.update()   

# main calls game loop and game over and checks if the player wants to continue playing.
def main(): 
    play = True
    while play:
        game_results = game_play()
        try:
            if game_results[0] == 100: # used when restart button is pressed during game
                pass
            else:    
                play = game_over(game_results[0],game_results[1])
        except:
            play = False

main()
pygame.quit() # quits game for good     
