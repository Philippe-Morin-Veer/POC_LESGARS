import RPi.GPIO as GPIO
import time

# Définir les numéros des broches BCM
BUTTON_PIN = 12      # Broche du bouton
LED_GREEN_PIN = 15   # Broche de la LED verte
LED_RED_PIN = 14     # Broche de la LED rouge

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Bouton avec résistance pull-up
GPIO.setup(LED_GREEN_PIN, GPIO.OUT)
GPIO.setup(LED_RED_PIN, GPIO.OUT)

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:  # Bouton appuyé
            print("Bouton appuyé")
            GPIO.output(LED_GREEN_PIN, GPIO.HIGH)  # Allume la LED verte
            GPIO.output(LED_RED_PIN, GPIO.LOW)     # Éteint la LED rouge
        else: # Bouton relâché
            print("Bouton relâché")
            GPIO.output(LED_GREEN_PIN, GPIO.LOW)   # Éteint la LED verte
            GPIO.output(LED_RED_PIN, GPIO.HIGH)    # Allume la LED rouge
        time.sleep(0.05)  # Petite pause pour éviter le rebond
finally:
    GPIO.cleanup()