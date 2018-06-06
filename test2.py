# Test the live preview capabilities of the camera and save the settings to a file
from picamera import PiCamera
from guizero import App, Text, PushButton, Window, info, Text, TextBox
from time import sleep
from easygui import enterbox, ynbox

# set up main App and Camera
app = App(title="Camera Preview", width=1024, height=768, layout="grid")
camera = PiCamera()

def update_text_boxes():
	"""update the values into the text boxes"""
	txt_cx.value = str("%.2f" % cx)
	txt_cy.value = str("%.2f" % cy)
	txt_cw.value = str("%.2f" % cw)
	txt_ch.value = str("%.2f" % ch)
		
def preview_show():
	"""open the preview window"""
	pX=app.tk.winfo_x() + 100
	pY=app.tk.winfo_y() + 200
	camera.start_preview(alpha=255, fullscreen=False, window=(pX, pY, pW, pH))
	update_text_boxes()
	

	
def preview_hide():
	"""hide the preview window"""
	camera.stop_preview()
			
def preview_change(args):
	"""a change was issued to camera preview"""
	global cx, cy, cw, ch
	dx = 0.01
	dy = 0.01
	dh = 0.01
	dw = 0.01
	
	if args == 'reset':
		cx = 0.02
		cy = 0.02
		ch = 1.0
		cw = 1.0
		
	if args == 'z+':
		cw -= dw
		ch -= dh
	if args == 'z-':
		cw += dw
		ch += dh
		
	if args=='x+':
		cx += dx
	if args=='x-':
		cx -= dx
	if cx < 0.0:
		cx = 0.0
	if cx > 1.0:
		cx = 1.0
		
	if args=='y+':
		cy += dy
	if args=='y-':
		cy -= dy
	if cy < 0.0:
		cy = 0.0
	if cy > 1.0:
		cy = 1.0
		
	if args=='w+':
		cw += dw
	if args=='w-':
		cw -= dw
	if cw < 0.0:
		cw = 0.0
	if cw > 1.0:
		cw = 1.0
		
	if args=='h+':
		ch += dh
	if args=='h-':
		ch -= dh
	if ch < 0.0:
		ch = 0.0
	if ch > 1.0:
		ch = 1.0
		
	#print(cx,cy,cw,ch)
	update_text_boxes()
	camera.zoom = (cx,cy,cw,ch)
	
def save_settings():
	#resp = ynbox('Are you sure?')
	with open('camera_settings.txt','w') as fp:
		buf='x={0:.2f}\ny={1:.2f}\nw={2:.2f}\nh={3:.2f}\n'.format(cx,cy,cw,ch)
		fp.write(buf)
	preview_hide()
	info('info','settings saved')
		

pX=app.tk.winfo_x()
pY=200
pW=640
pH=480
cx=0.02
cy=0.02
cw=1.0
ch=1.0
	
btn1 = PushButton(app, text="Open Preview", command=preview_show, grid=[0,0,2,1])
btn2 = PushButton(app, text="Close Preview", command=preview_hide, grid=[2,0,2,1])
btn_reset = PushButton(app, text="Reset", command=preview_change, args=['reset'], grid=[4,0,2,1])
btn_save = PushButton(app, text="Save Settings", command=save_settings, grid=[6,0,2,1])
lbl_cx = Text(app, text="cX", grid=[0,3])
txt_cx = TextBox(app, grid=[1,3])
lbl_cy = Text(app, text="cY", grid=[2,3])
txt_cy = TextBox(app, grid=[3,3])
lbl_cw = Text(app, text="cW", grid=[4,3])
txt_cw = TextBox(app, grid=[5,3])
lbl_ch = Text(app, text="cH", grid=[6,3])
txt_ch = TextBox(app, grid=[7,3])
btn_xp = PushButton(app, text="<-", command=preview_change, args=['x+'], grid=[0,1])
btn_xm = PushButton(app, text="->", command=preview_change, args=['x-'], grid=[0,2])
btn_yp = PushButton(app, text="^", command=preview_change, args=['y+'], grid=[1,1])
btn_ym = PushButton(app, text="v", command=preview_change, args=['y-'],grid=[1,2])
btn_wp = PushButton(app, text="W+", command=preview_change, args=['w+'], grid=[2,1])
btn_wm = PushButton(app, text="W-", command=preview_change, args=['w-'], grid=[2,2])
btn_hp = PushButton(app, text="H+", command=preview_change, args=['h+'], grid=[3,1])
btn_hm = PushButton(app, text="H-", command=preview_change, args=['h-'],grid=[3,2])
btn_zp = PushButton(app, text="Z+", command=preview_change, args=['z+'], grid=[4,1])
btn_zm = PushButton(app, text="Z-", command=preview_change, args=['z-'],grid=[4,2])

camera.resolution = (1024, 768)
#camera.zoom = (0.37,0.37,0.27,0.27)
#camera.start_preview(alpha=255, fullscreen=False, window=(30,30,512,389))
#sleep(5)
#camera.stop_preview()

print(app.tk.winfo_x(), app.tk.winfo_y())
app.display()
