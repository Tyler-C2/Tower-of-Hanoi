import pygame
import sys 

#intialize pygame
pygame.init()
pygame.display.set_caption("Tower of Hanoi")

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

class Towers:
    def __init__(self):
        self.base_pole = []
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
            self.base_pole.append((base,pole))

            self.hitbox.append(pygame.Rect(xpos+15, 190, 130, 210))   

            self.drawn_pos.append([pygame.Rect(xpos, ypos, 160 , 20) for ypos in range(200,375+1,25)])

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

def disk_start_pos(tower_pos,disk_dict, positions):
    current_pos = 7

    for num in range(len(disk_dict),0,-1):
        positions[0][current_pos] = num
        disk_dict[num].center = tower_pos[0][current_pos].center
        current_pos -= 1

def click_validator(cursor):
    hitbox = new_towers.hitbox
    positions = new_towers.positions
    dict = new_disks.disk_dict
    valid = False
    t_hb = 0
    og_tower_pos = 0
    moving_disk = None

    for hb in hitbox:
        if hb.collidepoint(cursor):
            t_hb = hitbox.index(hb)
            for disk in dict: 
                if dict[disk].collidepoint(cursor):
                    for pos in range(8):
                        if pos > 0:
                            if positions[t_hb][pos] == disk and positions[t_hb][pos-1] == None:
                                valid = True
                                og_tower_pos = pos
                                moving_disk = disk
                                break
                        elif positions[t_hb][pos] == disk:
                            valid = True
                            og_tower_pos = pos
                            moving_disk = disk
                            break
            break        
    return [valid,t_hb,og_tower_pos,moving_disk]

def placement_validator(og_t_hitbox,disk):
    hitbox = new_towers.hitbox
    positions = new_towers.positions
    dict = new_disks.disk_dict
    valid = False
    idx_of_hb = 0
    new_tower_pos = 0

    for hb in hitbox:
        if hb.colliderect(dict[disk]) and hb != og_t_hitbox:
            idx_of_hb = hitbox.index(hb)
            for pos in range(7,-1,-1):
                if pos == 0 and positions[idx_of_hb][pos] == None:
                    if positions[idx_of_hb][pos+1] > disk:
                        new_tower_pos = pos
                        valid = True 
                else:
                    if positions[idx_of_hb][pos] == None and positions[idx_of_hb][pos-1] == None:
                        if pos < 7:
                            if positions[idx_of_hb][pos+1] > disk:
                                new_tower_pos = pos
                                valid = True
                                break
                            else:
                                break
                        else:
                            new_tower_pos = pos
                            valid = True
                            break
    return [valid,idx_of_hb,new_tower_pos]

def main_menu():
    global running
    count = 3
    launch_game = False
    launch_on_up = False
    increase = False
    decrease = False
    while not launch_game:  
        cursor = pygame.mouse.get_pos()
        screen.fill(light_blue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launch_game = True
                running = False
                return count
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 200+100 > cursor[0] > 200 and 210+100 > cursor[1] > 210:
                    count -= 1
                    if count < 1: 
                        count = 1   
                elif 500+100 > cursor[0] > 500 and 210+100 > cursor[1] > 210:
                    count += 1
                    if count > 8:
                        count = 8
                elif 300+200 > cursor[0] > 300 and 380+50 > cursor[1] > 380:
                    launch_on_up = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if launch_on_up:    
                    launch_game = True
                    return count

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
        blit_text(screen, str(count), (400, 240), font_name='sans serif', size=70, color=blue)
        blit_text(screen, 'Play', (400, 398), font_name='sans_serif', size=30, color=black)  
        pygame.draw.rect(screen, btn_grey, (515,253,70,15)) 
        pygame.draw.rect(screen, btn_grey, (543,225,15,70))
        pygame.draw.rect(screen, btn_grey, (215,253,70,15))

        pygame.display.update()

def game_over(num_of_disks,moves):
    screen.fill(light_blue)
    still_end = True
    min_moves = 2**num_of_disks-1 
    while still_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        blit_text(screen, 'You Won!', (400,60), font_name='sans serif', size=90, color=gold)
        blit_text(screen, f'Your Moves: {moves}', (415, 250), font_name='mono', size=30, color=black)
        blit_text(screen, f'Minimum Moves: {min_moves}', (410, 310), font_name='mono', size=30, color=red)
        
        if min_moves==moves:
            blit_text(screen, 'You finished in the least amount of moves!', (400, 160), font_name='mono', size=26, color=green)
        
        pygame.display.update()

def blit_text(screen, text, midtop, font_name, size, color):                                  
    font = pygame.font.SysFont(font_name, size)     
    font_surface = font.render(text, True, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)    

screen = pygame.display.set_mode((800, 480))
new_towers = Towers()
new_disks = Disks()

new_disks.disk_count = main_menu()

new_towers.make_towers(screen)
new_disks.create_disks(new_disks.disk_count, new_disks.disk_dict)
disk_start_pos(new_towers.drawn_pos,new_disks.disk_dict,new_towers.positions)

running = True
moving = False
# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            cursor = pygame.mouse.get_pos()
            previous_pos = click_validator(cursor)
            if previous_pos[0]:
                moving_rect = new_disks.disk_dict[previous_pos[-1]]
                new_towers.positions[previous_pos[1]][previous_pos[2]] = None
                if moving_rect.collidepoint(event.pos):
                    moving = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if previous_pos[0]:
                valid_place = placement_validator(previous_pos[2],previous_pos[3])
                if valid_place[0]: 
                    moving_rect.center = new_towers.drawn_pos[valid_place[1]][valid_place[-1]].center
                    new_towers.positions[valid_place[1]][valid_place[2]] = previous_pos[-1]
                    new_disks.total_moves+=1
                else:
                    moving_rect.center = new_towers.drawn_pos[previous_pos[1]][previous_pos[2]].center
                    new_towers.positions[previous_pos[1]][previous_pos[2]] = previous_pos[-1]
                moving_rect = None
                previous_pos[0] = False        
                moving = False

        elif event.type == pygame.MOUSEMOTION and moving:
            moving_rect.move_ip(event.rel)

    screen.fill(light_blue)
    
    blit_text(screen, "To win: move all disk to the right most tower, in ascending order.", (400,20), font_name='sans serif', size=30, color=black)

    # draws towers
    for tower in new_towers.base_pole:
        pygame.draw.rect(screen, green, tower[0])
        pygame.draw.rect(screen, grey, tower[1])

    # draws disks
    for disk in range(new_disks.disk_count,0,-1):
        pygame.draw.rect(screen, blue, new_disks.disk_dict[disk])

    blit_text(screen, f"Moves: {new_disks.total_moves}", (700, 65), font_name='mono', size=30, color=black)

    # end of game check
    if new_towers.positions[2][8-new_disks.disk_count] != None:
        running = game_over(new_disks.disk_count,new_disks.total_moves)

    pygame.display.update()    
        