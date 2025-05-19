import asyncio
from events.consumer import iniciar_consumidor

if __name__ == "__main__":
    asyncio.run(iniciar_consumidor())
