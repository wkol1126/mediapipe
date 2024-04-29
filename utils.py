import pygame

def load_image(path, color_Key=(0,0,0)):
    img = pygame.image.load(path).convert()
    img.set_colorkey(color_Key)
    return img

def rect(pos, size):
    return pygame.Rect(pos[0], pos[1], size[0], size[1])