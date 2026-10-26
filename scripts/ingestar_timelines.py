import time

from sqlalchemy import select

from lolanalytics.datos.conexion import SessionLocal
from lolanalytics.datos.modelos import FrameParticipante, Partida
from lolanalytics.ingesta.guardar_timeline import guardar_timeline
from lolanalytics.ingesta.riot_client import RiotClient

cliente = RiotClient()
guardadas = 0

with SessionLocal() as session:
    con_frames = select(FrameParticipante.match_id).distinct()
    pendientes = session.scalars(
        select(Partida.match_id).where(Partida.match_id.not_in(con_frames))
    ).all()
    print(f"Partidas sin timeline: {len(pendientes)}")

    for match_id in pendientes:
        datos = cliente.timeline(match_id)
        filas = guardar_timeline(session, match_id, datos)
        session.commit()
        guardadas += 1
        print(f"[{guardadas}/{len(pendientes)}] {match_id}: {filas} frames")
        time.sleep(1.3)  # respeta el límite de 100 peticiones cada 2 minutos

print("Listo")