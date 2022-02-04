import pygame as pg
import sys
from csv import reader
import random as rn
from re import split as Split
pg.init()

W = 1920
H = 1080

display = pg.display.set_mode((0,0), pg.FULLSCREEN)

# W,H = 1500,800
# display = pg.display.set_mode((W,H))

pg.display.set_caption(' ')

black = (0,0,0)
white = (255,255,255)
red = (158,27,50)
grey = (130,138,143)
blue = (0,150,255)
lred = (255,50,0)
magenta = (255,0,255)

Courses = list(reader(open('UACourses.csv','r')))
Info = Courses[0]
Courses = Courses[1:]

font = pg.font.SysFont('Arial',50)
fontS = pg.font.SysFont('Arial',35)

def centDraw(S,X,Y,Wd,C):
    txt = font.render(S,True,C)
    txtW = txt.get_rect()[2]
    if txtW > Wd-20:
        txt = pg.font.SysFont('Arial',int(50*(Wd-20)/txtW)).render(S,True,C)
        txtW = txt.get_rect()[2]
    txtH = txt.get_rect()[3]
    display.blit(txt, (X+int(Wd/2)-int(txtW/2),Y-int(txtH/2)))

def blockText(text, wid):
    words = [word.split(' ') for word in text.splitlines()]
    space = fontS.size(' ')[0]
    max_width = wid
    x,y = 0,0
    WordL = []
    WordLL = []
    for line in words:
        for word in line:
            word_surface = fontS.render(word, True, black)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = 0
                y += word_height
                WordLL.append(WordL)
                WordL = []
            WordL.append((word_surface, (x,y)))
            x += word_width + space
        x = 0
        y += word_height
        WordLL.append(WordL)
        WordL = []
    surf = pg.Surface((wid,y))
    surf.fill(white)
    for WordL in WordLL:
        shft = int((wid-WordL[-1][1][0]-WordL[-1][0].get_width())/2)
        for wordS,ps in WordL:
            surf.blit(wordS, (ps[0]+shft,ps[1]))
    return(surf)

def Quit(save):
    pg.quit()
    if save:
        with open('MyCourses.txt','w') as file:
            for course in CL:
                file.write(course.nn+',')
    sys.exit()

def courseSplit(s):
    lst = Split(spst,s.replace('(','xxx').replace(')','yyy'))
    while '' in lst:
        lst.remove('')
    return(lst)

def isValid():
    for c in CL:
        if not (condMet(c.pre, TL+[cr.nn for cr in CL if cr.pos[0] < c.pos[0]]) and condMet(c.cpre, TL+[cr.nn for cr in CL if cr.pos[0] <= c.pos[0]]) and str(((c.pos[0]-SBW)//DX)%2) in c.sem):
            return(False)
    return(True)

def canSwitch(c1,c2):
    if c1.hours == c2.hours and c1.pos[0] != c2.pos[0] and not (c1.lock or c2.lock):
        c1.pos,c2.pos = c2.pos,c1.pos
        result = isValid()
        c1.pos,c2.pos = c2.pos,c1.pos
        return(result)
    return(False)

def condMet(s,Taken):
    preL = courseSplit(s)
    BoolPreL = [(nn in Taken) for nn in preL]
    for i in range(len(preL)):
        s = s.replace(preL[i],str(BoolPreL[i]))
    return(s == '' or eval(s))

def genSemester(sem):
    global CL
    if SK[sem]:
        return([])
    AL = [c.nn for c in CL if (c.pos[0]-SBW)//DX > sem and not c.lock and str(sem%2) in c.sem]
    BL = TL+[c.nn for c in CL if (c.pos[0]-SBW)//DX < sem]
    SL = [c.nn for c in CL if (c.pos[0]-SBW)//DX == sem]
    hours = sum([c.hours for c in CL if (c.pos[0]-SBW)//DX == sem])
    done = False
    while not done:
        done = True
        rn.shuffle(CL)
        for c in CL:
            if c.nn in AL and hours + c.hours <= max_courses and condMet(c.pre,BL):
                if condMet(c.cpre,BL+SL):
                    SL.append(c.nn)
                    AL.remove(c.nn)
                    hours += c.hours
                    done = False
                    break
                else:
                    br = False
                    for c2 in CL:
                        if c != c2 and hours + c.hours + c2.hours <= max_courses and condMet(c2.pre,BL) and c.nn in courseSplit(c2.cpre) and c2.nn in courseSplit(c.cpre):
                            SL.append(c.nn)
                            SL.append(c2.nn)
                            AL.remove(c.nn)
                            AL.remove(c2.nn)
                            hours += c.hours + c2.hours
                            done = False
                            br = True
                            break
                    if br:
                        break
    return(SL)

def genSchedule():
    global CL
    count = 0
    PCL = {c.nn:c.pos for c in CL}
    while True:
        count += 1
        for c in CL:
            if not c.lock:
                c.pos = [2*W,0]
        tot = sum([c.hours for c in CL])
        for i in range(semesters):
            S = genSemester(i)
            her = 0
            for c in CL:
                if c.nn in S:
                    c.pos = [SBW+i*DX, her]
                    her += int(c.hours*(H/max_courses))
                    tot -= c.hours
                    
        if tot == 0 and isValid():
            return True
        elif count > 1000:
            for c in CL:
                c.pos = PCL[c.nn]
            return False

course_eval = lambda c: c.num + 100*ord(c.name[0].lower()) - 100000*c.hours

class Course():
    def __init__(self,ps,ind):
        self.pos = list(ps)
        self.name = results[ind][0]
        self.num = int(results[ind][1])
        self.nn = self.name+' '+str(self.num)
        self.hours = float(results[ind][2].split(',')[0])
        if self.hours%1 == 0:
            self.hours = int(self.hours)
        self.title = results[ind][3]
        self.desc = results[ind][4]
        self.pre = results[ind][5]
        self.cpre = results[ind][6]
        self.sem = '0'*int('F' in results[ind][7]) + '1'*int('S' in results[ind][7])
        self.w = DX
        self.h = int(self.hours*(H/max_courses))
        self.lock = False

    def update(self):
        if self == selcrs:
            newx = SBW+DX*max(0,(pos[0]-SBW)//DX)
            if pos[0] < SBW:
                self.pos = [pos[0]-int(self.w/2),pos[1]-int(self.h/2)]
            elif str(((pos[0]-SBW)//DX)%2) in self.sem and H-sum([crs.h for crs in CL if crs != self and crs.pos[0] == newx]) >= self.h:
                self.pos[0] = newx
        if self.pos[0] >= SBW:
            self.pos[1] = max([crs.pos[1]+crs.h for crs in CL if crs != self and crs.pos[0] == self.pos[0]]+[0])
                
    def draw(self):
        if sel:
            hovL = [selcrs]
        else:
            hovL = [c for c in CL if 0 < pos[0]-c.pos[0] < c.w and 0 < pos[1]-c.pos[1] < c.h]
        col = 255 - 60*int(self in hovL)
        tc = black
        if hovL != []:
            if self.nn in courseSplit(hovL[0].pre)+courseSplit(hovL[0].cpre):
                tc = blue
            elif hovL[0].nn in courseSplit(self.pre)+courseSplit(self.cpre):
                tc = lred
            elif canSwitch(self, hovL[0]):
                tc = magenta
        pg.draw.rect(display, (col*int(not self.lock), col-50*int(switch != -1 and canSwitch(switch,self)), col*int(not self.lock)-50*int(self == switch)), [self.pos[0],self.pos[1],self.w,self.h])
        pg.draw.rect(display, black, [self.pos[0],self.pos[1],self.w+1,self.h], 2)
        centDraw(self.nn, self.pos[0], self.pos[1]+int(self.h/2), self.w, tc)

    def showStats(self):
        ch = 0
        Soff = 0
        curdisp = display.copy()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Quit(not shift)
                elif event.type == pg.KEYDOWN:
                    if event.key in [pg.K_ESCAPE, pg.K_TAB]:
                        return
                elif event.type == pg.MOUSEBUTTONDOWN:
                    but = event.dict['button']
                    if but in [4,5]:
                        Soff = min(max(0,ch+20-H),max(0,Soff+40*(2*but-9)))

            display.blit(curdisp, (0,0))
            pg.draw.rect(display, white, [SBW,0,W-SBW,H])
            ch = 140
            centDraw('Hours: '+str(self.hours), SBW, ch-Soff, W-SBW, black)
            ch += 85
            centDraw('Description:', SBW, ch-Soff, W-SBW, black)
            ch += 35
            descS = blockText(self.desc+'None'*int(self.desc == ''), W-310)
            display.blit(descS, (305,ch-Soff))
            ch += descS.get_height()+65
            centDraw('Prerequisites:', SBW, ch-Soff, W-SBW, black)
            ch += 35
            preS = blockText(self.pre+'None'*int(self.pre == ''), W-310)
            display.blit(preS, (305,ch-Soff))
            ch += preS.get_height()+65
            centDraw('Concurrent Prerequisites:', SBW, ch-Soff, W-SBW, black)
            ch += 35
            cpreS = blockText(self.cpre+'None'*int(self.cpre == ''), W-310)
            display.blit(cpreS, (305,ch-Soff))
            ch += cpreS.get_height()+65
            centDraw('Semesters Offered:', SBW, ch-Soff, W-SBW, black)
            ch += 35
            cpreS = blockText('Fall '*int('0' in self.sem)+'and '*int(self.sem == '01')+'Spring '*int('1' in self.sem), W-310)
            display.blit(cpreS, (305,ch-Soff))
            ch += cpreS.get_height()
            pg.draw.rect(display, white, [SBW,0,W-SBW,90])
            pg.draw.rect(display, black, [SBW,0,W-SBW,H],3)
            centDraw(self.nn+': '+self.title, SBW, 50, W-SBW, black)
            pg.draw.line(display, black, (SBW,90), (W-50,90), 3)
            
            pg.display.update()
        
max_courses = 16
semesters = 8
inpt = ''
results = [clas for clas in Courses]
off = 0
h = 100
bar = 100+int(h/2)
bardown = False
sel = False
selcrs = -1
CL = []
NL = [nn for nn in open('MyCourses.txt','r').read().split(',')[:-1]]
oNL = [nn for nn in NL]
TL = [nn for nn in open('CompletedCourses.txt','r').read().split(',')[:-1]]
oTL = [nn for nn in TL]
SK = [False for i in range(semesters)]
i = 0
SBW = 300
DX = (W-SBW)//semesters
spst = 'yyy and xxx|yyy and | and xxx| and |yyy or xxx|yyy or | or xxx| or |xxx|yyy'
shift = False
switch = -1

while len(NL) > 0:
    nn = Courses[i][0]+' '+Courses[i][1]
    if nn in NL:
        CL.append(Course((0,0),i))
        NL.remove(nn)
    else:
        i += 1
NL = oNL

genSchedule()

while True:
    pos = pg.mouse.get_pos()
    for event in pg.event.get():
        hovCL = [c for c in CL if 0 < pos[0]-c.pos[0] < c.w and 0 < pos[1]-c.pos[1] < c.h]
        if event.type == pg.QUIT:
            Quit(not shift)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                Quit(not shift)
            elif event.key == pg.K_RETURN:
                genSchedule()
            elif event.key == pg.K_LSHIFT:
                shift = True
            elif event.key == pg.K_TAB:
                if hovCL != []:
                    hovCL[0].showStats()
            elif event.key == pg.K_LALT:
                if hovCL != [] and switch == -1:
                    if [c for c in CL if canSwitch(hovCL[0],c)] != []:
                        switch = hovCL[0]
                else:
                    if hovCL != [] and canSwitch(hovCL[0],switch):
                        hovCL[0].pos,switch.pos = switch.pos,hovCL[0].pos
                    switch = -1
            elif event.key == pg.K_p and shift:
                for c in CL:
                    print(c.nn+':')
                    print('PRE: '+str(c.pre))
                    print('CON_PRE: '+str(c.cpre)+'\n')
            elif event.key == pg.K_LEFT:
                semesters -= 1
                prev = SK[-1]
                SK = SK[:-1]
                DX = (W-SBW)//semesters
                if genSchedule():
                    for c in CL:
                        c.w = DX
                else:
                    semesters += 1
                    SK.append(prev)
                    DX = (W-SBW)//semesters
            elif event.key == pg.K_RIGHT:
                semesters += 1
                SK.append(False)
                DX = (W-SBW)//semesters
                for c in CL:
                    c.w = DX
                genSchedule()
            elif event.key == pg.K_DOWN:
                max_courses -= 1
                if genSchedule():
                    for c in CL:
                        c.h = int(c.hours*(H/max_courses))
                else:
                    max_courses += 1
            elif event.key == pg.K_UP:
                max_courses += 1
                for c in CL:
                    c.h = int(c.hours*(H/max_courses))
                genSchedule()
            else:
                if event.key == pg.K_BACKSPACE:
                    if len(inpt) != 0:
                        inpt = inpt[:-1]
                elif event.key == pg.K_DELETE:
                    inpt = ''
                else:
                    try:
                        ch = chr(event.key)
                        if (ch.isalpha() or ch == ' ') and inpt.count(' ') == 0:
                            inpt = inpt+ch.upper()
                        elif ch.isnumeric() and inpt.count(' ') == 1:
                            inpt = inpt+ch
                    except:
                        pass
                results = [clas for clas in Courses if (' ' in inpt and inpt.split(' ')[0] == clas[0] and inpt.split(' ')[1] == clas[1][:len(inpt.split(' ')[1])]) or (' ' not in inpt and inpt.split(' ')[0] == clas[0][:len(inpt.split(' ')[0])])]
                off = min(max(0,len(results)*50-H+100),off)
                h = max(100,min(H-100,int(((H-100)**2)/(50*len(results)+20))))
                bar = (H-100-h)*off/(50*len(results)-H+100)+100+int(h/2)
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LSHIFT:
                shift = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            but = event.dict['button']
            if but == 1 and not shift:
                if pos[0] < 20 and abs(pos[1]-bar)*2 < h:
                    bardown = True
                elif pos[0] < SBW and 100 < pos[1] < 50*len(results)+100:
                    NC = Course(pos,(pos[1]-100+off)//50)
                    CL.append(NC)
                    selcrs = NC
                    sel = True
                elif pos[0] > SBW and hovCL != [] and not hovCL[0].lock:
                    selcrs = hovCL[0]
                    CL.remove(selcrs)
                    CL.append(selcrs)
                    sel = True
            elif but == 3 or but == 1 and shift:
                if pos[0] > SBW:
                    if hovCL != []:
                        hovCL[0].lock = not hovCL[0].lock
                    else:
                        SK[(pos[0]-SBW)//DX] = not SK[(pos[0]-SBW)//DX]
            elif but in [4,5] and pos[0] < SBW:
                off = min(max(0,len(results)*50-H+100),max(0,off+40*(2*but-9)))
                h = max(100,min(H-100,int(((H-100)**2)/(50*len(results)+20))))
                bar = (H-100-h)*off/(50*len(results)-H+100)+100+int(h/2)
        elif event.type == pg.MOUSEBUTTONUP:
            but = event.dict['button']
            if but == 1:
                bardown = False
                if sel and pos[0] < SBW:
                    CL.remove(selcrs)
                sel = False
                selcrs = -1

    display.fill(grey)

    for i in range(semesters):
        if SK[i]:
            pg.draw.rect(display, (170,138,143), [SBW+DX*i,0,DX,H])
    
    pg.draw.rect(display, red, [0,0,SBW,H])

    if bardown and h != H-100:
        bar = max(100+int(h/2),min(H-int(h/2),pos[1]))
        off = int((bar-100-int(h/2))*(50*len(results)-H+100)/(H-100-h))
    pg.draw.rect(display, black, [0,bar-int(h/2),20,h])

    for i in range(off//50,min(len(results),(off+H-50)//50)):
        centDraw(results[i][0]+' '+results[i][1], 0, i*50+130-off, SBW, black)

    pg.draw.rect(display, red, [0,0,SBW,100])
    pg.draw.line(display, black, (0,100), (SBW,100), 2)
    centDraw(inpt,0,50,SBW,black)

    for x in range(SBW,W+DX,DX):
        pg.draw.line(display, black, (x,0), (x,H), 2)
    pg.draw.rect(display, black, [W-(W-SBW)%DX,0,(W-SBW)%DX,H])

    CL = sorted(CL, key=course_eval)

    for course in CL:
        course.pos[1] = -H
    
    for course in CL:
        course.update()

    for course in CL:
        course.draw()
                
    pg.display.update()
