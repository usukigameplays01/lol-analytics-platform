import requests
from sqlalchemy import func, select

from lolanalytics.datos.conexion import SessionLocal
from lolanalytics.datos.modelos import Jugador, Partida
from lolanalytics.ingesta.guardar import guardar_partida
from lolanalytics.ingesta.guardar_timeline import guardar_timeline
from lolanalytics.ingesta.riot_client import RiotClient

QUEUE_SOLO_DUO = 420
PARTIDAS_POR_JUGADOR = 20
DURACION_MINIMA_SEG = 300  # descarta remakes

cliente = RiotClient()

with SessionLocal() as session:
    while True:
        jugador = session.scalars(
            select(Jugador).where(Jugador.procesado.is_(False)).limit(1)
        ).first()
        if jugador is None:
            print("No quedan jugadores pendientes. Ejecuta muestrear_jugadores.py")
            break

        try:
            ids = cliente.ids_partidas(
                jugador.puuid, PARTIDAS_POR_JUGADOR, queue=QUEUE_SOLO_DUO
            )
        except requests.HTTPError as e:
            if e.response.status_code in (401, 403):
                raise  # clave inválida: no tiene sentido seguir
            print(f"Jugador omitido ({e.response.status_code})")
            jugador.procesado = True
            session.commit()
            continue

        nuevas = 0
        for match_id in ids:
            if session.get(Partida, match_id):
                continue
            try:
                datos = cliente.partida(match_id)
                if datos["info"]["gameDuration"] < DURACION_MINIMA_SEG:
                    continue
                guardar_partida(session, datos)
                session.commit()
                guardar_timeline(session, match_id, cliente.timeline(match_id))
                session.commit()
                nuevas += 1
            except requests.HTTPError as e:
                session.rollback()
                if e.response.status_code in (401, 403):
                    raise
                print(f"  {match_id} omitida ({e.response.status_code})")

        jugador.procesado = True
        session.commit()

        total = session.scalar(select(func.count()).select_from(Partida))
        pendientes = session.scalar(
            select(func.count()).select_from(Jugador).where(Jugador.procesado.is_(False))
        )
        print(f"{jugador.tier} {jugador.division}: +{nuevas} partidas | "
              f"total {total} | jugadores pendientes {pendientes}")