#Ion-Alexandru GHEORGHIU
#MITSC-FILS
#https://github.com/alexandruGheorghiu94

#libraries for the I/O
import RPi.GPIO as GPIO
import time
import array
from time import gmtime, strftime

#library used for getting the space left of the card
import subprocess

#verificare ca fisierul exista
import os.path



#libraries for the OLED display
import Adafruit_GPIO
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#libraries for the Raspberry pi camera
from picamera import PiCamera
from time import sleep

#lybrary used for creating folders
import pathlib


RST = None
#display initialization
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

#camera initialization
camera = PiCamera()

#camera rotation, angle must be modified depending of the orientation of the camera module
#possible values: 0, 90, 180, 270
camera.rotation = 270


#creation of folders for each mode + check of they allready exist
pathlib.Path('/home/pi/Desktop/Photos').mkdir(parents=True, exist_ok=True)
pathlib.Path('/home/pi/Desktop/Videos').mkdir(parents=True, exist_ok=True) 
pathlib.Path('/home/pi/Desktop/Timelapse').mkdir(parents=True, exist_ok=True)



#first run of the script that contains the creation of the file for retaining indexes
if os.path.isfile('/home/pi/Desktop/values.txt') == True :
    
    lines = open('values.txt').read().splitlines()
    photoIndex = int(lines[0])
    videoIndex =  int(lines[1])
    timelapseIndex = int(lines[2])

else:
    
    f = open("values.txt","w+")
    f.write('0 \n')
    f.write('0 \n')
    f.write('0 \n')
    f.close()
    lines = open('values.txt').read().splitlines()
    photoIndex = int(lines[0])
    print(photoIndex)
    videoIndex =  int(lines[1])
    print(videoIndex)
    timelapseIndex = int(lines[2])
    print(timelapseIndex)





#variabila care tine minte indexul pozei
#photoIndex = 0
#variabila care tine minte indexul videoului
#videoIndex = 0
#variabila care tine minte indexul timelapsului
#timelapseIndex = 0
#intervalul la care face poze de timelapse exprimat in secunde
timelapseDuration = 5

#variabila care stie dak inregistrez sau nu
isRecording = False

#camera resolution by default
camera.resolution = (1920, 1080)

#initialication of the button used for controlling the camera
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#quality of the camera selector
qualityIndex = ['1080p30','720p60','480p90']
currentQuality = 0

#1- photos | 2- video | 3-timelapse |
menuIndex = ['Photos', 'Video' , 'Timelapse'];
#the index that goes through menuIndex
currentIndex=1;

#placeholder for the current status of the camera
currentStatus = ""

while True:
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    #Get the available storage
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )


    # Displaying stuff on the screen
    draw.text((x, top),       "Mode: " +menuIndex[currentIndex-1],  font=font, fill=255)
    draw.text((x, top+10),     "Status: "+currentStatus, font=font, fill=255)
    draw.text((x, top+20),    "Quality:"+qualityIndex[currentQuality] ,  font=font, fill=255)
    draw.text((x-11, top+30),    str(Disk),  font=font, fill=255)
    draw.text((x-5, top+40),    ' Time: '+ strftime("%H:%M:%S", gmtime()),  font=font, fill=255)


    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)


    #confirm
    #qualityIndex = ['1080p30','720p60','480p90']
    input_state_confirm = GPIO.input(17)
    if input_state_confirm == False:
        if currentQuality == 2:
            currentQuality= 0
        else:
            currentQuality = currentQuality+1
 
        if currentQuality == 0:
            camera.resolution = (1920, 1080)
            print('FHD quality')
        if currentQuality == 1:
            camera.resolution = (1280, 720)
            print('HD quality')
        if currentQuality == 2:
            camera.resolution = (640, 480)
            print('SD quality')

        time.sleep(0.1)
        
        
    #stanga 
    input_state_left = GPIO.input(18)
    if input_state_left == False:
        if(currentIndex == 1):
            currentIndex = 3
        else:
                currentIndex = currentIndex-1
        
        print(menuIndex[currentIndex-1]+' mode')
        time.sleep(0.1)
        
    #action button   
    input_state_action = GPIO.input(23)
    if input_state_action == False:
        #take a picture
        if (currentIndex == 1):
            camera.capture('/home/pi/Desktop/Photos/image'+str(photoIndex)+'.jpg')
            print('The photo image'+str(photoIndex)+'.jpg was saved in the directory home/pi/Desktop/Photos/')
            currentStatus = 'image'+str(photoIndex)
            photoIndex = photoIndex+1
            time.sleep(0.1)

        #make a video    
        if(currentIndex == 2 and isRecording == False):
            print('Recording has begun.')
            camera.start_recording('/home/pi/Desktop/Videos/video'+str(videoIndex)+'.h264',quality =1)
            currentStatus = "REC"
            videoIndex = videoIndex+1
            isRecording = True
            camera.wait_recording(0.1)
            
        elif(currentIndex == 2 and isRecording == True):
            print('The movie video'+str(videoIndex)+'.h264 was saved in directory /home/pi/Desktop/Videos/')
            camera.stop_recording()
            currentStatus = "Stopped REC"
            isRecording = False
            time.sleep(0.1)

        if currentIndex == 3 :
            currentStatus = 'Running'
            for x in range(0,timelapseDuration):
                camera.capture('/home/pi/Desktop/Timelapse/image'+str(timelapseIndex)+'.jpg')
                timelapseIndex = timelapseIndex+1
                print('Timelapse still image'+str(timelapseIndex)+'.jpg was saved in directory home/pi/Desktop/Timelapse/')
                time.sleep(1)
            currentStatus = 'Done'

    #dreapta   
    input_state = GPIO.input(27)
    if input_state == False:
        if(currentIndex == 3):
            currentIndex = 1
        else:
                currentIndex = currentIndex+1
        
        print(menuIndex[currentIndex-1]+' mode')
        time.sleep(0.1)
    
    lines = open('values.txt').read().splitlines()
    lines[0] = str(photoIndex)
    lines[1] = str(videoIndex)
    lines[2] = str(timelapseIndex)
    open('values.txt','w').write('\n'.join(lines))
