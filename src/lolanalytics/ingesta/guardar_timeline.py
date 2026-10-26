from lolanalytics.datos.modelos import Evento, FrameParticipante

TIPOS_EVENTO = {"CHAMPION_KILL", "ELITE_MONSTER_KILL", "BUILDING_KILL"}


def equipo_de(participant_id: int) -> int:
    """Los participantes 1-5 son del equipo 100 y 6-10 del equipo 200."""
    return 100 if participant_id <= 5 else 200


def guardar_timeline(session, match_id: str, datos: dict) -> int:
    """Guarda frames y eventos clave de una timeline. Devuelve los frames guardados."""
    total = 0
    for frame in datos["info"]["frames"]:
        ts = frame["timestamp"]

        for pid_str, pf in frame["participantFrames"].items():
            pid = int(pid_str)
            session.add(
                FrameParticipante(
                    match_id=match_id,
                    timestamp_ms=ts,
                    minuto=ts // 60000,
                    participant_id=pid,
                    equipo=equipo_de(pid),
                    oro_total=pf["totalGold"],
                    xp=pf["xp"],
                    nivel=pf["level"],
                    minions=pf["minionsKilled"] + pf["jungleMinionsKilled"],
                    dano_campeones=pf["damageStats"]["totalDamageDoneToChampions"],
                )
            )
            total += 1

        for ev in frame.get("events", []):
            tipo = ev["type"]
            if tipo not in TIPOS_EVENTO:
                continue

            if tipo == "CHAMPION_KILL":
                # El equipo que consigue la muerte es el contrario al de la víctima
                equipo = 300 - equipo_de(ev["victimId"])
                detalle = ""
            elif tipo == "ELITE_MONSTER_KILL":
                equipo = ev["killerTeamId"]
                detalle = ev.get("monsterSubType") or ev["monsterType"]
            else:  # BUILDING_KILL: teamId es el dueño de la estructura destruida
                equipo = 300 - ev["teamId"]
                detalle = ev.get("towerType") or ev["buildingType"]

            session.add(
                Evento(
                    match_id=match_id,
                    timestamp_ms=ev["timestamp"],
                    minuto=ev["timestamp"] // 60000,
                    tipo=tipo,
                    equipo=equipo,
                    detalle=detalle,
                )
            )
    return total