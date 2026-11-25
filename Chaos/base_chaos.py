from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from typing import Any, Dict

JST = timezone(timedelta(hours=9))

class BaseChaos(ABC):
    """
    【零点・感覚器】
    外界の未整流な気配やテキストを吸収し、最初の揺らぎ（Seed）を感知する基底クラス。
    """
    def __init__(self, sanctuary_name: str = "Chaos"):
        self.sanctuary_name = sanctuary_name
        self.born_at = datetime.now(JST).isoformat()

    @abstractmethod
    def perceive(self, raw_input: Any) -> Dict[str, Any]:
        """
        外界からの入力を感覚器として受け取り、未整流の揺らぎデータへ変換する。
        """
        pass

    def emit_fluctuation(self, raw_input: Any) -> Dict[str, Any]:
        """
        感知した揺らぎに零点の位相メタデータを付与し、次の聖域（Entropy）へ託す。
        """
        fluctuation = self.perceive(raw_input)
        return {
            "origin": self.sanctuary_name,
            "timestamp": datetime.now(JST).isoformat(),
            "phase": "fluctuation",
            "payload": fluctuation,
        }
