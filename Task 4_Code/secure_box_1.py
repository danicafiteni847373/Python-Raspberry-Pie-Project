import RPi.GPIO as GPIO
import time
from pad4pi import rpi_gpio
from gpiozero import LED
from time import sleep
import smtplib
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

led = LED(4)
lock_pin = 16

GPIO.setmode(GPIO.BCM)



buzzer = 3
GPIO.setup(buzzer, GPIO.OUT)

#******************************************#
KEYPAD = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"]
]


COL_PINS = [26,20,21] # BCM numbering
ROW_PINS = [5, 6,13,19] # BCM numbering

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)


    

#******************************************#


def printKey(key):
    lcd_byte(ord(key),LCD_CHR)
    if key == "#":
        lcd_string(" Correct Pin :) ",LCD_LINE_1)
        time.sleep(1)
        lcd_string("    Unlocked", LCD_LINE_2)
        lcd_byte(0xC0, LCD_CMD)
        led.on()

        
        
        
        
        #email alert
        gmail_user = "danfit784@gmail.com"
        gmail_password = "tssphpbqjnfschti"

        
        sent_from = gmail_user
        to = ["danicafiteni@gmail.com"]
        subject = 'OMG Super Important Message'
        body = 'Hey, your secure box is unlocked :). Well Done.'


        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()

            print( 'Email sent!')
        except:
            print('Something went wrong...Email not sent')



        
        time.sleep(10)
        led.off()


        
        lcd_string("  ",LCD_LINE_1)
        lcd_string("  ",LCD_LINE_2)


        print("Unlocking")
        GPIO.setup(lock_pin, GPIO.OUT)
        GPIO.output(lock_pin, GPIO.HIGH)      

        
    else:
        lcd_string("Incorrect Pin :) ",LCD_LINE_1)
        lcd_string("  Try again ", LCD_LINE_2)
        led.off()

        

        
        GPIO.output(buzzer, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(buzzer, GPIO.LOW)
        sleep(0.5)
     
    
        lcd_string("Enter your pin :", LCD_LINE_1)
        lcd_string(" ", LCD_LINE_2
                   )
        lcd_byte(0xC0, LCD_CMD)

        GPIO.setup(lock_pin, GPIO.OUT)
        GPIO.output(lock_pin, GPIO.LOW)
        GPIO.cleanup(lock_pin)
        print("Lock stay locked")


#******************************************#

# printKey will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(printKey)




# Define GPIO to LCD mapping
LCD_RS = 25
LCD_E  = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 18
LCD_D7 = 22



# Define LCD parameters
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


#******************************************#
def main():
  # Main program block
  global pm
  global system_sts
  
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7


  # Initialise display
  lcd_init()
  lcd_byte(0x01, LCD_CMD)
  lcd_string("Enter your pin : ",LCD_LINE_1)
  lcd_byte(0xC0, LCD_CMD)
  while True:
      time.sleep(1)

      
#******************************************#  
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

#******************************************#
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

#******************************************#
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

#***************************************#


def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")
 
  

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)


  

#******************************************#



if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1) #CTRL + C
    
    GPIO.cleanup()
