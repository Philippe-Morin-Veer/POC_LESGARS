import asyncio
import logging

from asyncua import Client

_logger = logging.getLogger(__name__)


class SubHandler:
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("New data change event", node, val)

    def event_notification(self, event):
        print("New event", event)


async def main():
    url = "opc.tcp://10.4.1.155:4840/freeopcua/server/"
    async with Client(url=url) as client:
        idx = await client.get_namespace_index("http://examples.freeopcua.github.io")


        LedR=False
        LedB=False
        LedG=False
        NodeR = await client.nodes.root.get_child(["0:Objects", f"{idx}:LED1", f"{idx}:R"])
        NodeG = await client.nodes.root.get_child(["0:Objects", f"{idx}:LED1", f"{idx}:G"])
        NodeB = await client.nodes.root.get_child(["0:Objects", f"{idx}:LED1", f"{idx}:B"])

        while True:
            lumiere= input("Entrez une couleur de lumiere (r, g, b) ou bien si vous voulez fermer le programme, appuyez sur Entrée: ")
            if lumiere=="r":
                if LedR==False:
                    await NodeR.write_value(True)
                    LedR=True
                else:
                    await NodeR.write_value(False)
                    LedR=False
            elif lumiere=="g":
                if LedG==False:
                    await NodeG.write_value(True)
                    LedG=True
                else:
                    await NodeG.write_value(False)
                    LedG=False
            elif lumiere=="b":
                if LedB==False:
                    await NodeB.write_value(True)
                    LedB=True
                else:
                    await NodeB.write_value(False)
                    LedB=False
            elif lumiere=="":
                await NodeR.write_value(False)
                await NodeG.write_value(False)
                await NodeB.write_value(False)
                break
            else:
                print("Vous n'avez pas choisi un type de lumiere valide")
            await asyncio.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())