import time
import subprocess
import RPi.GPIO as GPIO
import datetime
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

GPIO.setmode(GPIO.BCM)
button_pin = 17  # GPIO Pin Button change screen
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define I2C
serial = i2c(port=1, address=0x3C)

# display
WIDTH = 128
HEIGHT = 64

# Start Device OLED SSH1106
device = sh1106(serial, width=WIDTH, height=HEIGHT, rotate=0)

image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

def display1():
    font = ImageFont.truetype('PixelOperator.ttf', 16)
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "top -bn1 | grep \"Cpu(s)\" | awk '{printf \"CPU: %.1f%%\", $2}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%.0fGB %.1f%%\", $3,$2/1024,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

    draw.text((0, 0), "IP: " + IP, font=font, fill=255)
    draw.text((0, 16), CPU, font=font, fill=255)
    draw.text((75, 16), Temp, font=font, fill=255)
    draw.text((0, 32), MemUsage, font=font, fill=255)
    draw.text((0, 48), Disk, font=font, fill=255)

    device.display(image)


def display2():
    font = ImageFont.truetype('PixelOperator.ttf', 45)
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")

    x = 15
    y = 15
    draw.text((x, y), current_time, font=font, fill=255)

    device.display(image)




# Default start screen
current_function = display2
while True:
    if GPIO.input(button_pin) == GPIO.LOW:
        if current_function == display1:
            current_function = display2
        else:
            current_function = display1

    current_function()

    time.sleep(1)


GPIO.cleanup()
