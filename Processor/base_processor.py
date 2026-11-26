from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from typing import Any, Dict

JST = timezone(timedelta(hours=9))


class BaseProcessor(ABC):
    """[Level 2: 心臓・骨芽細胞] 整流されたワイヤーフレームに光・色彩・演出を定着させ、結晶化パケットへ昇華する基底クラス"""

    def __init__(self, sanctuary_name: str = "Processor") -> None:
        self.sanctuary_name = sanctuary_name

    @abstractmethod
    def materialize(self, wireframe: Dict[str, Any]) -> Dict[str, Any]:
        """Entropyからのワイヤーフレーム（カスケード構造等）を受け取り、具現化された成果物（artifact）を生成する"""
        raise NotImplementedError

    def pulse(self, entropy_packet: Dict[str, Any]) -> Dict[str, Any]:
        """Entropyからのパケットを受け取り、骨芽細胞による定着を経て StrataCrystallization へ送出する"""
        phase = entropy_packet.get("phase")

        if phase == "quarantined":
            return {
                "origin": self.sanctuary_name,
                "phase": "skipped_by_metabolism",
                "pulsed_at": datetime.now(JST).isoformat(),
                "reason": "Upstream packet was quarantined by ErrorTrapper",
                "quarantine_report": entropy_packet.get("report"),
            }

        if phase != "aligned":
            return {
                "origin": self.sanctuary_name,
                "phase": "rejected_by_processor",
                "pulsed_at": datetime.now(JST).isoformat(),
                "reason": f"Unsupported upstream phase: {phase}",
            }

        wireframe = entropy_packet.get("wireframe", {})
        artifact = self.materialize(wireframe)

        return {
            "origin": self.sanctuary_name,
            "phase": "ready_for_strata",
            "crystallized_at": datetime.now(JST).isoformat(),
            "artifact": artifact,
        }
