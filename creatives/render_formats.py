"""Исходники учебной карусели и видеокреатива HubSpot.
Запуск: python render_formats.py --only all
Зависимости: Pillow, FFmpeg. Выходные файлы сохраняются рядом с исходником.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from functools import lru_cache
from html import escape
import argparse, math, subprocess
ROOT=Path(__file__).resolve().parent
FONTROOT=Path('/usr/share/fonts/truetype/dejavu')
INK='#16353b';CORAL='#e85735';CREAM='#fbf8f2';MUTED='#536a6e';TEAL='#a5c7bc'
@lru_cache(maxsize=128)
def font(size,bold=False):return ImageFont.truetype(str(FONTROOT/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),size)
class Card:
 def __init__(self,bg):
  self.im=Image.new('RGB',(1200,1200),bg);self.d=ImageDraw.Draw(self.im)
  self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xml:lang="ru" width="1200" height="1200" viewBox="0 0 1200 1200"><rect width="1200" height="1200" fill="{bg}"/>']
 def box(self,xy,color,r=0,outline=None):
  x,y,w,h=xy;self.d.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=color,outline=outline,width=2)
  self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{color}"'+(f' stroke="{outline}" stroke-width="2"' if outline else '')+'/>')
 def text(self,x,y,s,size=32,color=INK,bold=False,maxw=1050):
  while self.d.textlength(s,font=font(size,bold))>maxw:size-=1
  self.d.text((x,y),s,font=font(size,bold),fill=color,anchor='lt')
  self.svg.append(f'<text x="{x}" y="{y+size}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(s)}</text>')
 def line(self,xy,color,width=4):
  self.d.line(xy,fill=color,width=width)
  self.svg.append(f'<path d="M{xy[0]} {xy[1]}L{xy[2]} {xy[3]}" stroke="{color}" stroke-width="{width}"/>')
 def circle(self,x,y,r,color):
  self.d.ellipse((x-r,y-r,x+r,y+r),fill=color)
  self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
 def save(self,name):
  self.im.save(ROOT/(name+'.png'));(ROOT/(name+'.svg')).write_text('\n'.join(self.svg+['</svg>']))
def carousel():
 c=Card(CREAM);c.text(70,52,'HubSpot · УЧЕБНЫЙ ПРОЕКТ',25,bold=True);c.text(1000,52,'01 / 03',24,color=MUTED)
 c.text(70,180,'Заявка пришла.',76,bold=True);c.text(70,280,'Что дальше?',76,bold=True)
 c.text(70,405,'Когда история разбросана,',31,color=MUTED);c.text(70,450,'команде сложнее продолжить разговор.',31,color=MUTED)
 for x,y,w,title,body,color in [(85,620,310,'Письмо','Запрос клиента','#f5d2c5'),(445,545,310,'Таблица','Контакты','#dce7e0'),(805,655,310,'Заметка','Договорённости','#e6e0f1')]:
  c.box((x+9,y+12,w,230),'#e8e9e1',18);c.box((x,y,w,230),'#ffffff',18,outline='#ccd8d1');c.box((x,y,w,58),color,18);c.text(x+23,y+17,title,24,bold=True,maxw=w-45);c.text(x+23,y+89,body,22,maxw=w-45)
  for j,k in enumerate([1,.75,.9]):c.box((x+23,y+142+j*22,int((w-46)*k),7),'#d8e0da',3)
 c.text(70,1020,'Соберите контекст в одном месте →',34,color=CORAL,bold=True);c.text(70,1120,'Карусель · Листайте дальше',22,color=MUTED);c.save('02-carousel-1')
 c=Card('#edf4ef');c.text(70,52,'HubSpot · УЧЕБНЫЙ ПРОЕКТ',25,bold=True);c.text(1000,52,'02 / 03',24,color=MUTED)
 c.text(70,180,'Вся история',76,bold=True);c.text(70,280,'в одной карточке.',76,bold=True)
 c.box((70,470,1060,485),'#ffffff',26,outline='#ccddd2');c.circle(150,560,40,TEAL);c.text(133,536,'В',38,bold=True);c.text(220,525,'Компания «Вектор»',38,bold=True);c.text(220,581,'Учебный пример карточки клиента',24,color=MUTED)
 for y,title,body in [(665,'Задача','Настроить работу с заявками'),(750,'История','Клиент запросил демонстрацию'),(835,'Действие','Передать запрос в отдел продаж')]:
  c.line((115,y-20,1085,y-20),'#e1e9e3',2);c.text(115,y,title,25,bold=True);c.text(365,y,body,25,maxw=700)
 c.text(70,1020,'Контекст доступен всей команде →',34,color=CORAL,bold=True);c.text(70,1120,'Карусель · Следующий шаг',22,color=MUTED);c.save('02-carousel-2')
 c=Card('#ffffff');c.text(70,52,'HubSpot · УЧЕБНЫЙ ПРОЕКТ',25,bold=True);c.text(1000,52,'03 / 03',24,color=MUTED)
 c.text(70,180,'Следующий шаг',76,bold=True);c.text(70,280,'виден команде.',76,bold=True)
 c.line((160,520,160,870),'#b5cdbf',8)
 for y,n,title,body in [(520,'1','Заявка получена','Потребность клиента зафиксирована'),(680,'2','Контекст передан','Менеджер видит историю обращения'),(840,'3','Действие согласовано','Понятно, что делать дальше')]:
  c.circle(160,y,38,INK if n!='3' else CORAL);c.text(148,y-22,n,31,color='#ffffff',bold=True);c.text(235,y-36,title,33,bold=True);c.text(235,y+16,body,24,color=MUTED,maxw=850)
 c.box((70,970,1060,100),CORAL,12);c.text(110,997,'Посмотрите демо без регистрации →',34,color='#ffffff',bold=True,maxw=970)
 c.text(70,1120,'Учебный макет · indolentmenace.github.io/hubspot-lab3/',21,color=MUTED)
 c.save('02-carousel-3')
 print('Карусель: три последовательные карточки PNG/SVG.',flush=True)

def smooth(x):x=min(1,max(0,x));return x*x*(3-2*x)
def tx(d,xy,s,size=30,color=INK,bold=False):d.text(xy,s,font=font(size,bold),fill=color,anchor='lt')
def box(d,xy,color,r=16,outline=None):d.rounded_rectangle(xy,radius=r,fill=color,outline=outline,width=2)
def scene(k,u):
 bg=[INK,CREAM,'#e7f0e9',CORAL][k];im=Image.new('RGB',(1280,720),bg);d=ImageDraw.Draw(im)
 fg='#ffffff' if k in [0,3] else INK;sub='#bdd3cf' if k==0 else MUTED
 tx(d,(60,38),'HubSpot',29,fg,True);tx(d,(240,43),'УЧЕБНЫЙ ВИДЕОРОЛИК',16,fg)
 if k==0:
  tx(d,(60,148),'Заявка есть.',66,fg,True);tx(d,(60,234),'А контекст',58,fg,True);tx(d,(60,311),'потерялся?',58,fg,True)
  tx(d,(64,436),'Письма, таблицы, заметки…',24,sub);tx(d,(64,478),'Соберите историю клиента.',24,sub)
  for i,(label,col) in enumerate([('Письмо','#f5d2c5'),('Таблица','#dce7e0'),('Заметка','#e6e0f1')]):
   x=790+(i%2)*115+int(18*math.sin(u*2+i));y=160+i*133+int(13*math.cos(u*2+i));box(d,(x,y,x+270,y+105),'#ffffff',14);box(d,(x,y,x+270,y+35),col,12);tx(d,(x+18,y+13),label,20,INK,True)
   for j,w in enumerate([200,155]):box(d,(x+20,y+61+j*18,x+20+w,y+67+j*18),'#d4ded7',2)
  tx(d,(60,643),'От разрозненных записей — к общей истории.',20,sub)
 elif k==1:
  tx(d,(60,155),'Вся история',58,INK,True);tx(d,(60,234),'в одной CRM.',58,INK,True)
  tx(d,(64,360),'Потребность клиента,',26,MUTED);tx(d,(64,403),'договорённости и следующий шаг.',26,MUTED)
  x=685+int(250*(1-smooth(u/.8)));y=155;box(d,(x,y,x+530,y+415),'#ffffff',24,outline='#cbd9ce');box(d,(x,y,x+530,y+94),'#dcebe1',24)
  tx(d,(x+28,y+26),'Компания «Вектор»',31,INK,True)
  for j,(label,body) in enumerate([('Задача','Объединить заявки'),('История','Запрос на демо'),('Действие','Передать в продажи')]):
   if u>j*.65:
    dy=y+126+j*87;d.ellipse((x+28,dy,x+47,dy+19),fill=CORAL);tx(d,(x+64,dy-6),label,20,MUTED);tx(d,(x+64,dy+25),body,26,INK,True)
  tx(d,(60,643),'Учебная иллюстрация принципа работы CRM.',20,MUTED)
 elif k==2:
  tx(d,(60,145),'Передайте заявку',58,INK,True);tx(d,(60,225),'вместе с контекстом.',58,INK,True)
  pts=[(220,465),(640,465),(1060,465)];d.line((220,465,1060,465),fill='#bdcfc3',width=8)
  prog=smooth(u/2.5);d.line((220,465,220+840*prog,465),fill=CORAL,width=8)
  px=220+840*prog;d.ellipse((px-13,452,px+13,478),fill='#ffffff')
  for j,((x,y),label) in enumerate(zip(pts,['Маркетинг','Продажи','Следующий шаг'])):
   active=prog>=j/2;d.ellipse((x-50,y-50,x+50,y+50),fill=CORAL if active else INK);tx(d,(x-13,y-21),str(j+1),35,'#ffffff',True)
   width=d.textlength(label,font=font(24,True));tx(d,(x-width/2,y+82),label,24,INK,True)
  tx(d,(60,643),'Одна команда. Понятное действие.',22,MUTED)
 else:
  tx(d,(60,155),'Посмотрите демо',64,'#ffffff',True);tx(d,(60,245),'без регистрации.',64,'#ffffff',True)
  tx(d,(65,365),'Три шага, чтобы познакомиться с CRM.',28,'#fff5e7')
  pulse=1+0.018*math.sin(u*3);cx,cy=345,500;w,h=int(560*pulse),int(100*pulse);box(d,(cx-w//2,cy-h//2,cx+w//2,cy+h//2),'#ffffff',14);tx(d,(93,475),'Открыть демонстрацию →',29,INK,True)
  tx(d,(65,622),'indolentmenace.github.io/hubspot-lab3/',24,'#ffffff')
  tx(d,(65,666),'Учебный проект. Демонстрация не создаёт аккаунт HubSpot.',17,'#fff5e7')
 return im

def frame(time):
 starts=[0,3,7,11];ends=[3,7,11,15]
 k=next(i for i,e in enumerate(ends) if time<e);u=time-starts[k];im=scene(k,u)
 if k and u<.3:im=Image.blend(scene(k-1,starts[k]-starts[k-1]),im,smooth(u/.3))
 d=ImageDraw.Draw(im);d.rectangle((0,713,int(1280*time/15),719),fill='#ffffff' if k in [0,3] else CORAL)
 return im

def video():
 fps=24;cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','medium','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'03-video.mp4')]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for n in range(15*fps):proc.stdin.write(frame(n/fps).tobytes())
 proc.stdin.close();code=proc.wait();assert code==0,code
 frame(12.5).save(ROOT/'03-video-poster.jpg',quality=92)
 # Иллюстрация ролика в отчёте и презентации; оригинальное видео сохранено отдельно.
 print('Видео: 15 секунд, 1280×720, 24 кадра/с, MP4, русские титры, без звука.',flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--only',choices=['all','carousel','video'],default='all');arg=ap.parse_args()
 if arg.only in ['all','carousel']:carousel()
 if arg.only in ['all','video']:video()
