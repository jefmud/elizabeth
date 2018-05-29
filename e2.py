from picamera import PiCamera
from time import sleep
import sys
import easygui
import os
import datetime

DEVICE = "box1"
EXTENSION = 'jpg'

def timestamp(date=True,time=True):
	current = datetime.datetime.now()
	if date and time:
		return current.strftime("%Y%m%d_%H%M%S")
	elif date:
		return current.strftime("%Y%m%d")
	return current.strftime("%H%M%S")

def timestamp_name(date=True, time=True, device=None, extension=None):
	if device is None:
		device = DEVICE
	if extension is None:
		extension = EXTENSION
	return '{}_{}.{}'.format(device, timestamp(date, time), extension)
	
camera = PiCamera()
basefolder = "./capture"

easygui.msgbox("Welcome to Muday Lab Root Snap Program")

while True:
	prompt = 'What is the unique name (or number) of this seedling box?\n Note: A name is required to uniquely identify the seedling box'
	device = easygui.enterbox(prompt, title="Specify Device name", default=DEVICE)
	if device is None:
		if not easygui.ynbox("Do you want to continue?"):
			easygui.msgbox("Program cancelled.  Exiting")
			sys.exit(0)
	else:
		DEVICE = device
		break

while True:
	prompt = "Enter Resolution 1=1024x768, 2=2592,1944, or custom resolution separated by commas, ENTER to quit: "
	resolution = easygui.enterbox(prompt, title="Specify Resolution")
	#resolution = input(prompt)
	
	if resolution is None or resolution == "":
		print("Exiting")
		sys.exit(0)
		
	if resolution == '1':
		camera.resolution = (1024, 768)
		break
	if resolution == '2':
		camera.resolution = (2592, 1944)
		break
	
	if ',' in resolution:
		try:
			x,y = resolution.split(',')
			x = int(x)
			y = int(y)
			camera.resolution = (x,y)
		except:
			easygui.msgbox("Error: enter 1 or 2, or comma separated integers for custom")
		

while True:
	easygui.msgbox("Click OK to start 10 second preview", title="Preview")
	#camera.start_preview(alpha=255)
	camera.start_preview(alpha=255, fullscreen=False, window=(30,30,512,389))
	sleep(10)
	camera.stop_preview()
	resp = easygui.ynbox("Are you ready to begin?")
	if resp == True:
		break
	resp = easygui.ynbox("Would you like to try again?\n(note: answering NO will exit program)")
	if resp == False:
		easygui.msgbox("Thanks for using the program.")
		sys.exit(0)
		




#camera.zoom = (0.2, 0.2, 0.6, 0.6)


			
while True:
	folder = easygui.enterbox('Enter directory to save snaps (leave blank for "capture" subdir): ', title="Select Directory")
	if folder is None or folder == "":
		capture_folder = os.path.join(basefolder, timestamp(date=True, time=False))
	else:
		capture_folder = os.path.join(folder, timestamp(date=True,time=False))
		
	if not os.path.exists(capture_folder):
		print("Directory created")
		os.makedirs(capture_folder)
		
	print("Captures will be saved into > {}".format(capture_folder))
	break

# Test snap
camera.crop = (0.0, 0.0, 1.0, 1.0)
sleep(2)
filename = os.path.join(capture_folder,'preview.jpg')
camera.capture(filename)
print("preview snapshot > {}".format(filename))

while True:
	minutes = easygui.enterbox("Enter number of MINUTES to run: ", title="Minutes")
	if minutes is None:
		easygui.msgbox("Program cancelled.  Exiting")
		sys.exit(0)
		
	try:
		minutes = int(minutes)
		break
	except:
		easygui.msgbox("Error: please enter an integer value")
		
print("Total number of minutes > {}".format(minutes))
		
while True:
	snapdelay = easygui.enterbox("Enter delay between captures in SECONDS: ", title="Delay")
	if snapdelay is None:
		easygui.msgbox("Program cancelled.  Exiting")
		sys.exit(0)
		
	try:
		snapdelay = int(snapdelay)
		break
	except:
		easygui.msgbox("Error: please enter an integer value")
		
numberofsnaps = int(minutes*60/snapdelay)
print("Delay between snaps = {}".format(snapdelay))
print("Number of snaps = {}".format(numberofsnaps))
		
for i in range(numberofsnaps):
    filename = os.path.join(capture_folder, timestamp_name())
    camera.capture(filename)
    print("snap {}/{} filename={}".format(i+1,numberofsnaps,filename))
    sleep(snapdelay)
    
easygui.msgbox("Done.  Thank you for using the program.\nPlease check the folder for your snaps.")
