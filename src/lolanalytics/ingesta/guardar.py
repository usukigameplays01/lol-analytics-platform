from lolanalytics.datos.modelos import Partida, Participante


def guardar_partida(session, datos: dict) -> bool:
    """Guarda una partida de MATCH-V5. Devuelve False si ya existía."""
    match_id = datos["metadata"]["matchId"]
    if session.get(Partida, match_id):
        return False

    info = datos["info"]
    partida = Partida(
        match_id=match_id,
        queue_id=info["queueId"],
        game_mode=info["gameMode"],
        game_version=info["gameVersion"],
        duracion_seg=info["gameDuration"],
        creada_ms=info["gameCreation"],
    )
    for p in info["participants"]:
        partida.participantes.append(
            Participante(
                puuid=p["puuid"],
                campeon=p["championName"],
                equipo=p["teamId"],
                posicion=p.get("teamPosition", ""),
                victoria=p["win"],
                kills=p["kills"],
                muertes=p["deaths"],
                asistencias=p["assists"],
                oro=p["goldEarned"],
                dano_campeones=p["totalDamageDealtToChampions"],
                vision=p["visionScore"],
                minions=p["totalMinionsKilled"] + p["neutralMinionsKilled"],
            )
        )
    session.add(partida)
    return True