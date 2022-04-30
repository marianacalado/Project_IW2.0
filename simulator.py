#Differential drive robot simulation
#keyboard: https://www.pygame.org/docs/ref/key.html

import pygame
import math

class Envir:
    def __init__(self,dimentions): #método com os codigos das cores e outros parametros descritos 
        # colors  
        self.black = (0,0,0)
        self.white = (255, 255, 255)
        self.green = (0,255,0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)
        #map_dims
        self.height = dimentions[0]
        self.width = dimentions[1]
        #window settings
        pygame.display.set_caption("interface_window")
        self.screen = pygame.display.set_mode((self.width, self.height))#largura e altura do ecra
        #trail
        self.trail_set=[]

    def trail(self, pos): #método para aparecer um caminho 
        for i in range(0,len(self.trail_set)-1):
            pygame.draw.line(self.screen,self.yel,(self.trail_set[i][0],self.trail_set[i][1]),
                                (self.trail_set[i+1][0], self.trail_set[i+1][1]))

        if self.trail_set.__sizeof__()>10000:   
            self.trail_set.pop(0)
        self.trail_set.append(pos)

    def robot_frame(self,pos,rotation): #referencial que aparece no robo usando uma formula 
        n=80

        centerx, centery = pos
        x_axis=(centerx + n*math.cos(-rotation),centery + n*math.sin(-rotation))
        y_axis=(centerx + n*math.cos(-rotation+math.pi/2),centery + n*math.sin(-rotation+math.pi/2))
        pygame.draw.line(self.screen,self.red,(centerx, centery), x_axis,3)
        pygame.draw.line(self.screen,self.red,(centerx, centery), y_axis,3)


class Robot:
    def __init__(self, startpos, robotImg, width):
        self.m2p=3779.52 #meter 2 pixels
        #robot_dims
        self.w=width
        self.x=startpos[0]
        self.y=startpos[1]
        self.theta=0
        self.vl=0.01*self.m2p #meter/s
        self.vr=0.01*self.m2p 
        self.maxspeed=0.02*self.m2p 
        self.minspeed=-0.02*self.m2p 
        #graphics
        self.img = pygame.image.load(robotImg)
        self.rotated=self.img
        self.rect= self.rotated.get_rect(center=(self.x,self.y))

    def draw (self, screen): #metodo para colocar robo 
        screen.blit(self.rotated,self.rect)

    def move(self,event=None): #metodo de movimento do robo 
        if event is not None: #se estiver a acontecer um evento verificar se há alguma key do teclado a ser clicada
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: #se a tecla 1 for precionada aumenta a velocidade da roda esquerda,roda para a direita 
                    self.vl += 0.001*self.m2p 
                # elif event.key == pygame.K_2:
                #     self.vl -= 0.001*self.m2p #se a tecla 2 for precionada diminui a velocidade da roda esquerda 
                elif event.key == pygame.K_a:
                    self.vr += 0.001*self.m2p #aum velocidade roda direita logo vira para a esquerda
                # elif event.key == pygame.K_4: 
                #     self.vr -= 0.001*self.m2p  
                elif event.key == pygame.K_r: #robo pára
                    self.vl = 0*self.m2p 
                    self.vr = 0*self.m2p 
                elif event.key == pygame.K_t: #robo continua a andar 
                    self.vl = 0.01*self.m2p 
                    self.vr = 0.01*self.m2p 
                elif event.key == pygame.K_o: #robo aumenta a velocidade para o local que está 
                    self.vl += 0.003*self.m2p 
                    self.vr += 0.003*self.m2p 
                elif event.key == pygame.K_BACKSPACE: #robo anda para trás 
                    self.vl -= 0.02*self.m2p 
                    self.vr -= 0.02*self.m2p 
                # elif event.key == pygame.K_g: #robo anda para trás + esq
                #     self.vl -= 0.01*self.m2p 
                #     self.vr -= 0.001*self.m2p #aum velocidade roda direita logo vira para a esquerda


        self.x+=((self.vl+self.vr)/2)*math.cos(self.theta)*dt #formula da orientação de robot, x axis
        self.y-=((self.vl+self.vr)/2)*math.sin(self.theta)*dt #y axis
        self.theta+=(self.vr-self.vl)/self.w*dt #quanto maior o comprimento do robo mais wider será a turn

        self.rotated=pygame.transform.rotozoom(self.img, math.degrees(self.theta),1)
        self.rect=self.rotated.get_rect(center=(self.x,self.y))



#initialize pygame comands
pygame.init()

#start position 
start = (200, 200)

#dimenstions 
dims = (600, 1200)

#running or not
running = True 

#the enviromenat
environment = Envir(dims)

#the robot
robot= Robot(start, r"C:\Users\maria\OneDrive\Documentos\UNIVERSIDADE\MESTRADO\1º ANO_MEB\2ºsemestre\PTL\tetst\robotImg.png"
             ,0.01*3779.52)

#dtime
dt = 0
lasttime = pygame.time.get_ticks()

#simulation loop
while running:
    for event in pygame.event.get():#enquNTO run get evento do pygame
        if event.type == pygame.QUIT: #se o tipo é quit entao run false
            running= False 
        robot.move(event) #se nao ele move (metodo de mover)

    dt=(pygame.time.get_ticks()-lasttime)/1000 #calculo do tempo
    lasttime=pygame.time.get_ticks()
    pygame.display.update() #update
    environment.screen.fill(environment.black) #enche o ambiente de preto
    robot.move()
    #environment.write_info(int(robot.vl),int(robot.vr), robot.theta)
    robot.draw(environment.screen) #poe o desenho do robo no screen
    environment.robot_frame((robot.x,robot.y), robot.theta)
    environment.trail((robot.x,robot.y))

pygame.quit()#close window