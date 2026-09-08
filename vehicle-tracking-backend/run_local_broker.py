import asyncio
import logging
from amqtt.broker import Broker

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '127.0.0.1:1883',
        }
    },
    'sys_interval': 10,
    'auth': {
        'allow-anonymous': True,
        'plugins': ['auth_anonymous']
    }
}

async def start_broker():
    broker = Broker(config)
    await broker.start()
    print("Local MQTT Broker running on 127.0.0.1:1883 (TCP)")
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(start_broker())
    except KeyboardInterrupt:
        print("MQTT Broker stopped")
