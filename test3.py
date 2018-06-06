# Test the live preview capabilities of the camera and save the settings to a file
# this program is in its very alpha stages, so it is decidedly inelegant!
#
# Jeff Muday, Wake Forest University 2018
#
#
from picamera import PiCamera
from guizero import App, Text, PushButton, Window, info, Text, TextBox, CheckBox
from time import sleep
from easygui import enterbox, ynbox

DEBUG = True

# set up main App and Camera
app = App(title="Camera Preview", width=1024, height=768, layout="grid")
camera = PiCamera()

def update_text_boxes():
	"""update the values into the text boxes"""
	txt_cx.value = str("%.2f" % cx)
	txt_cy.value = str("%.2f" % cy)
	txt_cw.value = str("%.2f" % cw)
	txt_ch.value = str("%.2f" % ch)
	txt_cb.value = str(cb)
	txt_cc.value = str(cc)
		
def preview_show():
	"""open the preview window"""
	pX=app.tk.winfo_x() + pXdelta
	pY=app.tk.winfo_y() + pYdelta
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
	
	print("preview_change: ", args)
	
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
	
def exposure_change(args):
	if DEBUG: print("exposure change: ", args)
	if args=="auto":
		if cbx_auto.value:
			camera.exposure_mode="off"
		else:
			update_text_boxes()
		
	if args == "apply" and cbx_auto.value == False:
		if DEBUG: print("exposure_change: apply manual values")
		try:
			cb = int(txt_cb.value)
			txt_cb.text_color = "black"
			camera.brightness = cb
		except:
			txt_cb.text_color = "red"
		try:
			cc = int(txt_cc.value)
			txt_cc.text_color = "black"
			camera.contrast = cc
		except:
			txt_cc.text_color = "red"
			
	
def save_settings():
	#resp = ynbox('Are you sure?')
	with open('camera_settings.txt','w') as fp:
		buf='x={0:.2f}\ny={1:.2f}\nw={2:.2f}\nh={3:.2f}\n'.format(cx,cy,cw,ch)
		buf+='exposure={0}\nbright={1}\ncont={2}'.format(cex,cb,cc)
		fp.write(buf)
	preview_hide()
	info('info','settings saved')
		

# preview window, has to be mostly static (for now)
# picamera "overlays" the display in the window at topmost level
# not controlled by guizero/tkinter, so it simulates being in the window
pXdelta=100 # offset from window left anchor
pYdelta=250 # offset from window top anchor
pW=640 # preview window width
pH=480 # preview window height

# initial camera zoom and exposure
cx=0.02 # zoom x (0.0 - 1.0)
cy=0.02 # zoom y (0.0 - 1.0)
cw=1.0 # zoom width (0.0 - 1.0)
ch=1.0 # zoom height (0.0 - 1.0)
cb = 50 # camera brightness (0-100)
cc = 50 # camera contrast (0-100)
cex='auto' # camera exposure see documentation
camera.resolution = (1024, 768)

# top level buttons
btn1 = PushButton(app, text="Open Preview", command=preview_show, grid=[0,0,2,1])
btn2 = PushButton(app, text="Close Preview", command=preview_hide, grid=[2,0,2,1])
btn_reset = PushButton(app, text="Reset", command=preview_change, args=['reset'], grid=[4,0,2,1])
btn_save = PushButton(app, text="Save Settings", command=save_settings, grid=[6,0,2,1])

# camera zoom (cx, cy, cw, ch) text boxes and labels
lbl_cx = Text(app, text="cX", grid=[0,3])
txt_cx = TextBox(app, grid=[1,3])
lbl_cy = Text(app, text="cY", grid=[2,3])
txt_cy = TextBox(app, grid=[3,3])
lbl_cw = Text(app, text="cW", grid=[4,3])
txt_cw = TextBox(app, grid=[5,3])
lbl_ch = Text(app, text="cH", grid=[6,3])
txt_ch = TextBox(app, grid=[7,3])

# interactive zoom controls
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

# brightness/contrast
lbl_cb = Text(app, text="brit", grid=[0,4])
txt_cb = TextBox(app, grid=[1,4], command=exposure_change)
lbl_cc = Text(app, text="cont", grid=[2,4])
txt_cc = TextBox(app, grid=[3,4], command=exposure_change)
cbx_auto = CheckBox(app, "auto exposure", grid=[4,4], command=exposure_change, args=["auto"])
cbx_auto.value = True
btn_bright_apply = PushButton(app, text="Apply Exposure", grid=[5,4], command=exposure_change, args=["apply"])

app.display()
