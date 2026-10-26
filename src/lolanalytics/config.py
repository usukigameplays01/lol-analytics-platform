import os
from dotenv import load_dotenv

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Ruteo regional de Riot: las cuentas de LAN/LAS/NA/BR usan "americas"
REGION = "americas"

if not RIOT_API_KEY:
    raise RuntimeError("Falta RIOT_API_KEY en el archivo .env")