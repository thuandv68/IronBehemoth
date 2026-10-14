"""Animated end card: banner background (logo/text removed) + logo spin-in, wordmark wipe, underline draw,
tagline type-in, logo shine. Full frames -> gfx/endcard/%04d.jpg. The subscribe bar is overlaid by build_full (seq:subscribe).
Usage: python3 tools/make_endcard.py [duration_seconds]"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
TOOLS=os.path.dirname(os.path.abspath(__file__)); EP=os.environ.get('IB_EP',os.getcwd())
C=os.path.join(TOOLS,'common')
OUT=os.path.join(EP,'gfx','endcard'); os.makedirs(OUT,exist_ok=True)
for f in os.listdir(OUT): os.remove(os.path.join(OUT,f))
W,H,FPS=1920,1080,30
DUR=float(sys.argv[1]) if len(sys.argv)>1 else 12.0
NAVY=(15,24,44,255); ORANGE=(232,110,24,255)
bg0=Image.open(os.path.join(C,'brand','endcard_bg.png')).convert('RGB')
logo0=Image.open(os.path.join(C,'brand','brand_logo.png')).convert('RGBA')
WM=ImageFont.truetype(os.path.join(C,'fonts','BebasNeue.ttf'),158)
TG=ImageFont.truetype(os.path.join(C,'fonts','Oswald.ttf'),30); TG.set_variation_by_axes([600])
def clamp(x): return max(0.0,min(1.0,x))
def ease_out(t): return 1-(1-t)**3
def ease_back(t,s=1.7): t-=1; return t*t*((s+1)*t+s)+1
# layout (matches the banner at 1920 width)
LC=(552,512); LD=292
TX=712; TY=0
tmp=ImageDraw.Draw(Image.new('RGBA',(10,10)))
bb=tmp.textbbox((0,0),'IRON BEHEMOTH',font=WM); TW=bb[2]-bb[0]
TY=448-bb[1]
UL_Y=TY+bb[3]+14
TAG='INSIDE THE MACHINES THAT SHAPE WARFARE.'
base=sum(tmp.textlength(c,font=TG) for c in TAG); SP=(TW-base)/(len(TAG)-1)
# wordmark layer
wm=Image.new('RGBA',(TW+20,bb[3]+20),(0,0,0,0)); ImageDraw.Draw(wm).text((-bb[0],0),'IRON BEHEMOTH',font=WM,fill=NAVY)
# tagline glyph positions
tag_x=[]; x=0
for ch in TAG:
    tag_x.append(x); x+=tmp.textlength(ch,font=TG)+SP
TAGW=x-SP
TAG_X0=TX+(TW-TAGW)/2; TAG_Y=UL_Y+22
logo_base=logo0.resize((LD,LD),Image.LANCZOS)
shine_mask=logo_base.getchannel('A')
def frame(t):
    # background: fade from black, slow push-in
    z=1.0+0.04*(t/DUR)
    cw,ch=int(bg0.width/z),int(bg0.height/z); x0=(bg0.width-cw)//2; y0=(bg0.height-ch)//2
    bg=bg0.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.BILINEAR).convert('RGBA')
    img=bg
    # orange pulse ring behind logo
    if 1.05<=t<2.2:
        u=(t-1.05)/1.15; r=LD/2*(1+0.9*ease_out(u)); a=int(200*(1-u))
        ring=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ring)
        d.ellipse([LC[0]-r,LC[1]-r,LC[0]+r,LC[1]+r],outline=ORANGE[:3]+(a,),width=6)
        img.alpha_composite(ring)
    # logo: spin + scale in
    u=clamp((t-0.45)/0.85)
    if u>0:
        sc=0.25+0.75*ease_back(u); ang=-140*(1-ease_out(u))
        sz=max(2,int(LD*sc)); lg=logo_base.resize((sz,sz),Image.LANCZOS).rotate(ang,resample=Image.BICUBIC)
        if u<1: lg.putalpha(lg.getchannel('A').point(lambda v:int(v*min(1,u*2))))
        # shine sweep
        if 3.0<=t<3.9:
            s=(t-3.0)/0.9; band=Image.new('L',(LD,LD),0); bd=ImageDraw.Draw(band)
            cx=-LD*0.6+s*LD*2.2
            bd.polygon([(cx,0),(cx+70,0),(cx-90,LD),(cx-160,LD)],fill=150)
            band=band.filter(ImageFilter.GaussianBlur(14)); band=ImageChops.multiply(band,shine_mask)
            white=Image.new('RGBA',(LD,LD),(255,255,255,0)); white.putalpha(band)
            lg=logo_base.copy(); lg.alpha_composite(white)
        img.alpha_composite(lg,(int(LC[0]-lg.width/2),int(LC[1]-lg.height/2)))
    # wordmark wipe + slide
    u=clamp((t-1.15)/0.8)
    if u>0:
        e=ease_out(u); wpx=int(wm.width*e)
        if wpx>0:
            part=wm.crop((0,0,wpx,wm.height)); dx=int(40*(1-e))
            img.alpha_composite(part,(TX+dx,TY))
    # underline draw
    u=clamp((t-1.85)/0.7)
    if u>0:
        d=ImageDraw.Draw(img); x1=TX+TW*ease_out(u)
        d.rectangle([TX,UL_Y,x1,UL_Y+3],fill=ORANGE)
    # tagline letters fade in one by one
    if t>=2.35:
        lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
        for i,ch in enumerate(TAG):
            a=clamp((t-2.35-i*0.025)/0.25)
            if a>0: d.text((TAG_X0+tag_x[i],TAG_Y+6*(1-a)),ch,font=TG,fill=NAVY[:3]+(int(255*a),))
        img.alpha_composite(lay)
    # fade from / to black
    k=min(clamp(t/0.6), clamp((DUR-t)/1.0))
    if k<1: img=Image.blend(Image.new('RGBA',(W,H),(0,0,0,255)),img,k)
    return img.convert('RGB')
n=int(DUR*FPS)
for i in range(n): frame(i/FPS).save(os.path.join(OUT,f'{i:04d}.jpg'),quality=93)
print('endcard frames',n)
