from picamera import PiCamera
from time import sleep
import sys
import easygui

camera = PiCamera()

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

while True:
	numberofsnaps = easygui.enterbox("Enter number of snaps to take: ")
	if numberofsnaps is None:
		easygui.msgbox("Program cancelled.  Exiting")
		sys.exit(0)
		
	try:
		numberofsnaps = int(numberofsnaps)
		break
	except:
		easygui.msgbox("Error: please enter an integer value")
		
while True:
	snapdelay = easygui.enterbox("Enter delay between snaps in seconds: ")
	if snapdelay is None:
		easygui.msgbox("Program cancelled.  Exiting")
		sys.exit(0)
		
	try:
		snapdelay = int(snapdelay)
		break
	except:
		easygui.msgbox("Error: please enter an integer value")
		
for i in range(numberofsnaps):
    sleep(snapdelay)
    print("snap {}".format(i))
    camera.capture('./capture/image%06d.jpg' % i)
    
easygui.msgbox("Done.  Thank you for using the program.\nPlease check the folder for your snaps.")
