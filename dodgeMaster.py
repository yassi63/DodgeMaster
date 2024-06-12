import pygame 
import time 
import random
import os
player_height=35
player_width=35
spd=5
star_width=20
star_height=20
star_spd=5
pygame.font.init()
FONT=pygame.font.SysFont("comicsans",30)
width=600
height=600
win=pygame.display.set_mode((width,height))
bg=pygame.transform.scale(pygame.image.load("backgrounds/spacebg.webp"),(width,height))
pygame.display.set_caption("dodgeMaster")
border_thickness=2
record_file="record.txt"
if os.path.exists(record_file):
    with open(record_file,"r") as file:
        record=float(file.read())
else:
    record=0
def draw(FONT,elapsed_time,stars,record): 
    win.blit(bg,(0,0))
    timetxt=FONT.render(F"time: {round(elapsed_time)}s",1,"white")
    win.blit(timetxt,(10,10))
    pygame.draw.line(win,"white",(0,500),(600,500),2)
    pygame.draw.rect(win,"white",player)
    pygame.draw.rect(win,"black",inner_player)
    for star in stars:
        pygame.draw.rect(win,"yellow",star)
    recordtxt=FONT.render(F"record: {round(record)}s",1,"white")
    win.blit(recordtxt,(width-recordtxt.get_width()-10,10))
    pausetxt=FONT.render("press p to pause",1,"royalblue4")
    win.blit(pausetxt,(300-pausetxt.get_width()/2,560-pausetxt.get_height()/2))
    pygame.display.update()
playagain_width=175 
playagain_height=50
quitt_width=175
quitt_height=50
def endscreen():
    global playagain_width,playagain_height,quitt_width,quitt_height,play_again,quitt
    win.blit(bg,(0,0))
    play_again=pygame.Rect(width/2-playagain_width/2,height/2-playagain_height/2,playagain_width,playagain_height)
    quitt=pygame.Rect(width/2-quitt_width/2,height/2-quitt_height/2+60,quitt_width,quitt_height)
    playagain_txt=FONT.render("play again",1,"white")
    quit_txt=FONT.render("Quit",1,"White")
    pygame.draw.rect(win,"green",play_again)
    pygame.draw.rect(win,"red",quitt)
    overtxt=FONT.render("game over ! ",1,"white")
    win.blit(overtxt,(width/2-overtxt.get_width()/2,height/2-overtxt.get_height()/2-80))
    win.blit(playagain_txt,(play_again.x+playagain_width/2-playagain_txt.get_width()/2,height/2-playagain_height/2))
    win.blit(quit_txt,(quitt.x+quitt_width/2-quit_txt.get_width()/2,height/2-quitt_height/2+60))
    pygame.display.update()
def main():
    global run,hit,paused,pausedtxt,start_time,paused_start_time,star_count,elapsed_time,star_add_increment,stars,record,player,inner_player
    run=True
    hit=False
    paused=False
    player=pygame.Rect(width/2-player_width/2,500-player_height,player_width,player_height)
    inner_player=player.inflate(-2*border_thickness,-2*border_thickness)
    start_time=time.time()
    elapsed_time=0
    star_count=0
    star_add_increment=2000
    stars=[]
    while run:
        if paused:
            pausedtxt=FONT.render("game paused",1,"white")
            win.blit(pausedtxt,(width/2-pausedtxt.get_width()/2,height/2-pausedtxt.get_height()/2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                    run=False
                    break
                if event.type==pygame.KEYDOWN and event.key==pygame.K_p:
                    paused=False
                    start_time+=time.time()-paused_start_time
        else:
            draw(FONT,elapsed_time,stars,record)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                    break
                if event.type==pygame.KEYDOWN and event.key==pygame.K_p:
                    paused=True
                    paused_start_time=time.time()
        
            star_count+=pygame.time.Clock().tick(60)
            elapsed_time=time.time()-start_time
            if(star_count>star_add_increment):
                for _ in range(3):
                    star=pygame.Rect(random.randint(0,width-star_width),-(star_height),star_width,star_height)
                    stars.append(star)
                star_add_increment=max(200,star_add_increment-50)
                star_count=0
            for star in stars[:]:
                star.y+=star_spd
                if(star.y>500-star_height):
                    stars.remove(star)
                if(star.colliderect(player)) and (star.colliderect(inner_player)):
                    hit=True
            if hit:
                endscreen()
                choice=True
                while choice:
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            run=False
                            choice=False
                        if  (event.type==pygame.KEYDOWN and (event.key==pygame.K_RETURN)):
                            main()
                            choice=False
                        if (event.type==pygame.KEYDOWN and (event.key==pygame.K_ESCAPE)):
                            run=False
                            choice=False
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            mouse=event.pos
                            if play_again.collidepoint(mouse):
                                main()
                                choice=False
                            if quitt.collidepoint(mouse):
                                run=False
                                choice=False
                        
                break          
            keys=pygame.key.get_pressed()
            if (keys[pygame.K_RIGHT]) and (player.x<(width-player_width)) and (inner_player.x<(width-player_width)):
                player.x+=spd
                inner_player.x+=spd
            if (keys[pygame.K_LEFT]) and (player.x>0) and (inner_player.x>0):
                player.x-=spd
                inner_player.x-=spd
            if (keys[pygame.K_ESCAPE]):
                run=False
    if(elapsed_time>record):
        record=elapsed_time
        with open(record_file,"w") as file:
            file.write(str(record))
    pygame.quit()
main()
