import RPi.GPIO as GPIO
import cv2
import time
import asyncio
import websockets
from websocket_server import WebsocketServer
import logging
from .utils import capture_camera
from .config import IMAGE_DIR

class Websocket():
    def __init__(self, host, port, servo, pin_1, pin_2, server_link):
        self.server = WebsocketServer(port, host, loglevel=logging.DEBUG)
        self.servo = servo
        self.pin_1 = pin_1
        self.pin_2 = pin_2
        self.server_link = server_link
    def new_client(self, client, server):
        print("new client connected and was given id {}".format(client['id']))
        self.server.send_message_to_all("hey all, a new client has joined us")
        
    def client_left(self, client, server):
        print("client({}) disconnected".format(client['id']))

    def message_received(self, client, server, message):
        print("client({}) said: {}".format(client['id'], message))
        order = message.split()
        pin_1_input = None
        pin_2_input = None
        if order[0] == "e":
            pin_1_input = GPIO.HIGH
            pin_2_input = GPIO.LOW
        if order[0] == "d":
            pin_1_input = GPIO.LOW
            pin_2_input = GPIO.HIGH
        if order[0] == "q":
            pin_1_input = GPIO.LOW
            pin_2_input = GPIO.LOW
            order.append(0)
        GPIO.output(self.pin_1, pin_1_input)
        GPIO.output(self.pin_2, pin_2_input)
        self._servo_angle(int(order[1]))
        self._send_image()
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._send_image())
        self.server.send_message_to_all(message)

    def run(self):
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received) 
        self.server.run_forever()

    def _servo_angle(self, angle):
        duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180
        self.servo.ChangeDutyCycle(duty)
        time.sleep(0.3)

    async def _send_image(self):
        async with websockets.connect(self.server_link) as websocket:
            capture_camera(name="0")
            with open(f"{IMAGE_DIR}/0.jpg", "rb") as f:
                data = f.read()
                await websocket.send(data)
                


