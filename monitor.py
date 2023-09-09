import time
import subprocess
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

# Defina o objeto de série I2C
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
icon_font = ImageFont.truetype('lineawesome-webfont.ttf', 18)

while True:
    # Limpe a imagem
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    # Shell scripts para monitoramento do sistema
    cmd = "hostname -I | cut -d' ' -f1 | head --bytes -1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "top -bn1 | grep load | awk '{printf \"%.2fLA\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
    Temperature = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "smartctl -a /dev/sda | awk '/Temperature_Celsius/ {print $10}'"
    diskt = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Ícones
    # Ícone temperatura
    draw.text((0, 5), chr(62609), font=icon_font, fill=255)
    # Ícone uso de memória
    draw.text((65, 5), chr(62776), font=icon_font, fill=255)
    # Ícone uso de disco
    draw.text((0, 25), chr(63426), font=icon_font, fill=255)
    # Ícone uso da CPU
    draw.text((65, 25), chr(62171), font=icon_font, fill=255)
    # Ícone wifi
    draw.text((0, 45), chr(61931), font=icon_font, fill=255)

    # Texto
    # Texto temperatura
    draw.text((19, 5), Temperature, font=font, fill=255)
    # Texto uso de memória
    draw.text((87, 5), MemUsage, font=font, fill=255)
    # Texto uso de disco
    #draw.text((19, 25), Disk, font=font, fill=255)
    draw.text((19, 25), diskt, font=font, fill=255)
    # Texto uso da CPU
    draw.text((87, 25), CPU, font=font, fill=255)
    # Texto endereço IP
    draw.text((19, 45), IP, font=font, fill=255)

    # Exibir imagem no display
    device.display(image)

    # Aguardar um tempo antes de atualizar novamente
    time.sleep(1)

