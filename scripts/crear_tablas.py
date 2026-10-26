from lolanalytics.datos.conexion import engine
from lolanalytics.datos.modelos import Base

Base.metadata.create_all(engine)
print("Tablas creadas")
