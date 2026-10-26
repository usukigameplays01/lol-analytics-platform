from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String
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