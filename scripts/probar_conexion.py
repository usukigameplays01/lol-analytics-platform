from lolanalytics.ingesta.riot_client import RiotClient

cliente = RiotClient()
cuenta = cliente.cuenta_por_riot_id("Usuki", "L01")  # cambia por tu Riot ID
print("PUUID:", cuenta["puuid"])

ids = cliente.ids_partidas(cuenta["puuid"], 5)
print("Últimas partidas:", ids)