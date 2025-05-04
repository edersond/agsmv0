import os
from datetime import datetime, timedelta, timezone

__all__ = ["APP_GLOBALS", "TempoJogo"]

class APP_GLOBALS:
    """
    APP GLOBALS
    """
    APP_NAME = "AGIOTA SIMULATOR"
    APP_VERSION = "0.0.0"
    APP_DESCRIPTION = "AGIOTA SIMULATOR"
    
    class APP_DIRS:
        LIBS = os.path.join(os.getcwd(), "libs")
        LOGS = os.path.join(os.getcwd(), "logs")
        MEDIA = os.path.join(os.getcwd(), "media")
        MIDDLEWARE = os.path.join(os.getcwd(), "middleware")
        ROUTES = os.path.join(os.getcwd(), "routes")
        SRC = os.path.join(os.getcwd(), "src")
        STATIC = os.path.join(os.getcwd(), "static")
        TEMPLATES = os.path.join(os.getcwd(), "templates")
        TMP = os.path.join(os.getcwd(), "tmp")
        

class TempoJogo:
    """
    Converte entre tempo real e tempo do jogo.
    - 1 dia do jogo = 5 minutos reais
    - Dia 0, 00:00 do jogo = 1/1/2025 00:00 GMT-3
    """
    FATOR_ESCALA = 288  # 1440 min/dia ÷ 5 min/dia de jogo
    ORIGEM_JOGO = datetime(2025, 1, 1, 3, 0, 0, tzinfo=timezone.utc)  # GMT-3 em UTC

    @classmethod
    def agora_jogo(cls) -> tuple[int, int, int]:
        """Retorna tempo atual do jogo: (dia, hora, minuto)."""
        agora = datetime.now(timezone.utc)
        delta = agora - cls.ORIGEM_JOGO
        segundos_jogo = delta.total_seconds() * cls.FATOR_ESCALA
        dias = int(segundos_jogo // 86400)
        horas = int((segundos_jogo % 86400) // 3600)
        minutos = int((segundos_jogo % 3600) // 60)
        return dias, horas, minutos

    @classmethod
    def jogo_para_real(cls, dia: int, hora: int, minuto: int) -> datetime:
        """Converte dia/hora/minuto do jogo para datetime real (UTC)."""
        segundos_jogo = ((dia * 24 + hora) * 60 + minuto) * 60
        segundos_reais = segundos_jogo / cls.FATOR_ESCALA
        return cls.ORIGEM_JOGO + timedelta(seconds=segundos_reais)

    @classmethod
    def real_para_jogo(cls, dt: datetime) -> tuple[int, int, int]:
        """Converte datetime real (UTC) para tempo do jogo (dia, hora, minuto)."""
        delta = dt.astimezone(timezone.utc) - cls.ORIGEM_JOGO
        segundos_jogo = delta.total_seconds() * cls.FATOR_ESCALA
        dias = int(segundos_jogo // 86400)
        horas = int((segundos_jogo % 86400) // 3600)
        minutos = int((segundos_jogo % 3600) // 60)
        return dias, horas, minutos

