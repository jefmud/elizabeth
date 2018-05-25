from picamera import PiCamera
from time import sleep
import sys
import easygui
import os
import datetime

camera = PiCamera()
basefolder = "./capture"

easygui.msgbox("Welcome to Muday Lab Root Snap Program")

while True:
	prompt = "Enter Resolution 1=1024x768, 2=2592,1944, or custom resolution separated by commas, ENTER to quit: "
	resolution = easygui.enterbox(prompt)
	#resolution = input(prompt)
	if resolution == '1':
		camera.resolution = (1024, 768)
		break
	if resolution == '2':
		camera.resolution = (2592, 1944)
		break
	if resolution == "":
		print("Exiting")
		sys.exit(0)
	if ',' in resolution:
		try:
			x,y = resolution.split(',')
			x = int(x)
			y = int(y)
			camera.resolution = (x,y)
		except:
			easygui.msgbox("Error: enter 1 or 2, or comma separated integers for custom")
		

while True:
	easygui.msgbox("Click OK to start 10 second preview")
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
		


camera.crop = (0.0, 0.0, 1.0, 1.0)
sleep(2)
camera.capture('./capture/image.jpg')
print("snap")

camera.zoom = (0.2, 0.2, 0.6, 0.6)

def timestamp(date=True,time=True):
	current = datetime.datetime.now()
	if date and time:
		return current.strftime("%Y%m%d_%H%M%S")
	elif date:
		return current.strftime("%Y%m%d")
	return current.strftime("%H%M%S")
	

while True:
	folder = easygui.enterbox('Enter directory to save snaps (leave blank for "capture" subdir): ')
	if folder is None:
		capture_folder = os.join(basefolder, timestamp)
		easygui.msgbox("Program cancelled.  Exiting")
		sys.exit(0)
		
	try:
		minutes = int(minutes)
		break
	except:
		easygui.msgbox("Error: please enter an integer value")

while True:
	minutes = easygui.enterbox("Enter number of MINUTES to run: ")
	if minutes is None:
		easygui.msgbox("Program cancelled.  Exiting")
		sys.exit(0)
		
	try:
		minutes = int(minutes)
		break
	except:
		easygui.msgbox("Error: please enter an integer value")
		
while True:
	snapdelay = easygui.enterbox("Enter delay between captures in SECONDS: ")
	if snapdelay is None:
		easygui.msgbox("Program cancelled.  Exiting")
		sys.exit(0)
		
	try:
		snapdelay = int(snapdelay)
		break
	except:
		easygui.msgbox("Error: please enter an integer value")
numberofsnaps = minutes*60/snapdelay
		
for i in range(numberofsnaps):
    sleep(snapdelay)
    print("snap {}".format(i))
    camera.capture('./capture/image%06d.jpg' % i)
    
easygui.msgbox("Done.  Thank you for using the program.\nPlease check the folder for your snaps.")
