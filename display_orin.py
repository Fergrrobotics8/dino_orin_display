import smbus2
from PIL import Image, ImageDraw, ImageFont
import time

# Configuración I2C (Bus 7)
BUS = 7
ADDR = 0x3c
bus = smbus2.SMBus(BUS)

def command(cmd): bus.write_byte_data(ADDR, 0x00, cmd)

def init_display():
    cmds = [0xAE, 0xD5, 0x80, 0xA8, 0x1F, 0xD3, 0x00, 0x40, 0x8D, 0x14, 0x20, 0x00, 
            0xA1, 0xC8, 0xDA, 0x02, 0x81, 0x7F, 0xD9, 0xF1, 0xDB, 0x40, 0xA4, 0xA6, 0xAF]
    for c in cmds: command(c)

def display_image(img):
    pix = img.load()
    for page in range(4):
        command(0xB0 + page)
        command(0x00)
        command(0x10)
        for x in range(128):
            byte = 0
            for bit in range(8):
                if pix[x, page * 8 + bit]: byte |= (1 << bit)
            bus.write_byte_data(ADDR, 0x40, byte)

# --- DINO T-REX (Ojo 2x2 y Garras Adelante) ---
def draw_dino(d, x, y, vivo=True):
    # Cabeza (agrandada un pelín para el ojo)
    d.rectangle((x+10, y, x+17, y+6), fill=1)    
    # OJO 2x2: Hueco (0) si vive, Relleno (1) si muere
    d.rectangle((x+11, y+1, x+12, y+2), fill=0 if vivo else 1)  
    d.rectangle((x+17, y+3, x+19, y+6), fill=1)  # Hocico
    # Cuerpo
    d.rectangle((x+6, y+6, x+13, y+11), fill=1)  
    d.point((x+14, y+7), fill=1)                 # Bracito
    # Cola en J
    d.rectangle((x+4, y+7, x+6, y+10), fill=1)    
    d.rectangle((x+2, y+9, x+4, y+11), fill=1)   
    d.point((x+1, y+10), fill=1)                  
    # PATAS GORDAS (2px)
    d.rectangle((x+7, y+12, x+8, y+14), fill=1)  
    d.rectangle((x+11, y+12, x+12, y+14), fill=1) 
    # GARRAS HACIA ADELANTE
    d.point((x+9, y+14), fill=1)
    d.point((x+13, y+14), fill=1)

def draw_cactus(d, x, y):
    # Tronco central (2px ancho, más alto que los brazos)
    d.rectangle((x+3, y, x+4, y+9), fill=1)      
    # Brazo izquierdo (Forma de L hacia arriba)
    d.rectangle((x+1, y+4, x+1, y+7), fill=1)    # Vertical brazo L
    d.point((x+2, y+7), fill=1)                  # Codo L
    # Brazo derecho (Forma de L hacia arriba)
    d.rectangle((x+6, y+3, x+6, y+6), fill=1)    # Vertical brazo R
    d.point((x+5, y+6), fill=1)                  # Codo R



init_display()

try:
    font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
except:
    font_bold = ImageFont.load_default()

while True:
    score = 0
    cactus_x = 128
    dino_y = 16 
    velocidad = 0.010 
    
    while score < 15:
        img = Image.new('1', (128, 32), 0)
        draw = ImageDraw.Draw(img)
        
        cactus_x -= 12
        if cactus_x < -10:
            cactus_x = 128
            score += 1
        
        # Salto
        if 0 < cactus_x < 35:
            dino_y = 2 
        else:
            dino_y = 16 
            
        draw.text((42, 0), "ORIN NX", font=font_bold, fill=1)
        draw_dino(draw, 10, dino_y, vivo=True)
        draw_cactus(draw, cactus_x, 22)
        draw.line((0, 31, 128, 31), fill=1) 
        
        display_image(img)
        time.sleep(velocidad)

    # --- GAME OVER ---
    img_go = Image.new('1', (128, 32), 0)
    draw_go = ImageDraw.Draw(img_go)
    draw_dino(draw_go, 10, 16, vivo=False) 
    draw_go.text((45, 12), "GAME OVER", font=font_bold, fill=1)
    display_image(img_go)
    time.sleep(2.5)

