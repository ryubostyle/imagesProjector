from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Tuple

JST = timezone(timedelta(hours=9))


class ErrorTrapper:
    """[破骨細胞] 揺らぎの中に混入したノイズ・不純物を検知し、安全な隔離パケットへ変換する"""

    def __init__(self, sanctuary_name: str = "Entropy") -> None:
        self.sanctuary_name = sanctuary_name

    def isolate(self, error: Exception, raw_packet: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "origin": self.sanctuary_name,
            "phase": "quarantined",
            "quarantined_at": datetime.now(JST).isoformat(),
            "report": {
                "error_type": type(error).__name__,
                "message": str(error),
                "source_origin": raw_packet.get("origin", "Unknown"),
            },
        }


class BaseEntropy(ABC):
    """[Level 1: 神経・整流器] 混沌からの揺らぎを浄化し、カスケード構造（ワイヤーフレーム）へと整流する基底クラス"""

    def __init__(
        self,
        sanctuary_name: str = "Entropy",
        wireframes_dir: str = "Entropy/wireframes",
    ) -> None:
        self.sanctuary_name = sanctuary_name
        self.wireframes_dir = Path(wireframes_dir)
        self.trapper = ErrorTrapper(sanctuary_name=sanctuary_name)
        self._ensure_wireframes_sanctuary()

    def _ensure_wireframes_sanctuary(self) -> None:
        """整流された骨格データを格納する wireframes ディレクトリを保証する"""
        self.wireframes_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def dissolve_and_align(self, fluctuation: Dict[str, Any]) -> Dict[str, Any]:
        """混沌からのペイロードを浄化し、秩序ある構造（ワイヤーフレーム）へ変換する"""
        raise NotImplementedError

    def circulate(self, chaos_packet: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Chaosからのパケットを受け取り、破骨細胞による検査を経て整流パケットまたは隔離パケットを返す"""
        fluctuation = chaos_packet.get("payload", {})
        try:
            wireframe = self.dissolve_and_align(fluctuation)
            return True, {
                "origin": self.sanctuary_name,
                "phase": "aligned",
                "aligned_at": datetime.now(JST).isoformat(),
                "wireframe": wireframe,
            }
        except Exception as e:
            return False, self.trapper.isolate(e, chaos_packet)
