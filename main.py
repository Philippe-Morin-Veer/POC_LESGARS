import RPi.GPIO as GPIO
import time

LED1 = 15  # LED verte
LED2 = 14  # LED rouge
BUTTON = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        if GPIO.input(BUTTON) == GPIO.HIGH:  # Bouton appuyé
            GPIO.output(LED1, GPIO.HIGH)   # Allume LED verte
            GPIO.output(LED2, GPIO.LOW)    # Éteint LED rouge
        else:
            GPIO.output(LED1, GPIO.LOW)    # Éteint LED verte
            GPIO.output(LED2, GPIO.HIGH)   # Allume LED rouge
        time.sleep(0.05)  # Petite pause pour éviter la surcharge CPU
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()