import RPi.GPIO as GPIO
import asyncio
import copy
import logging
import time
from datetime import datetime, UTC
from math import sin

from asyncua import ua, uamethod, Server

_logger = logging.getLogger(__name__)

Led_bluePin = 21
Led_greenPin = 20
Led_redPin = 16

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Led_bluePin, GPIO.OUT)
GPIO.setup(Led_greenPin, GPIO.OUT)
GPIO.setup(Led_redPin, GPIO.OUT)



class SubHandler:


    def datachange_notification(self, node, val, data):
        _logger.warning("Python: New data change event %s %s", node, val)

    def event_notification(self, event):
        _logger.warning("Python: New event %s", event)


# method to be exposed through server
def func(parent):
    parent.get_child("2:Close").set_value(False)
    #faire sa avec les 3 noeuds des leds
    


# method to be exposed through server
# uses a decorator to automatically convert to and from variants
"""
@uamethod

def multiply(parent, x, y):
    _logger.warning("multiply method call with parameters: %s %s", x, y)
    return x * y
"""

async def main():
    server = Server()
    await server.init()
    # server.disable_clock()  #for debuging
    # server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("FreeOpcUa Example Server")
    # set all possible endpoint policies for clients to connect through
    server.set_security_policy(
        [
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign,
        ]
    )

    # set up our own namespace
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # create a new node type we can instantiate in our address space
    dev = await server.nodes.base_object_type.add_object_type(idx, "MyDevice")
    await (await dev.add_variable(idx, "sensor1", 1.0)).set_modelling_rule(True)
    await (await dev.add_property(idx, "device_id", "0340")).set_modelling_rule(True)
    ctrl = await dev.add_object(idx, "controller")
    await ctrl.set_modelling_rule(True)
    await (await ctrl.add_property(idx, "state", "Idle")).set_modelling_rule(True)


    # instanciate one instance of our device
    """ mydevice = await server.nodes.objects.add_object(idx, "Device0001", dev)
    mydevice_var = await mydevice.get_child(
        [f"{idx}:controller", f"{idx}:state"]
    )  # get proxy to our device state variable
    # create directly some objects and variables
    """
    led1 = await server.nodes.objects.add_object(idx, "LED1")
    red = await led1.add_variable(idx, "Red", False)
    await red.set_writable()  # Set MyVariable to be writable by clients
    green = await led1.add_variable(idx, "Green", False)
    await green.set_writable()  # Set MyVariable to be writable by clients
    blue = await led1.add_variable(idx, "Blue", False)
    await blue.set_writable()  # Set MyVariable to be writable by clients

   
    close = await led1.add_method(idx, "Close", func, [])
   

    # starting!
    async with server:
        print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
        # enable following if you want to subscribe to nodes on server side
        # handler = SubHandler()
        # sub = await server.create_subscription(500, handler)
        # handle = await sub.subscribe_data_change(myvar)
        # trigger event, all subscribed clients wil receive it
        """var = await myarrayvar.read_value()  # return a ref to value in db server side! not a copy!
        var = copy.copy(
            var
        )  # WARNING: we need to copy before writting again otherwise no data change event will be generated
        var.append(9.3)
        await myarrayvar.write_value(var)
        await mydevice_var.write_value("Running")
        await myevgen.trigger(message="This is BaseEvent")
        # write_attribute_value is a server side method which is faster than using write_value
        # but than methods has less checks
        await server.write_attribute_value(myvar.nodeid, ua.DataValue(0.9))
        """
        try:
            while True:
                await asyncio.sleep(0.1)
                # Lire les noeuds
                red_val = await red.read_value()
                green_val = await green.read_value()
                blue_val = await blue.read_value()
                #close_meth = await close.call_method()
                #activer les GPIO
                
                if red_val:
                    GPIO.output(Led_redPin, GPIO.LOW)
                else:
                    GPIO.output(Led_redPin, GPIO.HIGH)
                if green_val:
                    GPIO.output(Led_greenPin, GPIO.LOW)
                else:
                    GPIO.output(Led_greenPin, GPIO.HIGH)
                if blue_val:
                    GPIO.output(Led_bluePin, GPIO.LOW)
                else: 
                    GPIO.output(Led_bluePin, GPIO.HIGH)
                
                
        finally:
            GPIO.cleanup()

       
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # optional: setup logging
    # logger = logging.getLogger("asyncua.address_space")
    # logger.setLevel(logging.DEBUG)
    # logger = logging.getLogger("asyncua.internal_server")
    # logger.setLevel(logging.DEBUG)
    # logger = logging.getLogger("asyncua.binary_server_asyncio")
    # logger.setLevel(logging.DEBUG)
    # logger = logging.getLogger("asyncua.uaprocessor")
    # logger.setLevel(logging.DEBUG)

    asyncio.run(main())