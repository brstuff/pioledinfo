import time
import subprocess
import RPi.GPIO as GPIO
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BCM)
button_pin = 17  # Substitua pelo número do pino GPIO que você está usando
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define o objeto de série I2C
serial = i2c(port=1, address=0x3C)

# Configuração do display
WIDTH = 128
HEIGHT = 64

# Inicialize o dispositivo OLED SSH1106
device = sh1106(serial, width=WIDTH, height=HEIGHT, rotate=0)

# Crie uma imagem em branco para desenhar
image = Image.new("1", (WIDTH, HEIGHT))

# Obtenha o objeto de desenho para desenhar na imagem
draw = ImageDraw.Draw(image)

# Crie uma fonte
font = ImageFont.truetype('PixelOperator.ttf', 16)

def display1():
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    # Shell scripts para monitoramento do sistema
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Exibir estatísticas do Pi no display
    draw.text((0, 0), "IP: " + IP, font=font, fill=255)
    draw.text((0, 16), CPU + " LA", font=font, fill=255)
    draw.text((80, 16), Temp, font=font, fill=255)
    draw.text((0, 32), MemUsage, font=font, fill=255)
    draw.text((0, 48), Disk, font=font, fill=255)

    # Exibir a imagem no display
    device.display(image)


def display2():
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    draw.text((0, 48), "teste", font=font, fill=255)

    # Exibir a imagem no display
    device.display(image)



current_function = display1
while True:
    # Verifica se o botão foi pressionado
    if GPIO.input(button_pin) == GPIO.LOW:
        # Alterna entre as funções
        if current_function == display1:
            current_function = display2
        else:
            current_function = display1

    # Chama a função atual
    current_function()

    # Aguarda um pequeno intervalo para evitar detecções múltiplas
    time.sleep(1)


GPIO.cleanup()
