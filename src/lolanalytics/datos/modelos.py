from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Partida(Base):
    __tablename__ = "partidas"

    match_id: Mapped[str] = mapped_column(String, primary_key=True)
    queue_id: Mapped[int] = mapped_column(Integer)
    game_mode: Mapped[str] = mapped_column(String)
    game_version: Mapped[str] = mapped_column(String)
    duracion_seg: Mapped[int] = mapped_column(Integer)
    creada_ms: Mapped[int] = mapped_column(BigInteger)

    participantes: Mapped[list["Participante"]] = relationship(
        back_populates="partida", cascade="all, delete-orphan"
    )


class Participante(Base):
    __tablename__ = "participantes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[str] = mapped_column(ForeignKey("partidas.match_id"), index=True)
    puuid: Mapped[str] = mapped_column(String, index=True)
    campeon: Mapped[str] = mapped_column(String)
    equipo: Mapped[int] = mapped_column(Integer)
    posicion: Mapped[str] = mapped_column(String)
    victoria: Mapped[bool] = mapped_column(Boolean)
    kills: Mapped[int] = mapped_column(Integer)
    muertes: Mapped[int] = mapped_column(Integer)
    asistencias: Mapped[int] = mapped_column(Integer)
    oro: Mapped[int] = mapped_column(Integer)
    dano_campeones: Mapped[int] = mapped_column(Integer)
    vision: Mapped[int] = mapped_column(Integer)
    minions: Mapped[int] = mapped_column(Integer)

    partida: Mapped["Partida"] = relationship(back_populates="participantes")


class FrameParticipante(Base):
    __tablename__ = "frames_participante"
    __table_args__ = (
        UniqueConstraint("match_id", "timestamp_ms", "participant_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[str] = mapped_column(ForeignKey("partidas.match_id"), index=True)
    timestamp_ms: Mapped[int] = mapped_column(Integer)
    minuto: Mapped[int] = mapped_column(Integer)
    participant_id: Mapped[int] = mapped_column(Integer)
    equipo: Mapped[int] = mapped_column(Integer)
    oro_total: Mapped[int] = mapped_column(Integer)
    xp: Mapped[int] = mapped_column(Integer)
    nivel: Mapped[int] = mapped_column(Integer)
    minions: Mapped[int] = mapped_column(Integer)
    dano_campeones: Mapped[int] = mapped_column(Integer)


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[str] = mapped_column(ForeignKey("partidas.match_id"), index=True)
    timestamp_ms: Mapped[int] = mapped_column(BigInteger)
    minuto: Mapped[int] = mapped_column(Integer)
    tipo: Mapped[str] = mapped_column(String)
    equipo: Mapped[int] = mapped_column(Integer)
    detalle: Mapped[str] = mapped_column(String)

class Jugador(Base):
    __tablename__ = "jugadores"

    puuid: Mapped[str] = mapped_column(String, primary_key=True)
    tier: Mapped[str] = mapped_column(String)
    division: Mapped[str] = mapped_column(String)
    procesado: Mapped[bool] = mapped_column(Boolean, default=False)