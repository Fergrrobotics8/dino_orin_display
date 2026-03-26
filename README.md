# 1. Create the service file to execute it indefinitely
```bash
sudo nano /etc/systemd/system/dino_oled.service
```
Copy the contents of this in file and save it (ctrl+o & ctrl+x). Be sure to modify the necessary directories for it to work:
```bash
[Unit]
Description=Juego Dino OLED Orin NX
After=network.target
 
[Service]
3Use inverted bar for the space in the path
ExecStart=/usr/bin/python3 /home/fgarcia/funditec/Orin\ NX/display_orin.py
WorkingDirectory=/home/fgarcia/funditec/Orin\ NX/
Restart=always
User=fgarcia
Group=i2c
 
[Install]
WantedBy=multi-user.target
```
# 2. Configure and start the service (it will start automatically each time after reboot)
```bash
sudo systemctl daemon-reload
sudo systemctl restart dino_oled.service
sudo systemctl status dino_oled.service
```


![Dino_GIF](assets/dino.gif)
