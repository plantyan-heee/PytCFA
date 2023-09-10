from pmk import PMK
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
import time
import random
import usb_hid
from adafruit_hid.keycode import Keycode

keypico = PMK(Hardware())
keys = keypico.keys

button_pressed = False

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], 
                          out_channel=0)

# Colour selection
snow = (0, 0, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
purple = (255, 0, 255)

# Set key colours for all keys
keypico.set_all(*snow)

# Orientation
# keypico.set_led(0, *red)
# keypico.set_led(3, *green)
# keypico.set_led(12, *blue)
# keypico.set_led(15, *purple)

# Set sleep time
keypico.led_sleep_enabled = True
keypico.led_sleep_time = 10

# Midi

start_note = 38
velocity = 125

# Loop

for key in keys:
    @keypico.on_press(key)
    def press_handler(key):
        # print("Key {} pressed with colour blue".format(key.number))
        key.set_led(*blue)
        button_pressed = False
        note = start_note + key.number
        midi.send(NoteOn(note, velocity))


    @keypico.on_release(key)
    def release_handler(key):
        # print("Key {} released with colour snow".format(key.number))
        if key.rgb == [255, 0, 0]:
            key.set_led(*green)
            button_pressed = False
        else:
            key.set_led(*snow)
            button_pressed = False
        note = start_note + key.number
        midi.send(NoteOff(note, 0))

    @keypico.on_hold(key)
    def hold_handler(key):
        # print("Key {} held with colour green".format(key.number))
        key.set_led(*green)
        button_pressed = True
        
        if key.number == 0:
            if button_pressed == True:
                key.set_led(*red)
                print("   ")
                current_time = time.localtime()
                gmt_plus_8_time = time.mktime(current_time) + 8 * 3600
                gmt_plus_8_struct_time = time.localtime(gmt_plus_8_time)
                time_str = "{:02d}:{:02d}:{:02d}".format(gmt_plus_8_struct_time.tm_hour, gmt_plus_8_struct_time.tm_min, gmt_plus_8_struct_time.tm_sec)
                hr = random.randint(50,120)
                print(time_str)
                for i in range (10):
                    time.sleep(0.5)
                    hr1 = random.randint(-5,5)
                    hr = hr + hr1
                    print("Heart rate:", hr)
                    
        if key.number == 15:
            user = 1
            if button_pressed == True:
                if user == 1:
                    user = user + 1
                    print("User switched to user 2")
                    print("   ")
                    weight1 = float(input("Weight for User 1 in kg: "))
                    height1 = float(input("Height for User 1 in m: "))
                if user == 2:
                    user = user - 1
                    print("User switched to user 1")
                    print("   ")
                    weight2 = float(input("Weight for User 2 in kg: "))
                    height2 = float(input("Height for User 2 in m: "))

while True:
    keypico.update()