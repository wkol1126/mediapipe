import pygame as py
from pygame.locals import QUIT 
import utils
import cv2 as cv
import mediapipe as mp
from handtracking_module import handDetector
import os, sys, time

# pygame init
py.init()
Camera_SIZE = (640,480)
DISPLAY_SIZE = (1200, 700)
ration_x = DISPLAY_SIZE[0] / Camera_SIZE[0]
ration_y = DISPLAY_SIZE[1] / Camera_SIZE[1]
screen = py.display.set_mode(DISPLAY_SIZE)
display = py.Surface(DISPLAY_SIZE)

# loading imgae
finger_tip = utils.load_image('finger_tip.png', (255,255,255))
circle_open = utils.load_image('circle_open.png',(255,255,255))
circle_filled = utils.load_image('circle_filled.png',(255,255,255))
pathDIR = 'header'
headlist = os.listdir(pathDIR)
header=[]
for path in headlist:
    img = utils.load_image(pathDIR + '/' + path)
    header.append(img)
py.key.stop_text_input() # 停止偵測文字輸入
main_clock = py.time.Clock()

# mediapipe init
cap = cv.VideoCapture(0)
detector = handDetector()

#選擇列
circle_pos_o=(300,630)
circle_color_map = [(255,0,0), (0,0,255),(0,255,0),(255,255,0),(255,0,255),(0,255,255)]
circle_color = 0
circle_rect = utils.rect(circle_pos_o, circle_open.get_size())
circle_pos_f = (800, 630)
circle_fill_rect = utils.rect(circle_pos_f, circle_filled.get_size())
#parameter 
draw_circle = False
circle_sel = False
circle_fill_sel =False
fill = 0
circle_map ={}


while True:
    screen.fill((255, 255, 255))
    screen.blit(header[circle_color], (150,0))
    screen.blit(circle_open, circle_pos_o)
    screen.blit(circle_filled, circle_pos_f)
    
    for event in py.event.get():
        if event.type == QUIT:
            py.quit()
            sys.exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_1:
                print('color1')
                circle_color = 0
            elif event.key == py.K_2:
                print('color2')
                circle_color = 1
            elif event.key == py.K_3:
                print('color3')
                circle_color = 2
            elif event.key == py.K_4:
                print('color3')
                circle_color = 3
            elif event.key == py.K_5:
                print('color3')
                circle_color = 4
            elif event.key == py.K_6:
                print('color3')
                circle_color = 5    
            elif event.key == py.K_SPACE:
                draw_circle = True   
            elif event.key == py.K_x:
                circle_fill_map = {}
                circle_map = {}     
        
        if event.type == py.KEYUP:
            if event.key == py.K_SPACE:
                draw_circle = False

    
    sucess, frame = cap.read()
    frame = cv.flip(frame, 1)
    pos_x, pos_y, _dect = detector.find_finger(frame, 8)
    pos_x, pos_y = int(pos_x * ration_x), int(pos_y * ration_x)
    
    finger_rec = utils.rect((pos_x, pos_y), finger_tip.get_size())

    
    for loc in circle_map:       
        py.draw.circle(screen, circle_color_map[circle_map[loc][3]], 
                       (circle_map[loc][0], circle_map[loc][1]), circle_map[loc][2], circle_map[loc][4])
    
    
    if circle_rect.colliderect(finger_rec):
        circle_sel = True
        circle_fill_sel = False
        fill = 1
        print(fill)
        py.draw.rect(screen, (0,255,0),[circle_rect.x + circle_rect.width//-50, 
                                        circle_rect.y - circle_rect.height//2+28,
                                        circle_rect.width, circle_rect.height], 2)         
  
    if circle_fill_rect.colliderect(finger_rec):
        circle_fill_sel = True
        circle_sel = False
        fill = 0
        print(fill)
        py.draw.rect(screen, (0,255,0),[circle_fill_rect.x + circle_fill_rect.width//2-25, 
                                        circle_fill_rect.y - circle_fill_rect.height//2+28,
                                        circle_fill_rect.width, circle_fill_rect.height], 2)    
  
    if circle_sel and _dect:
        finger_dis = detector.finger_distance(4,8)        
        py.draw.circle(screen, circle_color_map[circle_color], (pos_x, pos_y), finger_dis, fill)
        if draw_circle:
            circle_map[str(pos_x) +';'+ str(pos_y)] = [pos_x, pos_y, finger_dis, circle_color,fill]

    
    if circle_fill_sel and _dect:
        finger_dis = detector.finger_distance(4,8)        
        py.draw.circle(screen, circle_color_map[circle_color], (pos_x, pos_y), finger_dis, fill)
        if draw_circle:
            circle_map[str(pos_x) +';'+ str(pos_y)] = [pos_x, pos_y, finger_dis,circle_color,fill]
    
    
    
    screen.blit(finger_tip,(pos_x, pos_y))
    
    
    # cv.imshow('camera', frame)
    # if cv.waitKey(1) & 0XFF == ord('d'):
    #     cap.release()
    #     break
    main_clock.tick(60)
    py.display.update()

    
