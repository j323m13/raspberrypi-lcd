from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime
import requests
import os
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# compatible with all versions of RPI as of Jan. 2019
# v1 - v3B+
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)


# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows)

# looking for an active Ethernet or WiFi device
def find_interface():
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name

# find an active IP on the first LIVE network device
def parse_ip():
    find_ip = "ip addr show %s" % interface
    find_ip = "ip addr show %s" % interface
    ip_parse = run_cmd(find_ip)
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]
    return ip

# find external IP
def getExternalIP():
    with open('/home/pi/Documents/getIP/externalIP.txt') as f:
        lines = f.readlines()
        externalIP_tmp = lines.pop(0)
        externalIP = str(externalIP_tmp)
        print(externalIP)
        f.close()
        return externalIP


# run unix shell command, return as ASCII
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')

# get CPU temp
def getCPUTemperature():
    res = os.popen("vcgencmd measure_temp").readline()
    return(res.replace("temp=","").replace("'C\n",""))

# get CPU load
def getCPULoad():
    return str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())

# wipe LCD screen before we start
lcd.clear()

# before we start the main loop - detect active network device and ip address
sleep(2)
interface = find_interface()
ip_address = parse_ip()

while True:

    # get external ip
    externalIP = getExternalIP()

    # date and time
    lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n')
    
    #cpu temp and CPU load
    CPUTemperature = getCPUTemperature()
    CPULoad = getCPULoad()
    lcd_line_2  = "CPU:"+CPUTemperature+"C "+CPULoad+"%\n"
   
    # combine both lines into one update to the display
    lcd.message = lcd_line_1 + lcd_line_2

    sleep(2)
    lcd.clear()

    lcd_line_1 = "IP "+externalIP
    lcd_line_2 = "IP "+ip_address

    # combine both lines into one update to the display
    lcd.message = lcd_line_1 + lcd_line_2

    sleep(2)
    lcd.clear()

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
    

