from gpiozero import LED, Button
import time
import pyttsx3
import os

# Variables
count = 0
delay1 = 0.1
delay2 = 2
pin_index = 0  # Start with the first LED in the list
green_pin = 27
yellow_pin = 17
sounds_dir = '/home/eastonli/buzzer_game/sounds'

# Setup LEDs and buttons
led_pins = [4, 5, 6, 13, 19, 26]
leds = [LED(pin) for pin in led_pins]
green_button = Button(green_pin, pull_up=True)
yellow_button = Button(yellow_pin, pull_up=True)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to reset LEDs
def reset_led():
    for led in leds:
        led.off()

# Function to turn on LED
def turn_on_led():
    global pin_index
    if pin_index < len(leds):
        leds[pin_index].on()
        pin_index += 1

# Function to play sound
def play_sound(file_name):
    os.system(f"aplay {sounds_dir}/{file_name}.wav")

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize the script
reset_led()
play_sound("Gong")

def check_yellow():
    global count, pin_index
    if yellow_button.is_pressed:
        play_sound("zoop")
        turn_on_led()
        speak("careful")
        count += 1
        time.sleep(delay1)

        if count == 3:
            for _ in range(3):
                play_sound("Alien_Creak1")
            speak(f"You lose! Game will start in {delay2} seconds")
            time.sleep(delay2)
            count = 0
            reset_led()
            pin_index = 0  # Reset pin index for new game
            play_sound("Gong")

def check_green():
    global count, pin_index
    if green_button.is_pressed:
        leds[3].on()
        leds[4].on()
        leds[5].on()
        play_sound("dance_around")
        speak(f"You win! Game will restart in {delay2} seconds")
        time.sleep(delay2)
        count = 0
        reset_led()
        pin_index = 0  # Reset pin index for new game
        play_sound("Gong")

# Main loop
while True:
    check_yellow()
    check_green()