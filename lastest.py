from picamera import PiCamera
from time import sleep
import datetime
import smtplib
from email.mime.text import MIMEText
import cv2
import numpy as np 
from matplotlib import pyplot as plt 
import serial
import board
import neopixel
import sys

# data store
sys.stdout = open('/home/pi/data/experimentData.txt','a')
print('aa')

# neopixel setting
pixel_pin = board.D18
num_pixels = 8
pixels = neopixel.Neopixel(board.D18, num_pixels)
ORDER = neopixel.RGBW
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
# pixels.fill((255, 0, 0, 0))
# pixels.show()

# camera setting
camera = PiCamera()
camera.resolution = (3280,2464)
camera.brightness = 52 # Bright Setting is can be changed.

# rgb extraction pixel range setting
seg_range = 30 # (ex. when seg_range=10 -> width=20 , height=20, with picked center point)
point1 = [459,1627]
point2 = [1818,2232]
point3 = [459,1627]
point4 = [1818,2232]
point5 = [459,1627]
point6 = [1818,2232]
point7 = [459,1627]
point8 = [1818,2232]
point9 = [459,1627]
point10 = [1818,2232]

# Serial Communication setting
ser = serial.Serial('/dev/ttyUSB0',115200,timeout=1)
ser.flushInput()
ser.flushOutput()

# Email send
def send_mail(rgb):
    text = rgb
    smtp = smtplib.SMTP('smtp.gmail.com',587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('jhs8891@gmail.com', 'ubivqwqqcomxjbei')
    message = MIMEText(text)
    message['subject'] = 'walden_experiment_data'
    message['From'] = 'jhs8891@gmail.com'
    message['To'] = 'jhs8891@gmail.com'
    smtp.sendmail("jhs8891@gmail.com", "walden.toilet.test@gmail.com", message.as_string())
    smtp.quit()

# RGB extraction
def segment_avg_rgb(r,g,b, left_top_idx, right_bottom_idx):
    seg = r[left_top_idx[0] : right_bottom_idx[0], left_top_idx[1] : right_bottom_idx[1]]
    r_avg = np.average( r[left_top_idx[0] : right_bottom_idx[0], left_top_idx[1] : right_bottom_idx[1]] )
    g_avg = np.average( g[left_top_idx[0] : right_bottom_idx[0], left_top_idx[1] : right_bottom_idx[1]] )
    b_avg = np.average( b[left_top_idx[0] : right_bottom_idx[0], left_top_idx[1] : right_bottom_idx[1]] )
    
    return round(r_avg,3), round(g_avg,3), round(b_avg,3)

def point_avg_rgb(r,g,b, point, seg_range):
    return segment_avg_rgb(r,g,b,[point[0]-seg_range,point[1]-seg_range],[point[0]+seg_range,point[1]+seg_range])

def get_picture(img):
    img_color = cv2.imread(img)
    b, g, r = cv2.split(img_color)
    return r,g,b

# HSV extraction
def segment_avg_hsv(h,s,v, left_top_idx, right_bottom_idx):
    h_avg = np.average( h[left_top_idx[0] : right_bottom_idx[0], left_top_idx[1] : right_bottom_idx[1]] )
    s_avg = np.average( s[left_top_idx[0] : right_bottom_idx[0], left_top_idx[1] : right_bottom_idx[1]] )
    v_avg = np.average( v[left_top_idx[0] : right_bottom_idx[0], left_top_idx[1] : right_bottom_idx[1]] )
    return round(h_avg,3), round(s_avg,3), round(v_avg,3)

def point_avg_hsv(h,s,v, point, seg_range):
    return segment_avg_hsv(h,s,v,[point[0]-seg_range,point[1]-seg_range],[point[0]+seg_range,point[1]+seg_range])

def get_HSV_picture(img):
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    return h,s,v

class email_content(object):
        def __init__(self):
                self.sentence = ''

        def add_content(self,number,r,g,b,h,s,v):
                self.sentence += (str(number) + ':' + str(r)+ ',' +str(g)+',' + str(b)+ ',' +str(h)+ ',' +str(s)+ ',' +str(v)+ '\n')
        
        def clear_content(self,):
                self.sentence = ''

def processingImage():
        nowDateTime = datetime.datetime.now()
        strDateTime = nowDateTime.strftime('%Y-%m-%d %H:%M:%S')
        camera.annotate_text = "Date: %s" % strDateTime
        camera.capture('/home/pi/data/temp.jpg')
        camera.capture('/home/pi/data/backup_%s.jpg' %strDateTime)
        #print('tic')
        r,g,b = get_picture('/home/pi/data/temp.jpg')
        get_HSV_picture('/home/pi/data/temp.jpg')
        #print('tok')

        # image Processing
        r1,g1,b1 = point_avg_rgb(r,g,b, point1, seg_range)
        r2,g2,b2 = point_avg_rgb(r,g,b, point2, seg_range)
        r3,g3,b3 = point_avg_rgb(r,g,b, point3, seg_range)
        r4,g4,b4 = point_avg_rgb(r,g,b, point4, seg_range)
        r5,g5,b5 = point_avg_rgb(r,g,b, point5, seg_range)
        r6,g6,b6 = point_avg_rgb(r,g,b, point6, seg_range)
        r7,g7,b7 = point_avg_rgb(r,g,b, point7, seg_range)
        r8,g8,b8 = point_avg_rgb(r,g,b, point8, seg_range)
        r9,g9,b9 = point_avg_rgb(r,g,b, point9, seg_range)
        r10,g10,b10 = point_avg_rgb(r,g,b, point10, seg_range)

        mail = """
        Capture date : %s

        data 01 : %s , %s , %s
        data 02 : %s , %s , %s
        data 03 : %s , %s , %s
        data 04 : %s , %s , %s
        data 05 : %s , %s , %s
        data 06 : %s , %s , %s
        data 07 : %s , %s , %s
        data 08 : %s , %s , %s
        data 09 : %s , %s , %s
        data 10 : %s , %s , %s
        
        Body Forecast

        """ %(strDateTime ,  r1, g1, b1,  r2, g2, b2,  r3, g3, b3,  r4, g4, b4,  r5, g5, b5, r6, g6, b6,  r7, g7, b7,  r8, g8, b8,  r9, g9, b9,  r10, g10, b10)

print('ready')
try:
        while (1):
                # a = str(raw_input('press z key')) # this line for test
                ser.flushInput()
                data = ser.readline()
                # ser.write("aaaaaa\r\n")
                
                if GPIO.input(8) == GPIO.HIGH: # experiment
                        GPIO.output(3,False) #initialize
                        GPIO.output(5,True)
                        processingImage()
                        print('done')
                elif data == 'z\r\n': # embedded
                        print('captured!')
                        pixels.fill((255, 0, 0, 0))
                        pixels.show()
                        processingImage()
                        send_mail(mail)
                        print('done')
except KeyboardInterrupt :
        print('ecsape')

