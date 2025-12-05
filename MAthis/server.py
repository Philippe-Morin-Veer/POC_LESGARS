import asyncio
import RPi.GPIO as GPIO
import copy
import logging
import time
from datetime import datetime, UTC
from math import sin

from asyncua import ua, uamethod, Server

_logger = logging.getLogger(__name__)


class SubHandler:
    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        _logger.warning("Python: New data change event %s %s", node, val)

    def event_notification(self, event):
        _logger.warning("Python: New event %s", event)


# method to be exposed through server
def func(parent, variant):
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]


# method to be exposed through server
# uses a decorator to automatically convert to and from variants
@uamethod
def multiply(parent, x, y):
    _logger.warning("multiply method call with parameters: %s %s", x, y)
    return x * y


async def main():
    server = Server()
    await server.init()
    # server.disable_clock()  #for debuging
    # server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://10.4.1.155:4840/freeopcua/server/")
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
    R = await dev.add_variable(idx, "R", False)
    await R.set_modelling_rule(True)
    await R.set_writable()
    G = await dev.add_variable(idx, "G", False)
    await G.set_modelling_rule(True)
    await G.set_writable()
    B = await dev.add_variable(idx, "B", False)
    await B.set_modelling_rule(True)
    await B.set_writable()
    await (await dev.add_property(idx, "device_id", "0340")).set_modelling_rule(True)
    ctrl = await dev.add_object(idx, "controller")
    await ctrl.set_modelling_rule(True)
    await (await ctrl.add_property(idx, "state", "Idle")).set_modelling_rule(True)

    # create directly some objects and variables
    LED1 = await server.nodes.objects.add_object(idx, "LED1", dev)
    LED1_var = await LED1.add_variable(idx, "State", False)
    await LED1_var.set_writable()  # Set LED1 to be writable by clients


    myevgen = await server.get_event_generator()
    myevgen.event.Severity = 300

    # starting!
    async with server:
        print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
        await myevgen.trigger(message="This is BaseEvent")
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(16, GPIO.IN)
        GPIO.setup(21, GPIO.IN)
        GPIO.setup(20, GPIO.IN)
        while True:
            await asyncio.sleep(0.1)
            LedR = await server.nodes.root.get_child(f"0:Objects/{idx}:LED1/{idx}:R")
            valueR = await LedR.read_value()
            LedG = await server.nodes.root.get_child(["0:Objects", f"{idx}:LED1", f"{idx}:G"])
            valueG = await LedG.read_value()
            LedB = await server.nodes.root.get_child(["0:Objects", f"{idx}:LED1", f"{idx}:B"])
            valueB = await LedB.read_value()
            if valueR==False:
                GPIO.setup(16, GPIO.IN)
            else:
                GPIO.setup(16, GPIO.OUT)
            if valueG==False:
                GPIO.setup(20, GPIO.IN)
            else:
                GPIO.setup(20, GPIO.OUT)
            if valueB==False:
                GPIO.setup(21, GPIO.IN)
            else:
                GPIO.setup(21, GPIO.OUT)
            


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)


    asyncio.run(main())