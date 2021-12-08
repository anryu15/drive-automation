from src.websocket import Websocket
import RPi.GPIO as GPIO
import websockets
from src.config import IP_ADDR, PORT, SERVO_PIN, PWM, GPIO_PIN_1, GPIO_PIN_2, SERVER_LINK

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    Servo = GPIO.PWM(SERVO_PIN, PWM)
    Servo.start(0)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN_1, GPIO.OUT)
    GPIO.setup(GPIO_PIN_2, GPIO.OUT)
    GPIO.output(GPIO_PIN_1, GPIO.LOW)
    GPIO.output(GPIO_PIN_2, GPIO.LOW)

    ws_server = Websocket(PORT, IP_ADDR, Servo, GPIO_PIN_1, GPIO_PIN_2, SERVER_LINK)
    ws_server.run()