import sys, pygame
from time import time,sleep
import subprocess
import winsound
from math import floor
import wave
accompaniment=0

def shrutiname(n):
        octave,just= (int(floor(n/22)),[(1,1),(256,243),(16,15),(10,9),(9,8),(32,27),(6,5),(5,4),(81,64),(4,3),(27,20),(45,32),(729,512),(3,2),(128,81),(8,5),(5,3),(27,16),(16,9),(9,5),(15,8),(243,128)][wrap(n,22)])
        if octave<0:
                just=just[0],just[1]*2**abs(octave)
        if octave>0:
                just=just[0]*2**abs(octave),just[1]
    
        return "%s_%s.wav"%(just[0],just[1])

def wrap(a,b):
        if a<0:
                return wrap(a+b,b)
        if a>=b:
                return wrap(a-b,b)
        else:
                return a
def inimixer():
    return pygame.mixer.pre_init(frequency=44100, size=-16, channels=8, buffer=512)
channels=[0,0,0,0,0,0,0,0]
mixer=inimixer()
pygame.init()
Pluck_Sounds=[pygame.mixer.Sound(shrutiname(i) )for i in range(-22,23)]
 
def shruti(n):
	return 261.6256*2**(int(floor(n/22)))*[1,256/243,16/15,10/9,9/8,32/27,6/5,5/4,81/64,4/3,27/20,45/32,729/512,3/2,128/81,8/5,5/3,27/16,16/9,9/5,15/8,243/128][wrap(n,22)]
 
def firstfreechannel():
    t=time()
    for i in range(1,8):
        if channels[i]<t:
            return i
    return 1
 
def bpmadjust(keys):
    global bpm,secondsperbeat
    if keys[pygame.K_LEFT]:
        bpm-=5
        secondsperbeat=60.0/bpm
        print( "set bpm: %s"%bpm)
    if keys[pygame.K_RIGHT]:
        bpm+=5
        secondsperbeat=60.0/bpm
        print ("set bpm: %s"%bpm)


def playnote(n):
    name=shrutiname(n)
    channel=firstfreechannel()
    playsoundbuff(Pluck_Sounds[n+21],channel)
    #winsound.PlaySound(name,winsound.SND_ASYNC)

 
def playsoundbuff(rawdata,channel):
        beep = pygame.mixer.Sound(buffer=rawdata)
        channels[channel]=time()+1
        pygame.mixer.Channel(channel).play(beep)
 
def playbeatsound():
        if accompaniment==2:
                playsoundbuff(kick)
def nextbeattime(time):
    return (nextbeat-time)/secondsperbeat
keylookup={pygame.K_1:12,pygame.K_2:13,pygame.K_3:14,pygame.K_4:15,pygame.K_5:16,pygame.K_6:17,pygame.K_7:18,pygame.K_8:19,pygame.K_9:20,pygame.K_0:21,pygame.K_MINUS:22,pygame.K_EQUALS:23,
    pygame.K_q:0,pygame.K_w:1,pygame.K_e:2,pygame.K_r:3,pygame.K_t:4,pygame.K_y:5,pygame.K_u:6,pygame.K_i:7,pygame.K_o:8,pygame.K_p:9,pygame.K_LEFTBRACKET:10,pygame.K_RIGHTBRACKET:11,
           pygame.K_a:-12,pygame.K_s:-11,pygame.K_d:-10,pygame.K_f:-9,pygame.K_g:-8,pygame.K_h:-7,pygame.K_j:-6,pygame.K_k:-5,pygame.K_l:-4,pygame.K_SEMICOLON:-3,pygame.K_QUOTE:-2,pygame.K_BACKSLASH:-1,
           pygame.K_z:-22,pygame.K_x:-21,pygame.K_c:-20,pygame.K_v:-19,pygame.K_b:-18,pygame.K_n:-17,pygame.K_m:-16,pygame.K_COMMA:-15,pygame.K_PERIOD:-14,pygame.K_SLASH:-13}


notes={}
for i in keylookup:
    notes[i]=0
def playsounds(keys):
    for i in keylookup:
        if keys[i]:
            playnote(keylookup[i])
def drawbeats(screen):
    bps=bpm/60;t=time();nbt=nextbeattime(t)
    pygame.draw.line(screen, (255,255,255), (nbt*80,0), (nbt*80,240), 3)
    pygame.draw.line(screen, (255,255,255), (nbt*80+80,0), (nbt*80+80,240), 3)
    pygame.draw.line(screen, (255,255,255), (nbt*80+160,0), (nbt*80+160,240), 3)
    pygame.draw.line(screen, (255,255,255), (nbt*80+240,0), (nbt*80+240,240), 3)


size = width, height = 320, 240
bpm=65
secondsperbeat=60/bpm
black = 0, 0, 0
cl=pygame.time.Clock()
screen = pygame.display.set_mode(size)
starttime=time()
lastbeat=starttime
nextbeat=lastbeat+secondsperbeat
lastrefresh=0
#if accompaniment==1:
#        playnote(shruti(-22),pygame.K_q,100,'-30dB',False)
while 1:
    t=time()
    if t>nextbeat:
        lastbeat=nextbeat
        nextbeat=lastbeat+secondsperbeat
    events=pygame.event.get()
    for event in events:
            if event.type == pygame.KEYDOWN:
                    if event.key in keylookup:
                            playnote(keylookup[event.key])
    if lastrefresh+1/30<t:
        screen.fill(black)
        drawbeats(screen)
        pygame.display.flip()
    pygame.event.pump()
#playnote(440,0)
