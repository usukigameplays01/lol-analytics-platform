import time
import requests
from lolanalytics import config


class RiotClient:
    def __init__(self, region: str = config.REGION):
        self.base = f"https://{region}.api.riotgames.com"
        self.session = requests.Session()
        self.session.headers.update({"X-Riot-Token": config.RIOT_API_KEY})

    def _get(self, path: str, params: dict | None = None, reintentos: int = 3):
        url = self.base + path
        for _ in range(reintentos):
            resp = self.session.get(url, params=params, timeout=15)
            if resp.status_code == 429:  # límite de peticiones
                espera = int(resp.headers.get("Retry-After", 2))
                time.sleep(espera)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError(f"Se agotaron los reintentos para {path}")

    def cuenta_por_riot_id(self, nombre: str, tag: str) -> dict:
        return self._get(f"/riot/account/v1/accounts/by-riot-id/{nombre}/{tag}")

    def ids_partidas(self, puuid: str, cantidad: int = 20) -> list[str]:
        return self._get(
            f"/lol/match/v5/matches/by-puuid/{puuid}/ids", {"count": cantidad}
        )

    def partida(self, match_id: str) -> dict:
        return self._get(f"/lol/match/v5/matches/{match_id}")

    def timeline(self, match_id: str) -> dict:
        return self._get(f"/lol/match/v5/matches/{match_id}/timeline")