from lolanalytics.datos.conexion import SessionLocal
from lolanalytics.datos.modelos import Jugador
from lolanalytics.ingesta.riot_client import RiotClient

TIERS = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND"]
DIVISIONES = ["I", "II", "III", "IV"]
PAGINAS = 1  # cada página trae cientos de jugadores por división

cliente = RiotClient()
nuevos = 0

with SessionLocal() as session:
    for tier in TIERS:
        for division in DIVISIONES:
            for pagina in range(1, PAGINAS + 1):
                entradas = cliente.entradas_liga(tier, division, pagina)
                agregados = 0
                for e in entradas:
                    puuid = e.get("puuid")
                    if not puuid:
                        continue
                    if session.get(Jugador, puuid):
                        continue
                    session.add(Jugador(puuid=puuid, tier=tier, division=division))
                    agregados += 1
                session.commit()
                nuevos += agregados
                print(f"{tier} {division} pág {pagina}: {agregados} jugadores nuevos")

print(f"Total de jugadores nuevos: {nuevos}")