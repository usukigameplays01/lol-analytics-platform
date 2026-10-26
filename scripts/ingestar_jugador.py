import time

from lolanalytics.datos.conexion import SessionLocal
from lolanalytics.datos.modelos import Partida
from lolanalytics.ingesta.guardar import guardar_partida
from lolanalytics.ingesta.riot_client import RiotClient

NOMBRE, TAG = "Usuki", "L01"
cliente = RiotClient()
puuid = cliente.cuenta_por_riot_id(NOMBRE, TAG)["puuid"]
ids = cliente.ids_partidas(puuid, 20)

nuevas = 0
with SessionLocal() as session:
    for match_id in ids:
        if session.get(Partida, match_id):
            continue
        datos = cliente.partida(match_id)
        if guardar_partida(session, datos):
            nuevas += 1
        session.commit()
        time.sleep(1.3)  # respeta el límite de 100 peticiones cada 2 minutos

print(f"Partidas nuevas guardadas: {nuevas}")