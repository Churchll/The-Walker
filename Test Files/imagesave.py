from pygame import *
from glob import *

init()
running = True
screen = display.set_mode((800,600))
display.set_caption("Right click to save.")
screen.fill((255,255,255))

canvas = Rect(10,10,780,580)
draw.rect(screen, (0,0,0), canvas, 1)

def getName():
    ans = ""                    # final answer will be built one letter at a time.
    arialFont = font.SysFont("Times New Roman", 16)
    typing = True
    while typing:
        for e in event.get():
            if e.type == QUIT:
                event.post(e)   # puts QUIT back in event list so main quits
                return ""
            if e.type == KEYDOWN:
                if e.key == K_BACKSPACE:    # remove last letter
                    if len(ans)>0:
                        ans = ans[:-1]
                elif e.key == K_KP_ENTER or e.key == K_RETURN : 
                    typing = False
                elif e.key < 256:
                    ans += e.unicode       # add character to ans
                    
        txtPic = arialFont.render(ans, True, (0,0,0))   #
        screen.blit(txtPic,(50,50))
        display.flip()
    return ans

while running:
	for e in event.get():
		if e.type == QUIT:
			running = False
	name = getName()
	print(name)
	display.flip()
quit()
