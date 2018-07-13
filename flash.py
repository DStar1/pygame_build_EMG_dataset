# -*- coding: utf-8 -*-
import argparse
import time
import pygame
from random import randint
import random

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
done = False

parser = argparse.ArgumentParser()
parser.add_argument(
    '--csv',
    type=str,
    default='',
    help='Filename for csv file')
parser.add_argument(
    '--long_delay',
    type=str,
    default='',
    help='Flashing words delay in millis')
parser.add_argument(
    '--short_delay',
    type=str,
    default='',
    help='Write timestamp frequency in millis')
FLAGS, unparsed = parser.parse_known_args()
#print(unparsed[0], unparsed[1], unparsed[2])

def nearest_500(n):
    return round(n / 500) * 500

def nearest_50(n):
    return round(n / 50) * 50


font = pygame.font.SysFont("comicsansms", 72)

text = font.render("Hello, World", True, (0, 128, 0))

l=["yes","no","up", "down", "left", "right", "on", "off", "stop", "go"]
silence=""
# curr = randint(0,9)
ltext = random.sample(l, 1)[0]
prevWord = None
flag=0
text = font.render(l[0], True, (0, 128, 0))
last=0
ncurrent=0
nlast=0
delay=int(unparsed[1])#500
newDelay=int(unparsed[2])#50
file=str(unparsed[0])
globalStart=int(time.time() * 1000)
i = 0
keydown = None#0
while i < 5:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            i+=1
#time.sleep(10)
file = open( file ,'w')
file.write('keyPressed,wordSaid,timeStamp\n')
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
    done = True
if event.type == pygame.KEYDOWN:
    if (event.key >= 256 and event.key <= 265):
        keydown=str(event.key-256)
    elif (event.key == 256+15):
        keydown='enter'
        screen.fill((255, 255, 255))
        current=int(time.time() * 1000)-globalStart
        if (current-last>delay):
            last=current
flag=(flag+1)%2
if (flag):
    text=font.render(silence, True, (0, 128, 0))
else:
    newl = set(l)
    newl.discard(prevWord)#while 1:
    ltext =random.sample(newl, 1)[0]
    text = font.render(ltext, True, (0, 128, 0))
    prevWord = ltext

    ncurrent=nearest_50(int(time.time() * 1000)-globalStart)
    if (ncurrent-nlast>newDelay):
        nlast=ncurrent
file.write((str(keydown)) + ',' + ltext + ',' + str(int(ncurrent)) + '\n')
keydown=None

screen.blit(text,(320 - text.get_width() // 2, 240 - text.get_height() // 2))
pygame.display.flip()
clock.tick(60)
