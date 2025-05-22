# import asyncio
# from app.events.consumer import iniciar_consumidor

from app.services.persistencia import to_utc_datetime


if __name__ == "__main__":
    # asyncio.run(iniciar_consumidor())
    # fecha = '2025-05-13 20:00:00.000 -05:00'
    fecha = '2025-05-13T20:01:00'
    print(fecha)
    dt = to_utc_datetime(fecha)
    print(dt)