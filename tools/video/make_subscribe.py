"""Animated channel bar: logo + name + Subscribe -> Subscribed (one click) + ringing bell. Centered at bottom. Outputs RGBA PNG sequence."""
import os, math
from PIL import Image, ImageDraw, ImageFont
TOOLS=os.path.dirname(os.path.abspath(__file__)); EP=os.environ.get('IB_EP',os.getcwd())
C=os.path.join(TOOLS,'common')
OUT=os.path.join(EP,'gfx','subscribe'); os.makedirs(OUT,exist_ok=True)
W,H,FPS,DUR=1920,1080,30,4.6
S=1.6  # scale of the whole bar
def F(sz,w):
    f=ImageFont.truetype(os.path.join(C,'fonts','Roboto.ttf'),int(sz*S))
    f.set_variation_by_axes([w,100])
    return f
NAME=F(30,700); BTN=F(25,600)
logo=Image.open(os.path.join(C,'brand','brand_logo.png')).convert('RGBA').resize((int(58*S),int(58*S)),Image.LANCZOS)
def ease_out(t): return 1-(1-t)**3
def ease_io(t): return 3*t*t-2*t*t*t
def clamp(x): return max(0,min(1,x))
# layout (unscaled units)
pad=14; lh=58
def layout(d):
    x=pad; items={}
    items['logo']=(x,pad); x+=lh+16
    nb=d.textbbox((0,0),'Iron Behemoth',font=NAME); items['name']=(x,pad+lh/2); x+= (nb[2]-nb[0])/S+26
    sb=d.textbbox((0,0),'Subscribed',font=BTN); sw=(sb[2]-sb[0])/S+34+26; items['sub']=(x,pad+4,sw,lh-8); x+=sw+14
    items['bell']=(x,pad+4,lh-8,lh-8); x+=lh-8+pad
    return items,x,lh+2*pad
tmp=ImageDraw.Draw(Image.new('RGBA',(10,10)))
IT,BW,BH=layout(tmp)
BX=int((W-BW*S)/2); BY=H-120-BH*S   # centered at bottom
def thumb(d,cx,cy,s,fill):
    # simple thumbs-up icon
    col=(255,255,255,255)
    w=2*s/14
    d.rounded_rectangle([cx-9*s/10,cy-1*s/10,cx-5*s/10,cy+9*s/10],int(1.5*s/10),outline=col,width=max(2,int(w)),fill=col if fill else None)
    pts=[(cx-3*s/10,cy-1*s/10),(cx+0*s/10,cy-8*s/10),(cx+2*s/10,cy-8*s/10),(cx+2*s/10,cy-3*s/10),(cx+8*s/10,cy-3*s/10),(cx+9*s/10,cy-1*s/10),(cx+7*s/10,cy+9*s/10),(cx-3*s/10,cy+9*s/10)]
    d.polygon(pts,outline=col,fill=col if fill else None,width=max(2,int(w)))
def bell_icon(size,ang,col=(255,255,255,255)):
    b=Image.new('RGBA',(size*2,size*2),(0,0,0,0)); d=ImageDraw.Draw(b); c=size; r=size*0.42
    d.pieslice([c-r,c-r*1.15,c+r,c+r*0.85],180,360,fill=col)
    d.polygon([(c-r,c-r*0.15),(c+r,c-r*0.15),(c+r*1.25,c+r*0.75),(c-r*1.25,c+r*0.75)],fill=col)
    d.ellipse([c-r*0.22,c+r*0.78,c+r*0.22,c+r*1.15],fill=col)
    d.ellipse([c-r*0.12,c-r*1.32,c+r*0.12,c-r*1.08],fill=col)
    return b.rotate(ang,resample=Image.BICUBIC,center=(c,c-r))
def check(d,x,y,s,col):
    d.line([(x,y),(x+s*0.35,y+s*0.35),(x+s,y-s*0.45)],fill=col,width=max(3,int(s/5)),joint='curve')
def cursor(img,x,y,sc=1.0):
    c=Image.new('RGBA',(80,90),(0,0,0,0)); d=ImageDraw.Draw(c)
    p=[(4,4),(4,64),(19,50),(30,76),(40,72),(29,46),(48,46)]
    d.polygon(p,fill=(255,255,255,255),outline=(0,0,0,255),width=4)
    c=c.resize((int(80*sc*S*0.75),int(90*sc*S*0.75)),Image.LANCZOS)
    img.alpha_composite(c,(int(x),int(y)))
T_SUB_CLICK=1.45; T_BELL=1.75
def frame(t):
    img=Image.new('RGBA',(W,H),(0,0,0,0))
    # slide in/out
    a_in=ease_out(clamp(t/0.45)); a_out=ease_io(clamp((t-(DUR-0.5))/0.5))
    alpha=a_in*(1-a_out); dy=(1-a_in)*60+a_out*60
    bar=Image.new('RGBA',(int(BW*S)+4,int(BH*S)+4),(0,0,0,0)); d=ImageDraw.Draw(bar)
    d.rounded_rectangle([0,0,BW*S,BH*S],int(BH*S/2),fill=(22,22,24,225),outline=(255,255,255,40),width=2)
    lx,ly=IT['logo']; bar.alpha_composite(logo,(int(lx*S),int(ly*S)))
    nx,ny=IT['name']; d.text((nx*S,ny*S),'Iron Behemoth',font=NAME,fill=(255,255,255,255),anchor='lm')
    # subscribe button
    sx,sy,sw,sh=IT['sub']; subbed=t>=T_SUB_CLICK
    pop=1+0.08*math.exp(-((t-T_SUB_CLICK)*9)**2) if subbed else 1
    cxb,cyb=(sx+sw/2)*S,(sy+sh/2)*S; hw,hh=sw*S/2*pop,sh*S/2*pop
    if subbed:
        d.rounded_rectangle([cxb-hw,cyb-hh,cxb+hw,cyb+hh],int(hh),fill=(58,58,60,255))
        check(d,cxb-hw+20*S,cyb,14*S,(255,255,255,255))
        d.text((cxb+10*S,cyb),'Subscribed',font=BTN,fill=(255,255,255,255),anchor='mm')
    else:
        d.rounded_rectangle([cxb-hw,cyb-hh,cxb+hw,cyb+hh],int(hh),fill=(245,245,245,255))
        d.text((cxb,cyb),'Subscribe',font=BTN,fill=(15,15,15,255),anchor='mm')
    # bell (appears after subscribe, rings)
    bx,by,bw,bh=IT['bell']
    if t>=T_SUB_CLICK:
        k=ease_out(clamp((t-T_SUB_CLICK)/0.25))
        ang=18*math.sin((t-T_BELL)*28)*math.exp(-(t-T_BELL)*2.5) if t>=T_BELL else 0
        cxl,cyl=(bx+bw/2)*S,(by+bh/2)*S; rr=bh*S/2*k
        d.ellipse([cxl-rr,cyl-rr,cxl+rr,cyl+rr],fill=(58,58,60,255))
        if k>0.3:
            ic=bell_icon(int(25*S*k),ang); bar.alpha_composite(ic,(int(cxl-ic.width/2),int(cyl-ic.height/2+2*S)))
    if alpha<1:
        a=bar.getchannel('A').point(lambda v:int(v*alpha)); bar.putalpha(a)
    img.alpha_composite(bar,(BX,int(BY+dy)))
    # cursor path (absolute coords)
    p_start=(BX+BW*S+260,BY+BH*S+180)
    p_sub=(BX+cxb+10,BY+cyb+6); p_end=(BX+BW*S+220,BY+BH*S+170)
    def lerp(a,b,u): return (a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u)
    if 0.55<=t<DUR-0.35:
        if t<1.3: pos=lerp(p_start,p_sub,ease_io(clamp((t-0.55)/0.75)))
        elif t<2.4: pos=p_sub
        else: pos=lerp(p_sub,p_end,ease_io(clamp((t-2.4)/0.9)))
        sc=0.85 if abs(t-T_SUB_CLICK)<0.08 else 1.0
        cursor(img,pos[0],pos[1],sc)
    return img
n=int(DUR*FPS)
for i in range(n): frame(i/FPS).save(os.path.join(OUT,f'{i:04d}.png'))
print('frames',n,'click',T_SUB_CLICK,'bell',T_BELL)
