"""
Configuração centralizada da aplicação.

Lê variáveis de ambiente e define valores por omissão.
"""
from __future__ import annotations
import os


class Config:
    # Base da API do Smart Campus Core
    API_BASE: str = os.getenv("API_BASE", "http://localhost:5000")

    # Endpoint de espaços (suporta nomes antigos e novos)
    API_SPACES_ENDPOINT: str = (
        os.getenv("API_SPACES_ENDPOINT")
        or os.getenv("API_ROOMS_ENDPOINT")
        or "/api/spaces"
    )

    # Fuso horário (opcional, já é tratado a nível de container)
    TZ: str = os.getenv("TZ", "Europe/Lisbon")


config = Config()
