import time

import requests

from lolanalytics import config

PLATAFORMA = "la1"  # LAN. Si tu cuenta es de LAS, usa "la2"
PAUSA_ENTRE_PETICIONES = 1.25  # límite: 100 peticiones cada 2 minutos


class RiotClient:
    def __init__(self, region: str = config.REGION, plataforma: str = PLATAFORMA):
        self.base = f"https://{region}.api.riotgames.com"
        self.base_plataforma = f"https://{plataforma}.api.riotgames.com"
        self.session = requests.Session()
        self.session.headers.update({"X-Riot-Token": config.RIOT_API_KEY})
        self._ultima = 0.0

    def _esperar(self):
        faltan = PAUSA_ENTRE_PETICIONES - (time.monotonic() - self._ultima)
        if faltan > 0:
            time.sleep(faltan)
        self._ultima = time.monotonic()

    def _get(self, path: str, params: dict | None = None,
             reintentos: int = 3, base: str | None = None):
        url = (base or self.base) + path
        for _ in range(reintentos):
            self._esperar()
            resp = self.session.get(url, params=params, timeout=15)
            if resp.status_code == 429:  # límite de peticiones
                time.sleep(int(resp.headers.get("Retry-After", 2)))
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError(f"Se agotaron los reintentos para {path}")

    def cuenta_por_riot_id(self, nombre: str, tag: str) -> dict:
        return self._get(f"/riot/account/v1/accounts/by-riot-id/{nombre}/{tag}")

    def ids_partidas(self, puuid: str, cantidad: int = 20,
                     queue: int | None = None) -> list[str]:
        params = {"count": cantidad}
        if queue is not None:
            params["queue"] = queue
        return self._get(f"/lol/match/v5/matches/by-puuid/{puuid}/ids", params)

    def partida(self, match_id: str) -> dict:
        return self._get(f"/lol/match/v5/matches/{match_id}")

    def timeline(self, match_id: str) -> dict:
        return self._get(f"/lol/match/v5/matches/{match_id}/timeline")

    def entradas_liga(self, tier: str, division: str, pagina: int = 1,
                      queue: str = "RANKED_SOLO_5x5") -> list[dict]:
        return self._get(
            f"/lol/league/v4/entries/{queue}/{tier}/{division}",
            {"page": pagina},
            base=self.base_plataforma,
        )